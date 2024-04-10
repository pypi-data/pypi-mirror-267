from typing import Any, Optional, Sequence, Tuple, Union, Dict, Optional, List
from datetime import datetime
import numpy as np
from uuid import UUID, uuid4
from shapely import affinity, make_valid
from shapely import geometry as geom
from shapely.wkt import loads as wkt_loads
from shapely.ops import unary_union
from pydantic import BaseModel, Field, confloat, validator, Extra
from highlighter.labeled_uuid import LabeledUUID
from highlighter.const import (
        OBJECT_CLASS_ATTRIBUTE_UUID,
        PIXEL_LOCATION_ATTRIBUTE_UUID,
        EMBEDDING_ATTRIBUTE_UUID,
        DATA_FILE_ATTRIBUTE_UUID,
        )

__all__ = [
        "AttributeRecord",
        "ImageRecord",
        "S3Files",
        ]

DEFAULT_SPLIT_NAME = "data"
DEFAULT_DATA_FILES_KEY = "images"  # TODO: Update to 'files'
DEFAULT_ANNOS_KEY = "annotations"  # TODO: Update to 'attributes'
CLOUD_FILES_INFO_KEY = "cloud_files_info"

class ImageRecord(BaseModel):
    data_file_id: Union[int, str]
    width: Optional[int]=None
    height: Optional[int]=None
    filename: str
    split: Optional[str]=DEFAULT_SPLIT_NAME
    extra_fields: Optional[Dict]=None
    assessment_id: Optional[int]=None
    hash_signature: Optional[str]=None

# Extra fields are ignored and will be dropped when instantiating
# a the Object. This is done so things don't break if we load
# some older S3Files where 'type' is a field. If you plan on changing
# this you should consider what to do in this situation
class S3Files(BaseModel, extra=Extra.ignore):
    """Information needed to donwload files/records from s3

    s3://my-bucket/datasets/123/  <-- bucket_name = my-bucket
        records_abc123.json       <-- records_prefix = datasets/123/records_abc123.json
        files_def456.tar.gz       <-- files_prefix = [datasets/123/files_def456.tar.gz,]
    """
    bucket_name: str
    prefix: str
    files: List[str]
    records: List[str]=[]
    other: Dict[str, List[str]]=[]

class AttributeValue(BaseModel):
    attribute_id: LabeledUUID
    value: Any
    confidence: confloat(ge=0.0, le=1.0) = 1.0

    def attribute_label(self):
        if isinstance(self.attribute_id, LabeledUUID):
            return self.attribute_id.label
        else:
            return str(self.attribute_id)[:8]

    def serialize_value(self):
        return self.value
        

class ObjectClassAttributeValue(AttributeValue):
    attribute_id: Union[LabeledUUID, UUID] = Field(default_factory=lambda: OBJECT_CLASS_ATTRIBUTE_UUID)
    value: UUID

    def serialize_value(self):
        return str(self.value)


