from datetime import datetime
import shutil
import os
import tempfile
import tarfile
import zipfile
import json
import yaml
from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict, Tuple, Union, Any
from pathlib import Path
import pandas as pd
import numpy as np
from pydantic import BaseModel
from shapely.wkt import loads as wkt_loads
from shapely.geometry.base import BaseGeometry as ShapelyShape
from highlighter import HLClient, read_object_classes
from highlighter.base_models import (
        DatasetSubmissionTypeConnection,
        )
from highlighter.const import (
        OBJECT_CLASS_ATTRIBUTE_UUID,
        PIXEL_LOCATION_ATTRIBUTE_UUID,
        )

from highlighter.aws_s3 import download_file_from_s3, list_files_in_s3
from highlighter.datasets.interfaces import IReader
from highlighter.pagination import paginate, DEFAULT_PAGE_SIZE
from highlighter.datasets.formats import get_reader
from highlighter.datasets.base_models import (
        AttributeRecord,
        ImageRecord,
        S3Files,
        DEFAULT_DATA_FILES_KEY,
        DEFAULT_ANNOS_KEY,
        CLOUD_FILES_INFO_KEY,
        )

from highlighter.io import multithread_graphql_file_download, create_data_files
from highlighter.logging import LOG 

KEY_RECORDS = "records"
KEY_FILES = "files"
MANIFEST_YAML = "manifest.yaml"
AWS_S3 = "aws-s3"

__all__ = ["Dataset", "DatasetFormat"]


# Custom representer function for MyUUID
def uuid_representer(dumper, data):
    """Represent UUID|LabeledUUID as a string
    """
    return dumper.represent_scalar('tag:yaml.org,2002:str', str(data))
yaml.add_representer(UUID, uuid_representer)


class DatasetFormat:
    HIGHLIGHTER_WORKFLOW="highlighter-workflow"
    HIGHLIGHTER_DATASET="highlighter-dataset"
    JSON="json"
    HDF="hdf"
    AWS_S3="aws-s3"
    COCO="coco"
    HIGHLIGHTER_ASSESSMENTS="highlighter-assessments"
    DATA_FILE_FOLDER="torch-data_file-folder"


class TempDirAt:
    def __init__(self, path):
        self.path = Path(path)

    def __enter__(self):
        self.path.mkdir(exist_ok=False, parents=True)
        return self.path

    def __exit__(self, type, value, traceback):
        shutil.rmtree(str(self.path))

def md5sum_from_prefix(file_prefix: str):
    parts = Path(file_prefix).stem.split("_")
    if len(parts) == 1:
        # No md5sum in file_prefix
        return None
    else:
        return parts[-1]

def is_uuid(v):
    _is_uuid = False
    try:
        _v = UUID(v)
        _is_uuid = True
    except (ValueError, AttributeError):
        pass
    return _is_uuid


def is_enum_type(v):
    result = False
    if isinstance(v, UUID):
        result = str(v)
    elif is_uuid(v):
        result = v
    return result

def dataset_in_cloud(client: HLClient, dataset_id: int,
    ) -> Tuple[bool, Optional[str]]:
    """Discover if the dataset is in 3rd party cloud storage

    """
    class DatasetInfo(BaseModel):
        id: int
        locationUri: Optional[str]
        format: str


    if client.cloud_creds is None:
        return None, None

    result = client.dataset(
            return_type=DatasetInfo,
            id=dataset_id,
            )

    is_cloud_dataset = result.locationUri is not None
    return is_cloud_dataset, result.locationUri


def get_value_type(v):
    if isinstance(v, bool):
        return v, "boolean"

    _v = is_enum_type(v)
    if _v:
        return _v, "enum"

    if "POLYGON" in str(v):
        return v, PIXEL_LOCATION_ATTRIBUTE_UUID.label
    
    if isinstance(v, np.ndarray):
        return v, "numpy.ndarray"

    return v, type(v).__name__


def unpack_archive(archive_path: Path, unpack_dir: Path):
    archive_path = Path(archive_path)
    unpack_dir = Path(unpack_dir)

    ext = archive_path.suffix
    if ext == ".zip":
        with zipfile.ZipFile(str(archive_path), "r") as storage:
            storage.extractall(unpack_dir)
    
    elif ext in (".tar.gz", ".tar"):
        with tarfile.open(str(archive_path)) as storage:
            storage.extractall(unpack_dir)

