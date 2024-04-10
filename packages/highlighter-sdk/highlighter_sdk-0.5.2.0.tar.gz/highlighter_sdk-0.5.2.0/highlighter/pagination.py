import asyncio
import os

from tqdm import tqdm

__all__ = [
        "paginate",
        ]

DEFAULT_PAGE_SIZE=int(os.environ.get("HCP_PAGINATE_PAGE_SIZE", "200"))

def paginate(
        fn,
        return_type,
        page_size=DEFAULT_PAGE_SIZE,
        **kwargs,
    ):
    """
    fn: Graphql query that supports pagination
    return_type: Must contain be a BaseModel that contains

        pageInfo: PageInfo
        nodes: List[...]

    Where List[...] is a list of the type of the thing you want
    to return. EG

    class DatasetAssessmentType(BaseModel):
      stuff: ...

    class DatasetSubmissionTypeConnection(BaseModel):
      pageInfo: PageInfo
      nodes: List[DatasetAssessmentType]

    client = HLClient...
    generator = paginate(
        client.datasetSubmissionConnection,
        DatasetSubmissionTypeConnection,
        datasetId=123,
        )

    """
    def get_response(**kwargs):
        try:
            response = fn(
                    return_type=return_type,
                    first=page_size,
                    **kwargs,
                    )
            pbar.update(page_size)
        except asyncio.exceptions.TimeoutError:
            message = f"This could be becuase page_size ({page_size}) is too large"
            raise asyncio.exceptions.TimeoutError(message)
        return response

    with tqdm(desc=return_type.__name__) as pbar:
        response = get_response(**kwargs)

        for node in response.nodes:
            yield node

        while response.pageInfo.hasNextPage:
            kwargs["after"] = response.pageInfo.endCursor
            response = get_response(**kwargs)

            for node in response.nodes:
                yield node
