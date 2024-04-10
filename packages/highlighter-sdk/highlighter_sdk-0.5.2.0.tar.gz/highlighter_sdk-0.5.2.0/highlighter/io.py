import warnings
from io import BytesIO
from itertools import chain
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple, Union
from urllib.parse import urlparse

import numpy as np
import requests
from PIL import Image, ImageOps
from tqdm import tqdm

from highlighter.base_models import (TrainingRunArtefactTypeEnum,
                                               TrainingRunType)
from highlighter.const import DEPRECATED_CAPABILITY_IMPLEMENTATION_FILE
from highlighter.gql_client import HLClient
from highlighter.data_files import get_data_files
from highlighter.itertools import iterbatch
from highlighter.logging import LOG as logger

from .presigned_url import get_presigned_urls


def _pil_open_image_path(data_file_path: str):
    data_file = Image.open(data_file_path)
    data_file = ImageOps.exif_transpose(data_file)
    return data_file


def _pil_open_image_bytes(data_file_bytes: bytes):
    data_file = Image.open(BytesIO(data_file_bytes))
    data_file = ImageOps.exif_transpose(data_file)
    return data_file


def read_image(data_file_path: Union[str, Path]) -> np.ndarray:
    """Reads an data_file located at the path given.

    Args:
        data_file_path: The path of the data_file to read.

    Returns:
        The data_file as an array.
    """
    data_file = _pil_open_image_path(str(data_file_path))
    data_file = np.array(data_file).astype("uint8")

    if data_file is None:
        raise IOError("Unable to read data_file at path {}".format(data_file_path))

    return data_file


def read_artefact(
    client: HLClient,
    training_run_id: int,
    save_path: Path,
    artefact_type: Union[TrainingRunArtefactTypeEnum, str],
):

    result = client.trainingRun(return_type=TrainingRunType, id=training_run_id)

    # Validate artefact_type
    if isinstance(artefact_type, TrainingRunArtefactTypeEnum):
        artefact_type = artefact_type.value
    elif artefact_type == DEPRECATED_CAPABILITY_IMPLEMENTATION_FILE:
        pass
    elif isinstance(artefact_type, str):
        try:
            artefact_type = TrainingRunArtefactTypeEnum(artefact_type)
            artefact_type.value
        except ValueError:
            choices = list(TrainingRunArtefactTypeEnum.__members__.keys())
            choices += [DEPRECATED_CAPABILITY_IMPLEMENTATION_FILE]
            raise ValueError(
                f"artefact_type '{artefact_type}', must be of type TrainingRunArtefactTypeEnum or one of: {choices}"
            )

    if artefact_type == DEPRECATED_CAPABILITY_IMPLEMENTATION_FILE:
        file_url = result.modelImplementationFileUrl
    else:
        if not result.trainingRunArtefacts:
            raise ValueError(f"No trainingRunArtefacts associated with {id}")

        artefacts = [a for a in result.trainingRunArtefacts if a.type == artefact_type]

        if len(artefacts) == 0:
            raise ValueError(
                f"No trainingRunArtefacts of type {artefact_type} associated "
                f"with {id}"
            )

        artefact = sorted(artefacts, key=lambda d: d.updatedAt)[-1]
        file_url = artefact.fileUrl

    download_bytes(
        file_url,
        save_path=save_path,
    )


def write_image(save_path: str, data_file: np.ndarray, is_rgb: bool = True) -> None:
    """Saves an data_file to the path given.

    Args:
        save_path: The path to save the data_file to.
        data_file: The data_file to save.
        is_rgb: Whether or not the array is in RGB order. If False, it is
            assumed to be in BGR format.
    """
    if not is_rgb:
        data_file = data_file[:, :, [2, 1, 0]]
    # print(save_path)

    img = Image.fromarray(data_file.astype("uint8"))

    if img.mode == "RGBA":
        img = rgba_to_rgb(img)

    img.save(save_path)


def _to_cache_path(url: str, cachedir: Path) -> Path:
    """Infer path to target file in cachedir. Converting the file extention to
    lower
    """
    path = Path(urlparse(url).path)
    ext = path.suffix.lower()
    stem = path.stem
    return cachedir / f"{stem}{ext}"