def download_s3_files_archives(
        client: HLClient,
        bucket_name: str,
        files_prefixes: List[Path],
        data_files_cache_dir: Path,
        ) -> List[Path]:

    unpacked_files_list: List[str] = []
    for files_prefix in files_prefixes:
        md5sum = md5sum_from_prefix(files_prefix)
        file_cache_path = data_files_cache_dir / Path(files_prefix).name
        file_cache_marker = data_files_cache_dir / f"CACHED_{Path(files_prefix).stem}.yaml"

        _unpacked_files_list: List[str] = []
        if file_cache_marker.exists():
            with file_cache_marker.open("r") as f:
                data = yaml.safe_load(f)

            # Pull in files that have already been downloaded
            unpacked_files_list.extend(data["unpacked_files_list"])
            message = data["message"]
            LOG.info(f"Cache files marker found, {message}")
            continue
            
        LOG.info(f"Downloading s3://{bucket_name}/{files_prefix}")
        download_file_from_s3(
                client,
                bucket_name,
                str(files_prefix),
                str(file_cache_path),
                md5sum=md5sum,  # <-- If None, will not perform check
                )

        # Open a temporary directory in the data_files_cache_dir to unpack the
        # files archive before moving the contents to the final destination
        with TempDirAt(data_files_cache_dir / f"tmp_{files_prefix.stem}") as tmp:
            unpack_archive(file_cache_path, tmp)

            unpacked_files_dir = list(tmp.glob("*"))
            assert len(unpacked_files_dir) == 1
            unpacked_files_dir = unpacked_files_dir[0]

            
            # Move files from data_files_cache_dir/files/* to data_files_cache_dir/
            for f in unpacked_files_dir.rglob("*"):

                # Only interested in moving files not dirs
                if f.is_dir():
                    continue

                # Remove dest file if it exists already
                unpacked_file_rel_path = f.relative_to(unpacked_files_dir)

                # Add to unpacked_files_list so we can return it
                _unpacked_files_list.append(str(unpacked_file_rel_path))

                # Remove dest if exists
                dest = Path(data_files_cache_dir) / unpacked_file_rel_path
                if dest.exists():
                    dest.unlink()

                # Make destination dir as needed
                dest.parent.mkdir(exist_ok=True, parents=True)

                # Move the file
                shutil.move(str(f), str(dest))

      
        # Remove archive file after unpacking.
        os.remove(str(file_cache_path))

        # Create a marker file to indicate the file was downloaded on
        # a given date
        with file_cache_marker.open('w') as f:
            message = f"file s3://{bucket_name}/{files_prefix} downloaded at {datetime.now()}"
            yaml.dump({
                "message": message,
                "unpacked_files_list": _unpacked_files_list,
                }, f)

        unpacked_files_list += _unpacked_files_list
        LOG.info(f"Unpacked {len(_unpacked_files_list)} files")
    return unpacked_files_list


