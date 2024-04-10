from pydantic import BaseModel
from typing import List

from highlighter import (
        HLClient,
        SubmissionTypeConnection,
        )
from highlighter.pagination import paginate

def get_latest_assessments_gen(
        client: HLClient,
        **kwargs,
        ):

    query_args = {k: v for k, v in kwargs.items() if v is not None}
    assessments_gen = paginate(
            client.latestSubmissionConnection,
            SubmissionTypeConnection,
            **query_args,
            )
    return assessments_gen

def get_assessments_gen(
        client: HLClient,
        **kwargs,
        ):

    query_args = {k: v for k, v in kwargs.items() if v is not None}
    assessments_gen = paginate(
            client.assessmentConnection,
            SubmissionTypeConnection,
            **query_args,
            )
    return assessments_gen

def create_assessment_with_avro_file(
        client: HLClient,
        workflow_id: int,
        file_id: int,
        avro_file_info: dict
        ):
    class CreateAssessmentPayload(BaseModel):
        errors: List[str]
    result = client.createAssessment(
        return_type=CreateAssessmentPayload,
        projectId=workflow_id,
        imageId=file_id,
        backgroundInfoLayerFileData=avro_file_info,
        status="completed",
    )
    if len(result.errors) > 0:
        raise RuntimeError(f"Error creating assessment: {result.errors}")