def _is_in_cache(url: str, cachedir: Optional[Path]):
    if cachedir is None:
        return False, None

    path = _to_cache_path(url, cachedir)
    return path.exists(), path


def download_bytes(url: str, save_path: Path = None, check_cached=False):
    """Download contents as bytes from url. Optioanlly save to save_path"""
    if check_cached and save_path.exists():
        return

    response = requests.get(url)
    if not response.ok:
        raise ValueError(
            f"encounter network issue, status code: {response.status_code} downloading from {url}"
        )
    data_bytes = response.content
    if save_path is None:
        return data_bytes
    else:
        with save_path.open("wb") as f:
            f.write(data_bytes)


def read_image_from_url(url: str, cachedir: Path = None) -> np.ndarray:
    in_cache, path = _is_in_cache(url, cachedir)

    if in_cache:
        data_file = _pil_open_image_path(path)
    else:
        data_file_bytes = download_bytes(url)
        data_file = _pil_open_image_bytes(data_file_bytes)

        if cachedir is not None:
            data_file.save(path)
            logger.debug("Succesfully wrote cached data_file to %s", path)

    return np.array(data_file).astype("uint8")


def try_download_file(*, file_id, file_dst, file_url, overwrite_existing=False):

    result = {file_id: str(file_dst)}

    if (not Path(file_dst).exists()) or (overwrite_existing):
        try:
            download_bytes(file_url, save_path=Path(file_dst), check_cached=True)
        except Exception as e:
            warnings.warn(
                (
                    "Warning: An error occured when downloading file "
                    f"{file_url}. Exception: {e}"
                )
            )
            result = {file_id: None}
    return result


def _separate_downloadable_from_cached_file(
    file_ids: List[Union[int, str]], cache_dir: Path
) -> Tuple[Set[str], Dict[str, Path]]:
    """
    Glob cache_dir for each file_id in file_ids.
    Returns:
      to_download: list of ids to download
      id_to_path_map: Dict[<id>, <path-to-file-in-cache>]
    """
    all_cached_id_to_path = {p.stem: p for p in Path(cache_dir).glob("*")}
    all_cached_file_ids = set(all_cached_id_to_path.keys())

    file_id_strs = {str(i) for i in file_ids}
    to_download = file_id_strs.difference(all_cached_file_ids)
    cached_file_ids_we_want = all_cached_file_ids.intersection(file_id_strs)
    id_to_path_map = {i: all_cached_id_to_path[i] for i in cached_file_ids_we_want}
    return (to_download, id_to_path_map)


def _generator_empty(gen) -> bool:
    try:
        first = next(gen)
        is_empty = False
        _gen = chain([first], gen)
    except StopIteration:
        is_empty = True
        _gen = None
    return is_empty, _gen


def multithread_graphql_file_download(
    client: HLClient,
    file_ids: List[int],
    cache_dir: Path,
    threads: int = 8,
    chunk_size: int = 20,
):
    """Downloads files from Highlighter.

    Using multiple thread download files from Highlighter given the file ids.
    If an file alread exists in 'cache_dir' with the same id. The download
    will be skipped in favour of the file on disk.

    If you experience timeout issues due to the download taking too long per
    chunk consider lowerig the 'chunk_size'.

    Args:
      file_ids List[str|int]: Ids of files to download
      cache_dir [str]: If not exists, will be created
      threads optional[int]: Number of parallel threads to open
      chunk_size: optional[int]: Number of presigned_urls to get at once. At
          the time of writing this doc the timeout is 900sec (15min). If you
          experience timeout issues due to the download taking too long per
          chunk consider lowerig the 'chunk_size'.

    Returns:
      Dict[<id>, <path|None>]: Map of file_ids to their path on disk. If something
          went wrong during the download the value of the path will be None.

    """
    from multiprocessing.pool import ThreadPool

    Path(cache_dir).mkdir(parents=True, exist_ok=True)

    ids_to_download, id_to_path_map = _separate_downloadable_from_cached_file(
        file_ids, cache_dir
    )

    print(f"Found: {len(id_to_path_map)} of total {len(file_ids)}")
    print(f"Downloading {len(ids_to_download)} files using {threads} threads.")

    def dl_file(gql_response):
        file_id = int(gql_response.id)
        file_url = gql_response.fileUrlOriginal

        ext = Path(gql_response.originalSourceUrl).suffix.lower()
        file_dst = str(Path(cache_dir) / f"{file_id}{ext}")
        return try_download_file(
            file_id=file_id,
            file_dst=file_dst,
            file_url=file_url,
            overwrite_existing=False,
        )

    chunks = tqdm(
        iterbatch(ids_to_download, chunk_size),
        total=len(ids_to_download) // chunk_size,
        desc="Downloading file",
    )

    if threads > 1:
        with ThreadPool(processes=threads) as pool:
            for chunk in chunks:
                url_gen = get_presigned_urls(
                    client,
                    [int(file_id) for file_id in chunk],
                )

                is_empty, url_gen = _generator_empty(url_gen)
                if is_empty:
                    raise ValueError("No data_file urls found")

                for result in pool.imap_unordered(dl_file, url_gen):
                    id_to_path_map.update(result)
    else:
        for chunk in chunks:
            url_gen = get_presigned_urls(
                client,
                [int(file_id) for file_id in chunk],
            )

            is_empty, url_gen = _generator_empty(url_gen)
            if is_empty:
                raise ValueError("No data_file urls found")

            for gql_response in url_gen:
                result = dl_file(gql_response)

                id_to_path_map.update(result)

    return id_to_path_map


