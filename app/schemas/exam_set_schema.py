from pydantic import BaseModel, Field
from typing import Optional, List

class ExamSetCreateSchema(BaseModel):
    set_code: str = Field(..., example="APTIS_GENERAL_001")
    title: str = Field(..., example="Bộ đề thi Aptis tổng quát số 1")
    description: Optional[str] = None
    overall_time_limit_minutes: Optional[int] = Field(None, gt=0, example=120)

class ExamSetResponseSchema(BaseModel):
    exam_set_id: int
    set_code: str
    title: str
    description: Optional[str] = None
    overall_time_limit_minutes: Optional[int] = None
    created_by_user_id: int
    is_active: bool
    created_at: str # Hoặc datetime
    updated_at: str # Hoặc datetime

    class Config:
        json_schema_extra = { # Pydantic V2
            "example": {
                "exam_set_id": 1,
                "set_code": "APTIS_GENERAL_001",
                "title": "Bộ đề thi Aptis tổng quát số 1",
                "overall_time_limit_minutes": 120,
                "created_by_user_id": 1,
                "is_active": True,
                "created_at": "2023-10-27T10:00:00Z",
                "updated_at": "2023-10-27T10:00:00Z"
            }
        }
        # orm_mode = True # Pydantic V1

class ExamSetListResponseSchema(BaseModel):
    items: List[ExamSetResponseSchema]
    total: int
    limit: Optional[int] = None
    skip: Optional[int] = None