class Dataset():
    REQUIRED_ANNOTATIONS_DF_COLUMNS = set(AttributeRecord.__fields__.keys())
    REQUIRED_DATA_FILES_DF_COLUMNS = set(ImageRecord.__fields__.keys())

    def __init__(
            self,
            dataset_id: int=None,
            annotations_df=None,
            data_files_df=None,
            cloud_files_info: Union[S3Files, List[S3Files]]=None,
            attribute_records: Optional[List[AttributeRecord]]=None,
            data_file_records: Optional[List[ImageRecord]]=None,
            ):
        """

        Params:
            annotations_df: Pandas DataFrame with rows representing AttributeRecord

            data_files_df: Pandas DataFrame with rows representing ImageRecord

            cloud_files_info: Information needed to load download files from a
                              cloud services. At this point we only support S3.
                              See S3Files for more info
            attribute_records: List of AttributeRecords to initialize Dataset with, must
                               include data_file_records too

            data_file_records: List of ImageRecords to initialize Dataset with, must
                               include attribute_records too

        """
        self.dataset_id = dataset_id

        if (annotations_df is not None) and (data_files_df is not None):
            self.annotations_df = annotations_df
            self.data_files_df = data_files_df
        elif attribute_records is not None:
            self.annotations_df = pd.DataFrame([r.to_df_record() for r in attribute_records])
            if data_file_records is not None:
                self.data_files_df = pd.DataFrame([r.dict() for r in data_file_records])
            else:
                self.data_files_df = pd.DataFrame()


        if cloud_files_info is None:
            cloud_files_info = []
        if isinstance(cloud_files_info, (S3Files, dict)):
            cloud_files_info = [cloud_files_info]

        self.cloud_files_info = []
        for c in cloud_files_info:
            if isinstance(c, dict):
                self.cloud_files_info.append(S3Files(**c))
            elif isinstance(c, S3Files):
                self.cloud_files_info.append(c)
            else:
                raise ValueError(f"Expected dict or S3Files object got: {c}")

    @property
    def attributes_df(self):
        """For when I'm lazy and don't want to type annotations_df
        """
        return self.annotations_df

    @classmethod
    def get_reader(cls, dataset_format: str):
        readers = {
            DatasetFormat.JSON: cls.read_json,
            DatasetFormat.HDF: cls.read_hdf,
            DatasetFormat.AWS_S3: cls.read_s3,
            DatasetFormat.HIGHLIGHTER_DATASET: cls.read_highlighter_dataset_assessments,
            DatasetFormat.HIGHLIGHTER_WORKFLOW: cls.read_highlighter_workflow_assessments,
            DatasetFormat.HIGHLIGHTER_ASSESSMENTS: cls.read_assessments_gen,
            DatasetFormat.COCO: cls.read_coco,
            DatasetFormat.DATA_FILE_FOLDER: cls.read_data_file_folder,
                }

        if dataset_format not in readers:
            raise ValueError(f"Invalid dataset format: '{dataset_format}' for reader")

        return readers[dataset_format]

    @classmethod
    def _read_cached_dataset(cls,
                             dataset_path: Path,
                             **reader_kwargs,
                             ) -> Tuple[pd.DataFrame, pd.DataFrame, Optional[pd.DataFrame], Optional[S3Files]]:

        # Drop the '.' from the suffix, ie: '.json' -> 'json'
        dataset_format = dataset_path.suffix[1:]
        reader = cls.get_reader(dataset_format)

        return reader(path=dataset_path, **reader_kwargs)

    @classmethod
    def read_coco(cls, annotations_file: Path, bbox_only: bool=False):
        coco_reader = get_reader("coco")(
                annotations_file,
                bbox_only=bbox_only)
        return cls.load_from_reader(coco_reader)


    @classmethod
    def read_from(cls,
             dataset_format: Union[str, DatasetFormat],
             data_files_cache_dir: Union[str, Path]=None,
             **reader_kwargs,
             ):
        # TODO: All readers must deal with their own caching.

        reader = cls.get_reader(dataset_format)

        ds = reader(**reader_kwargs)

        """It is desirable to add the dataset_id to the annotations_df so a
        dev can easily inspect the data and know where it came from. This is
        especially useful when working with datasets that consist of 2 or more
        other smaller datasets.
        """
        dataset_id = reader_kwargs.get("dataset_id", None)
        if dataset_id is not None:
            ds.annotations_df["dataset_id"] = dataset_id

        """If data_files_cache_dir is provided we download the data_file files
        associated with the datasets.
        """
        if data_files_cache_dir is not None:
            data_files_cache_dir = Path(data_files_cache_dir)
            client = reader_kwargs.get("client")
            assert isinstance(client, HLClient), (
                    "if `data_files_cache_dir` is set you must provide a valid "
                    f"`client` in `reader_kwargs`, got: '{client}'")

            cls.download_dataset_files(
                    client,
                    data_files_cache_dir,
                    data_files_df=ds.data_files_df,
                    cloud_files_info=ds.cloud_files_info,
                    )


        return ds
    
    def append(self, datasets: List["Dataset"]):

        if not isinstance(datasets, (tuple, list)):
            datasets = [datasets]

        for dataset in datasets:
            self.data_files_df = self.data_files_df.append(dataset.data_files_df)
            self.annotations_df = self.annotations_df.append(dataset.annotations_df)
            self.cloud_files_info.extend(dataset.cloud_files_info)


    def apply_split(self, dataset_splitter: "DatasetSplitter"):
        (self.data_files_df,
         self.annotations_df) = dataset_splitter.split(self)


    def get_stats(self, split=None, uuid_to_name=None):
        stats_dict = dict(data_files=dict(), attributes=[])

        if split is not None:
            data_files_df = self.data_files_df[self.data_files_df.split == split]
            if data_files_df.shape[0] == 0:
                unique_splits = self.data_files_df.split.unique()
                raise ValueError(
                        f"No split '{split}' found in dataset. "
                        f"Expected one of; {unique_splits}"
                        )

            data_file_ids = data_files_df.data_file_id
            annotations_df = self.annotations_df[
                    self.annotations_df.data_file_id.isin(data_file_ids)
                    ]
        else:
            data_files_df = self.data_files_df
            annotations_df = self.annotations_df

        stats_dict["data_files"]["count"] = data_files_df.shape[0]

        for attr_id in annotations_df.attribute_id.unique():
            attr_df = annotations_df[annotations_df.attribute_id == attr_id]

            attr_record = dict(
                    id=attr_id,
                    name=attr_df.iloc[0].attribute_name,
                    count=attr_df.shape[0],
                    )

            value, value_type = get_value_type(attr_df.iloc[0].value)
            attr_record["value_type"] = value_type
            attr_record["total"] = attr_df.shape[0]
            if value_type == "enum":
                attr_record["member_counts"] = dict()
                for enum_id in attr_df.value.unique():
                    count_dict = {"count": attr_df[attr_df.value == enum_id].shape[0]}

                    enum_name = uuid_to_name.get(enum_id, None)
                    if enum_name is not None:
                        count_dict["name"] = enum_name

                    attr_record["member_counts"][enum_id] = count_dict

            elif value_type == "boolean":
                attr_record["member_counts"] = dict()
                for val in [True, False]:
                    attr_record["member_counts"][str(val)] = attr_df[attr_df.value == val].shape[0]
            stats_dict["attributes"].append(attr_record)
        return stats_dict

    def _get_uuid_to_name_lookup(self, client):
        """Get uuid for all enum values
        """

        # ToDo: Also get attribute names when gql allows it.

        mask = self.annotations_df.value.apply(is_uuid)
        uuid_values = self.annotations_df[mask].value.unique()
        object_classes = read_object_classes(client, uuid=uuid_values.tolist())
        return {str(o.uuid): o.name for o in object_classes}

    def publish_to_highlighter(
            self,
            client: HLClient,
            dataset_name: str,
            dataset_description_fields: List[Tuple[str, str]]=[],
            split_fracs: Dict[str, int]={},
            ):
        uuid_to_name = self._get_uuid_to_name_lookup(client)

        id_split_name_url = []
        ids = []
        # Loop over the unique splits and create a dataset in
        # highlighter without populating it. We do this so we
        # can get the dataset_ids upfront so we can generate
        # urls to the various splits.
        for split_name in self.data_files_df.split.unique():
            split_frac = split_fracs.get(split_name, None)
            if split_frac is not None:
                split_str = f"{split_name}-{split_frac}"
            else:
                split_str = split_name

            name = "_".join([
                     f"{datetime.now().strftime('%Y-%m-%d')}",
                     f"{dataset_name}",
                     f"{split_str}",
                   ])

            class DatasetType(BaseModel):
                id: int

            class CreateDatasetPayload(BaseModel):
                dataset: Optional[DatasetType]
                errors: list

            class DatasetPayload(BaseModel):
                dataset: Optional[DatasetType]
                errors: Optional[list]

            class SubsAndHashes(BaseModel):
                id: int
                hashSignature: str

            response = client.createDataset(
                    return_type=CreateDatasetPayload,
                    name=name,
                    description=name,
                    )

            if len(response.errors) > 0:
                raise ValueError(response.errors)

            id = response.dataset.id
            url = client.endpoint_url.replace("graphql", f"datasets/{id}")
            id_split_name_url.append((id, split_name, name, url))
            ids.append(id)
            print(f"Created dataset: {id}")

        def fix_underscores(n):
            return n.replace('_', '\\_')

        dataset_markdown_links = [
                f"[{id}]({url}): {fix_underscores(name)}" for id, _, name, url in id_split_name_url
                ]
        stats_dict = self.get_stats(uuid_to_name=uuid_to_name)
        global_stats_str = yaml.dump(stats_dict)

        df = self.data_files_df
        for idx, (id, split_name, name, url) in enumerate(id_split_name_url):
            records = df.loc[
                    df.split == split_name,
                    ["assessment_id", "hash_signature"]
                    ].to_dict("records")

            subs_and_hashes = [SubsAndHashes(
                id=r["assessment_id"],
                hashSignature=r["hash_signature"],
                ).dict() for r in records]

            response = client.populateDataset(
                    return_type=DatasetPayload,
                    datasetId=id,
                    submissionIdsAndHashes=subs_and_hashes,
                    )

            if response.errors:
                class DatasetPopulateError(Exception):
                    pass
                raise DatasetPopulateError("\n".join(response.errors))

            dataset_description = [
                    f"# {dataset_name.replace('-', ' ').replace('_', ' ').title()}\n",
                    f"**Dataset {id}**",
                    ]

            if len(id_split_name_url) >  1:
                # Make list of links
                # Make current split bold but remove url link
                def make_bold_remove_url(l):
                    return f'**{l[1:].split("]")[0]}**'

                links = [
                        f"  - {make_bold_remove_url(l)}: You are here 😀" if i == idx else f"  - {l}"
                        for i, l in enumerate(dataset_markdown_links)
                        ]

                links_str = "\n".join(links)
                _dataset_description_fields = [("Related Splits", links_str)] + dataset_description_fields
            else:
                _dataset_description_fields = dataset_description_fields


            dataset_description.extend([f"## {heading}\n\n{value}\n" for
                    heading, value in _dataset_description_fields])

            split_stats_str = yaml.dump(self.get_stats(
                split=split_name,
                uuid_to_name=uuid_to_name,
                ))

            dataset_description.extend([
                f"## {split_name.title()} Split Stats\n\n<pre>{split_stats_str}</pre> \n",
                ])

            dataset_description.extend([
                f"## Golbal Stats\n\n<pre>{global_stats_str}</pre> \n",
                ])

            dataset_description_str = "\n".join(dataset_description)

            response = client.updateDataset(
                    return_type=DatasetPayload,
                    id=id,
                    description=dataset_description_str,
                    )

            if len(response.errors) > 0:
                raise ValueError(response.errors)

            print(f"Populated Dataset: {id} with {len(subs_and_hashes)} assessments")

            response = client.lockDataset(
                    return_type=DatasetPayload,
                    datasetId=id,
                    )
            print(f"Locked Dataset: {id}")
            print(f"See dataset at: {url}")
        return ids


    @classmethod
    def combine(cls, datasets: List["Dataset"]):
        if len(datasets) == 1:
            return datasets[0]

        if len(datasets) == 0:
            raise ValueError("Expected list of Dataset objects, got []")

        base_ds = datasets[0]
        base_ds.append(datasets[1:])
        return base_ds


    @classmethod
    def download_dataset_files(
            cls,
            client: HLClient,
            data_files_cache_dir: Path,
            data_files_df: pd.DataFrame=None,
            cloud_files_info: List[S3Files]=None,
            **kwargs,
            ):
        data_files_cache_dir = Path(data_files_cache_dir)

        existing_file_paths: List[Path] = []
        if cloud_files_info is not None:
            for info in cloud_files_info:
                files_prefixes = [Path(info.prefix) / file for file \
                        in info.files]

                # paths relative to data_files_cache_dir
                existing_file_paths = download_s3_files_archives(
                    client,
                    info.bucket_name,
                    files_prefixes,
                    data_files_cache_dir,
                        )


        if data_files_df is not None:
            existing_file_strs: List[str] = [str(p) for p in existing_file_paths]

            data_files_to_download = data_files_df[~data_files_df.filename.isin(existing_file_strs)].data_file_id.unique()
            multithread_graphql_file_download(
                    client,
                    list(data_files_to_download),
                    data_files_cache_dir,
                    **kwargs,
                    )

    @classmethod
    def read_highlighter_workflow_assessments(
            cls,
            *,
            client: HLClient,
            queryArgs: Dict,
            **kwargs,
            ):
        """Instantiate a Dataset from a Highlighter workflow assessments.

        You can provide dict of queryArgs that will be used to compile a
        GraphQL query. The resulting assessments will populate the Dataset

        If you need to download accompanying data_files you can
        either use the generic `Dataset.read` classmethod or use
        `Dataset.download_dataset_files`
        """
        from highlighter.assessments import get_latest_assessments_gen

        assessments_gen = get_latest_assessments_gen(
                client,
                **queryArgs,
                )

        return cls.read_assessments_gen(assessments_gen=assessments_gen)


    @classmethod
    def read_highlighter_dataset_assessments(
            cls,
            client: HLClient,
            dataset_id: int,
            datasets_cache_dir: Path=None,
            page_size: int=DEFAULT_PAGE_SIZE,
            **kwargs,
            ):

        """Check for cached dataset
        """
        if datasets_cache_dir is not None:
            datasets_cache_dir = Path(datasets_cache_dir)
            dataset_cache_path = datasets_cache_dir / f"records_{dataset_id}.json"
            if dataset_cache_path.exists():
                return cls.read_json(path=dataset_cache_path)
        else:
            dataset_cache_path = None

        _assessments_gen = paginate(
                client.datasetSubmissionConnection,
                DatasetSubmissionTypeConnection,
                page_size=page_size,
                datasetId=dataset_id,
                )
        
        # datasetSubmissionConnection nests the SubmissionType
        # inside the node object as opposed to the SubmissionType
        # being the node object. So we unpack it here so to
        # adhear to a consistent interface
        assessments_gen = (
                node.submission for node in _assessments_gen
                )

        ds = cls.read_assessments_gen(assessments_gen=assessments_gen)

        """If we can, cache the dataset locally
        """
        if dataset_cache_path is not None:
            ds.write_json(dataset_cache_path)

        return ds



    @classmethod
    def read_assessments_gen(
            cls,
            assessments_gen,
            ):
        """Load data_files_df, annotatoins_df from a Highlighter assessments
        generator. Returns these as a tuple to be used by the generic
        `Dataset.read` classmethod
        """
        from highlighter.datasets.formats.highlighter.reader import HighlighterAssessmentsReader

        reader = HighlighterAssessmentsReader(assessments_gen)
        return cls.load_from_reader(reader)


    def download_files_from_datasource(
            self,
            client: HLClient,
            data_files_cache_dir: Path,
            data_file_ids: List[int],
            page_size: int=DEFAULT_PAGE_SIZE,
            ):
        data_files_cache_dir = Path(data_files_cache_dir)
        multithread_graphql_file_download(
                client,
                list(ds.data_files_df.data_file_id.unique()),
                data_files_cache_dir,
                **kwargs,
                )

    @classmethod
    def read_hdf(
            cls,
            path: Path,
            data_files_key: Optional[str] = DEFAULT_DATA_FILES_KEY,
            annotations_key: Optional[str] = DEFAULT_ANNOS_KEY,
            **kwargs,
            ):
        """Instantiate a Dataset from a local .hdf file

        If you need to download accompanying data_files you can
        either use the generic `Dataset.read` classmethod or use
        `Dataset.download_dataset_files`
        """
        path = Path(path)

        annotations_df = pd.read_hdf(path, key=annotations_key)
        data_files_df = pd.read_hdf(path, key=data_files_key)

        try:
            cloud_files_info = pd.read_hdf(path, key=CLOUD_FILES_INFO_KEY)
            cloud_files_info = [S3Files.safe_load(**info) for info in cloud_files_info.to_dict("records")]
        except KeyError:
            # cloud files key is optional
            cloud_files_info = None


        return cls(
                data_files_df=data_files_df,
                annotations_df=annotations_df,
                cloud_files_info=cloud_files_info,
                )


    def write_json(
            self,
            path: Path,
            data_files_key: Optional[str] = DEFAULT_DATA_FILES_KEY,
            annotations_key: Optional[str] = DEFAULT_ANNOS_KEY,
            ):

        payload = {}
        if len(self.cloud_files_info) > 0:
            payload[CLOUD_FILES_INFO_KEY] = [c.dict() for c in self.cloud_files_info]

        payload[annotations_key] = self.annotations_df.to_dict("records")
        payload[data_files_key] = self.data_files_df.to_dict("records")

        
        class ShapelyGeometryEncoder(json.JSONEncoder):
            def default(self, obj: Any) -> Any:
                if isinstance(obj, ShapelyShape):
                    return obj.wkt  # Convert BaseGeometry instances to WKT
                # Let the base class default method raise the TypeError
                return json.JSONEncoder.default(self, obj)

        path = Path(path)
        with path.open("w") as f:
            json.dump(payload, f, cls=ShapelyGeometryEncoder)

    @classmethod
    def read_data_file_folder(cls,
                          *,
                          path: Path,
                          attribute_id: str = str(OBJECT_CLASS_ATTRIBUTE_UUID),
                          attribute_name: str = OBJECT_CLASS_ATTRIBUTE_UUID.label,
                          ):
        from highlighter.datasets.formats.torch_image_folder.reader import TorchImageFolderReader

        reader = TorchImageFolderReader(path,
                                        attribute_id=attribute_id,
                                        attribute_name=attribute_name)
        return cls.load_from_reader(reader)

    @classmethod
    def load_from_reader(cls, reader: IReader):
        data_file_records, attribute_records = reader.read()

        if len(data_file_records) == 0:
            raise ValueError((f"Could not populate Dataset object from "
            f"{reader}. This could be because the "
            f"HLClient.endpoint_url is incorrect, or, if "
            "The dataset is stored as a 'cloud dataset' maybe the cloud credenials "
            "are incorrect/missing"))

        annotations_df = pd.DataFrame([r.to_df_record() for r in attribute_records])
        data_files_df = pd.DataFrame([r.dict() for r in data_file_records])
        return cls(data_files_df=data_files_df,
                   annotations_df=annotations_df)


    @classmethod
    def read_json(
            cls,
            path: Path,
            data_files_key: Optional[str] = DEFAULT_DATA_FILES_KEY,
            annotations_key: Optional[str] = DEFAULT_ANNOS_KEY,
            **kwargs,
            ):
        """Instantiate a Dataset from a local .json file

        If you need to download accompanying data_files you can
        either use the generic `Dataset.read` classmethod or use
        `Dataset.download_dataset_files`
        """
        # Make sure path is a Path object
        path = Path(path)

        class ShapelyGeometryDecoder(json.JSONDecoder):
            def __init__(self, *args, **kwargs):
                super().__init__(object_hook=self.dict_to_object, *args, **kwargs)
                self.WKT_INDICATORS = ("POLYGON", "MULTIPOLYGON", "POINT", "LINESTRING")
        
            def dict_to_object(self, d: dict) -> dict:
                if ("value" in d)  and isinstance(d["value"], str) and (d["value"].split(" ")[0] in self.WKT_INDICATORS):
                    d["value"] = wkt_loads(d["value"])
                return d

        with path.open("r") as f:
            data = json.load(f, cls=ShapelyGeometryDecoder)

        if annotations_key in data:
            attr_list = data[annotations_key]
        else:
            attr_list = data["attributes"]

        annotations_df = pd.DataFrame(attr_list)

        data_files_df = pd.DataFrame(data[data_files_key])

        cloud_files_info = data.get(CLOUD_FILES_INFO_KEY, None)

        if isinstance(cloud_files_info, dict):
            """Some older instances of cloud_files_info have a single dict
            not a list as is standard now
            """
            cloud_files_info = [cloud_files_info]

        assert (cloud_files_info is None) or isinstance(cloud_files_info, list)
        
        if isinstance(cloud_files_info, list):
            cloud_files_info = [S3Files(**info) for info in cloud_files_info]

        return cls(
                data_files_df=data_files_df,
                annotations_df=annotations_df,
                cloud_files_info=cloud_files_info,
                )


    @classmethod
    def read_s3(
            cls,
            client: HLClient,
            dataset_id: int,
            datasets_cache_dir: Path=None,
            data_files_key: Optional[str] = DEFAULT_DATA_FILES_KEY,
            annotations_key: Optional[str] = DEFAULT_ANNOS_KEY,
            **kwargs,
            ):
        """
        Will attempt to download dataset records from s3 and instantiate
        a Dataset object. Optioally will download files associated with records.

        NOTE: we're in the process of renaming `annotations` to `attributes` and
              `data_files` to `files`. So keep that in mind when reading this doc
              string.

        Highlighter Datasets are stored a directory with the `training_run_id`
        as the name. This dir contains two types of files; `records` and `files`.

        s3://my-bucket/datasets/123/       <-- `dataset_id` 123
            records_<md5sum>.<json | hdf>  <-- contains EAVT information
            files_<md5sum>.tar.gz          <-- one or more file archives contain
                                            the files references in `records`                  
            ...

        records: Is a `.json` or `.hdf` file containing Entity Attribute Value Type
                 information. This information is loaded into the Dataset's
                 `data_files_df` and `annotations_df`. For more information on the
                 underlying Dataframe's and their schema see the doc string
                 for the Dataset class.

        files: A `.tar.gz|.tar|.zip` archive file containing the files refered
               to in the `data_files_df`. If there is a large number of files these
               archives can be broken up into smaller chunks each with a unique
               md5sum. When unpacked, each archive must contain a singel directory
               names 'files' that contains the files refered to in `data_files_df`.
               NOTE: `data_files_df.filename` should NOT include 'files/' as this
               dir will be dropped when unpacking the archive.

        Params:
            bucket_name: name of s3 bucket. (above example = 'my-bucket')

            dataset_id: id of dataset to download  (above example = 123)

            client: a HLClient with the correct cloud credenials

            prefix: Relitave path to datasets dir (above example = 'datasets/123')

            files_cache: If supplied will download files archive from s3 and
                         unpack here
        """

        """Check for cached dataset
        """
        if datasets_cache_dir is not None:
            datasets_cache_dir = Path(datasets_cache_dir)

            dataset_cache_path = datasets_cache_dir / f"records_{dataset_id}.json"
            if dataset_cache_path.exists():
                return cls.read_json(path=dataset_cache_path)

        """No cached dataset found, read from s3
        """
        class DatasetInfo(BaseModel):
            id: int
            locationUri: Optional[str]
            format: str

        if client.cloud_creds is None:
            raise ValueError("Cannot read an s3 dataset without cloud_creds")

        result = client.dataset(
                return_type=DatasetInfo,
                id=dataset_id,
                )

        location_uri = result.locationUri

        assert location_uri.startswith("s3://")

        # S3 bucket_name is the first part in the uri after the s3://
        bucket_name = location_uri[5:].split("/")[0]

        prefix = "/".join(location_uri[5:].split("/")[1:])

        # the aws s3 cli treats prefixes with a trailing /
        # differenly to those without. It seems Boto3 is not
        # as tempormental, but just to be consistent.
        if prefix.endswith("/"):
            prefix = prefix[:-1]

        s3_contents = list_files_in_s3(
                client,
                bucket_name,
                prefix,
                )


        # Download MANIFEST_YAML that contains list of files in the dataset
        manifest_file_prefix = [x for x in s3_contents if Path(x).name == MANIFEST_YAML]
        assert len(manifest_file_prefix) == 1
        manifest_file_prefix = manifest_file_prefix[0]
        with tempfile.TemporaryDirectory() as tmp:
            tmp_manifes_path = Path(tmp) / MANIFEST_YAML
            download_file_from_s3(
                    client,
                    bucket_name,
                    str(manifest_file_prefix),
                    str(tmp_manifes_path),
                    )
            with tmp_manifes_path.open("r") as f:
                manifest = yaml.safe_load(f)


        with tempfile.TemporaryDirectory() as tmp:
            records_filename = manifest[KEY_RECORDS][0]
            records_md5sum = md5sum_from_prefix(records_filename)
            tmp_path = Path(tmp) / records_filename

            records_file_prefix = f"{prefix}/{records_filename}"
            download_file_from_s3(
                    client,
                    bucket_name,
                    records_file_prefix,
                    str(tmp_path),
                    md5sum=records_md5sum,  # <-- If None, will not perform check
                    )

            ext = tmp_path.suffix[1:]
            reader = cls.get_reader(ext)
            ds = reader(
                    path=tmp_path,
                    data_files_key=data_files_key,
                    annotations_key=annotations_key,
                    )

        """If we can, cache the dataset locally
        """
        if datasets_cache_dir is not None:
            ds.write_json(dataset_cache_path)

        return ds


    def write_hdf(self,
            path: Path,
            data_files_key: Optional[str] = DEFAULT_DATA_FILES_KEY,
            annotations_key: Optional[str] = DEFAULT_ANNOS_KEY,
            ):
        self.data_files_df.to_hdf(
            path, key=data_files_key, mode="w",
        )
        self.annotations_df.to_hdf(
            path, key=annotations_key, mode="a",
        )


        if len(self.cloud_files_info) > 0:
            payload = [c.dict() for c in self.cloud_files_info]
            tmp_df = pd.DataFrame(payload)
            tmp_df.to_hdf(path, key=CLOUD_FILES_INFO_KEY, mode="a")

    def upload_data_files(self,
                      client: HLClient,
                      data_source_id: int,
                      progress = False,
                      data_file_dir: Union[str, Path] = "",
                      multipart_filesize: Optional[str] = None,
                      ):
        data_file_dir_path = Path(data_file_dir)
        append_data_file_dir = lambda f: str(data_file_dir_path / f)
        self.data_files_df.loc[:,"filename"] = self.data_files_df.filename.map(append_data_file_dir)

        data_file_path_to_id, failed_data_file_paths = create_data_files(
                client,
                self.data_files_df.filename.values,
                data_source_id,
                progress=progress,
                multipart_filesize=multipart_filesize,
                )

        old_data_file_ids = self.data_files_df.data_file_id.values
        self.data_files_df.loc[:,"data_file_id"] = self.data_files_df.filename.map(data_file_path_to_id)

        new_data_file_ids = self.data_files_df.data_file_id.values
        old_to_new_data_file_ids = {o: n for o, n in zip(old_data_file_ids, new_data_file_ids)}
        self.annotations_df.loc[:,"data_file_id"] = self.annotations_df.data_file_id.map(old_to_new_data_file_ids)

        LOG.debug(f"{len(data_file_path_to_id)} succeeded, {len(failed_data_file_paths)} failed -> {failed_data_file_paths}")

