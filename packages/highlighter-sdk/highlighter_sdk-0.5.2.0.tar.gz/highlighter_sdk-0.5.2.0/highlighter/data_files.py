from datetime import datetime
import warnings
from pathlib import Path
from typing import List, Optional, Any, Union
from pydantic import BaseModel
from .pagination import paginate
from . import HLClient, PageInfo, ImageType
from .aws_s3 import upload_file_to_s3
from .presigned_url import get_presigned_url, get_presigned_urls

__all__ = [
        "get_presigned_data_file",
        "get_presigned_data_files",
        "get_data_files",
        ]


def get_data_files(
        client,
        data_file_ids: Optional[List[int]]=None,
        data_source_id: Optional[List[int]]=None,
        ):

    class ImageTypeConnection(BaseModel):
        pageInfo: PageInfo
        nodes: List[ImageType]

    kwargs = {"id": data_file_ids,
              "dataSourceId": data_source_id}
    kwargs = {k:v for k,v in kwargs.items() if v is not None}

    return paginate(
            client.imageConnection,
            ImageTypeConnection,
            **kwargs
            )

def get_presigned_data_file(
        client: HLClient,
        id: int,
        ):
    warnings.warn("get_presigned_data_file is deprecated use get_presigned_url")
    return get_presigned_url(
            client,
            id,
            )

def get_presigned_data_files(
        client,
        ids: List[int],
        ):
    warnings.warn("get_presigned_data_files is deprecated use get_presigned_urls")
    return get_presigned_urls(
            client,
            ids,
            )

def create_data_file(client: HLClient,
                 data_file_path: Union[str, Path],
                 data_source_id: int,
                 site_id: Optional[str]=None,
                 observed_timezone: Optional[str]=None,
                 recorded_at: Optional[str]=None,
                 metadata: str="{}",
                 uuid: Optional[str]=None,
                 multipart_filesize: Optional[str]=None,
                 ) -> ImageType:

    data_file_path = Path(data_file_path)
    if not data_file_path.exists():
        raise FileNotFoundError(f"{data_file_path}")

    file_data = upload_file_to_s3(client, str(data_file_path), multipart_filesize=multipart_filesize)

    if recorded_at is None:
        recorded_at = datetime.now().isoformat()

    class CreateImageResponse(BaseModel):
        image: Optional[ImageType]
        errors: Any


    create_data_file_response = client.create_image(return_type=CreateImageResponse,
                                                dataSourceId=data_source_id,
                                                originalSourceUrl=str(data_file_path),
                                                fileData=file_data,
                                                siteId=site_id,
                                                observedTimezone=observed_timezone,
                                                recordedAt=recorded_at,
                                                metadata=metadata,
                                                uuid=uuid,
                                                contentType="image",
                                                )

    if create_data_file_response.errors:
        raise ValueError(". ".join(create_data_file_response.errors))
    return create_data_file_response.image