class PixelLocationAttributeValue(AttributeValue):

    class Config():
        arbitrary_types_allowed = True

    attribute_id: Union[LabeledUUID, UUID] = Field(default_factory=lambda: PIXEL_LOCATION_ATTRIBUTE_UUID)

    value: Union[geom.Polygon, geom.MultiPolygon, geom.LineString, geom.Point]

    def serialize_value(self):
        return self.value.wkt

    @validator("value")
    def validate_geometry(cls, v):
        assert v.is_valid, f"Invalid Geometry: {v}"
        return v

    @classmethod
    def from_wkt(cls,
                 wkt_str: str,
                 attribute_id: Union[LabeledUUID, UUID] = PIXEL_LOCATION_ATTRIBUTE_UUID,
                 confidence: float = 1.0,
                 ):
        return cls(attribute_id=attribute_id, value=wkt_loads(wkt_str), confidence=confidence)

    @classmethod
    def from_point_coords(cls,
                          coords: Sequence[Union[Tuple[float, float], Tuple[float, float, float], np.ndarray]],
                          attribute_id: Union[LabeledUUID, UUID] = PIXEL_LOCATION_ATTRIBUTE_UUID,
                          confidence: float = 1.0,
                          ):
        """Create a LocationAttributeValue for a polygon

        Args:
            coords: A sequence or array-like of with 2 or 3 values.
        """
        value = geom.Point(coords)
        return cls(attribute_id=attribute_id, value=value, confidence=confidence)

    @classmethod
    def from_line_coords(cls,
                         coords: Sequence[Union[Tuple[float, float], Tuple[float, float, float], np.ndarray, Sequence[geom.Point]]],
                         attribute_id: Union[LabeledUUID, UUID] = PIXEL_LOCATION_ATTRIBUTE_UUID,
                         confidence: float = 1.0,
                         ):
        """Create a LocationAttributeValue for a polygon

        Args:
            coords: A sequence of (x, y [,z]) numeric coordinate pairs or triples, or
            an array-like with shape (N, 2) or (N, 3).
            Also can be a sequence of Point objects.
        """
        value = geom.LineString(coords)
        return cls(attribute_id=attribute_id, value=value, confidence=confidence)
    
    
    @classmethod
    def from_left_top_width_height_coords(cls,
                            coords: Union[Tuple[float, float, float, float], np.ndarray],
                            attribute_id: Union[LabeledUUID, UUID] = PIXEL_LOCATION_ATTRIBUTE_UUID,
                                          confidence: float = 1.0,
                            ):
        """Create a LocationAttributeValue for a box in the form [x,y,w,h]

        Args:
            coords: A sequence of box in the form [x,y,w,h]
        """
        x0, y0, w, h = coords
        x1 = x0 + w
        y1 = y0 + h
        _coords = [[x0, y0],[x1, y0],[x1, y1],[x0, y1],[x0, y0]]
        value = geom.Polygon(_coords)
        return cls(attribute_id=attribute_id, value=value, confidence=confidence)

    @classmethod
    def from_polygon_coords(cls,
                            coords: Sequence[Union[Tuple[float, float], Tuple[float, float, float], np.ndarray, Sequence[geom.Point]]],
                            attribute_id: Union[LabeledUUID, UUID] = PIXEL_LOCATION_ATTRIBUTE_UUID,
                            confidence: float = 1.0,
                            fix_invalid_polygons: bool=False,
                            ):
        """Create a LocationAttributeValue for a polygon

        Args:
            coords: A sequence of (x, y [,z]) numeric coordinate pairs or triples, or
            an array-like with shape (N, 2) or (N, 3).
            Also can be a sequence of Point objects.
        """
        value = geom.Polygon(coords)
        if fix_invalid_polygons:
            value = make_valid(value)
        return cls(attribute_id=attribute_id, value=value, confidence=confidence)

    @classmethod
    def from_multpolygon_coords(cls,
                                coords: Sequence[Sequence[Tuple[float, float]]],
                                attribute_id: Union[LabeledUUID, UUID] = PIXEL_LOCATION_ATTRIBUTE_UUID,
                                confidence: float = 1.0,
                                fix_invalid_polygons: bool=False,
                                ):
        """Create a LocationAttributeValue for a polygon

        Args:
            coords: A nested sequence of (x, y) numeric coordinate pairs, or
            an array-like with shape (N, 2).
        """
        shapes = []
        for poly_xys in coords:
            shape = geom.Polygon(poly_xys)
            if fix_invalid_polygons:
                shape = make_valid(shape)
            shapes.append(shape)

        if len(shapes) == 1:
            value = shapes[0]
        else:
            value = unary_union(shapes)

        return cls(attribute_id=attribute_id, value=value, confidence=confidence)
    
    def get_top_left_bottom_right_coordinates(self, scale: float=1.0,
                                              scale_about_origin: bool=True,
                                              pad: int=0) -> Tuple[int, int, int, int]:
        """
        to top left bottom right format

        for embedding
        """
        bounds: geom.Polygon = geom.box(*self.value.bounds)

        if scale_about_origin:
            bounds = affinity.scale(bounds, xfact=scale, yfact=scale, origin=(0, 0, 0))
        else:
            bounds = affinity.scale(bounds, xfact=scale, yfact=scale, origin="center")

        bounds = bounds.buffer(pad, join_style="bevel")
        return bounds.bounds