def create_data_files(
    client: HLClient,
    data_file_paths: Iterable[Union[str, Path]],
    data_source_id: int,
    threads: int = 8,
    progress: bool = False,
    multipart_filesize: Optional[str] = None,
) -> List[str]:
    from multiprocessing.pool import ThreadPool
    from warnings import warn

    from .data_files import create_data_file

    def get_progress_bar(progress, desc=None, total=None):
        if progress:
            pbar = tqdm(desc=desc, total=total)
        else:

            class MockPbar:
                def update(self):
                    pass

                def close(self):
                    pass

            pbar = MockPbar()
        return pbar

    total = getattr(data_file_paths, "__len__", lambda: None)()

    pbar = get_progress_bar(progress=progress, desc="create_data_files", total=total)

    def _create_data_file(data_file_path, client=client, data_source_id=data_source_id):
        data_file_path = str(data_file_path)
        try:

            # Create a temporary client because we can't have the
            # same client makeing multiple requests at the same time.
            # ToDo: Look into this.
            thread_client = HLClient.from_credential(
                api_token=client.api_token, endpoint_url=client.endpoint_url
            )

            data_file_info = create_data_file(
                thread_client,
                data_file_path,
                data_source_id,
                multipart_filesize=multipart_filesize,
            )

            return "SUCCESS", (data_file_info.id, data_file_path)

        except FileNotFoundError as e:
            warn(f"File not found: {e}")
            return "FAILED", data_file_path

        except Exception as e:
            if str(e) == "Original source url has already been taken":
                return "IMAGE_EXISTS", data_file_path
            else:
                warn(f"{e}")
                return "FAILED", data_file_path

    failed: List[str] = []
    data_file_path_to_id: Dict[str, int] = {}
    existing_data_file_paths: List[str] = []
    with ThreadPool(processes=threads) as pool:
        for outcome, result in pool.imap_unordered(_create_data_file, data_file_paths):

            if outcome == "SUCCESS":
                hl_data_file_id, data_file_path = result
                data_file_path_to_id[data_file_path] = hl_data_file_id

            elif outcome == "IMAGE_EXISTS":
                data_file_path = result
                existing_data_file_paths.append(data_file_path)

            elif outcome == "FAILED":
                failed_data_file_path = result
                failed.append(str(failed_data_file_path))

            else:
                raise ValueError()

            pbar.update()
    pbar.close()

    if len(failed) > 0:
        warn(f"Failed data_files: {failed}")

    if len(existing_data_file_paths) > 0:
        warn(
            f"Skipped uploading {len(existing_data_file_paths)} files to Data Source {data_source_id} because they already exist"
        )

    data_source_data_files = get_data_files(client, data_source_id=[data_source_id])
    existing_data_file_path_to_id = {
        o.originalSourceUrl: o.id
        for o in data_source_data_files
        if o.originalSourceUrl in existing_data_file_paths
    }
    data_file_path_to_id.update(existing_data_file_path_to_id)

    return data_file_path_to_id, failed