class EmbeddingAttributeValue(AttributeValue):
    class Config:
        arbitrary_types_allowed = True
        
    attribute_id: Union[LabeledUUID, UUID] = Field(default_factory=lambda: EMBEDDING_ATTRIBUTE_UUID)
    value: Union[Sequence[float], np.ndarray]

    def serialize_value(self):
        return [float(i) for i in self.value]

class DataFileAttributeValue(AttributeValue):
    class Config:
        arbitrary_types_allowed = True
        
    attribute_id: Union[LabeledUUID, UUID] = Field(default_factory=lambda: DATA_FILE_ATTRIBUTE_UUID)
    value: np.ndarray

    def serialize_value(self):
        raise NotImplementedError()

class EnumAttributeValue(AttributeValue):
    attribute_id: Union[LabeledUUID, UUID]
    value: Union[UUID, LabeledUUID]


    def serialize_value(self):
        raise str(self.value)

class ScalarAttributeValue(AttributeValue):
    attribute_id: Union[LabeledUUID, UUID]
    value: Union[float, int]

class DatumSource(BaseModel):
    confidence: confloat(ge=0.0, le=1.0) = 1.0
    frameId: Optional[int]
    hostId: Optional[str]
    pipelineElementName: Optional[str]
    pipelineId: Optional[int]
    pipelineElementId: Optional[int]
    trainingRunId: Optional[int]

class AttributeRecord(BaseModel):

    data_file_id: Union[int, str]
    entity_id: UUID = Field(default_factory=uuid4)
    attribute_id: Optional[Union[LabeledUUID, UUID, str]] = None
    attribute_name: str
    value: Any
    confidence: Optional[float] = 1.0
    frame_id: Optional[int] = None

    time: Union[datetime, str] = Field(default_factory=datetime.now)
    host_id: Optional[str] = None
    pipeline_element_name: Optional[str] = None
    pipeline_id: Optional[int] = None
    pipeline_element_id: Optional[int] = None
    training_run_id: Optional[int] = None

    @validator("time")
    def validate_isofrmat(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v)
        else:
            return v            

    @classmethod
    def from_attribute_value(cls, 
                             data_file_id: Union[int, str],
                             attribute_value: AttributeValue,
                             entity_id: Optional[UUID] = None,
                             frame_id: Optional[int] = None,
                             time: Optional[Union[datetime, str]] = None, 
                             host_id: Optional[str] = None,
                             pipeline_id: Optional[int] = None,
                             pipeline_element_id: Optional[int] = None,
                             pipeline_element_name: Optional[str] = None,
                             training_run_id: Optional[int] = None,
                             ):
        attribute_id = attribute_value.attribute_id
        attribute_name = getattr(attribute_value.attribute_id, "label", "")
        confidence = attribute_value.confidence
        value = attribute_value.value
        return cls(data_file_id=data_file_id,
                   entity_id=uuid4() if entity_id is None else entity_id,
                   attribute_id=attribute_id,
                   attribute_name=attribute_name,
                   value=value,
                   confidence=confidence,
                   frame_id=frame_id,
                   time=datetime.now() if time is None else time,
                   host_id=host_id,
                   pipeline_id=pipeline_id,
                   pipeline_element_id=pipeline_element_id,
                   pipeline_element_name=pipeline_element_name,
                   training_run_id=training_run_id,
                   )

    def dict(self, *args, **kwargs):
        _d = super().dict(*args, **kwargs)
        _d["time"] = _d["time"].isoformat()
        return _d

    def to_df_record(self):
        _d = self.dict(exclude_none=True)
        record = {"data_file_id": _d.pop("data_file_id"),
                  "entity_id": str(_d.pop("entity_id")),
                  "attribute_id": str(_d.pop("attribute_id")),
                  "attribute_name": _d.pop("attribute_name"),
                  "value": _d.pop("value"),
                  "confidence": _d.pop("confidence"),
                  }
        record["extra_fields"] = _d
        return record

