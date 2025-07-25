from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# -----------------------------
# Schema để tạo mới exam set
# -----------------------------
class ExamSetCreateSchema(BaseModel):
    set_code: str = Field(..., example="APTIS_GENERAL_001")
    title: str = Field(..., example="Bộ đề thi Aptis tổng quát số 1")
    description: Optional[str] = Field(None, example="Mô tả ngắn về bộ đề thi")


# -----------------------------
# Schema tóm tắt thông tin một bài thi
# -----------------------------
class ExamBriefSchema(BaseModel):
    id: int
    exam_code: str
    exam_type: str  # e.g. "READING", "LISTENING"
    description: Optional[str]
    time_limit: int


# -----------------------------
# Schema trả về chi tiết một exam set
# -----------------------------
class ExamSetResponseSchema(BaseModel):
    id: int
    set_code: str
    title: str
    description: Optional[str]
    created_by_user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    is_locked: bool
    exams: List[ExamBriefSchema] = []
    

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "set_code": "APTIS_GENERAL_001",
                "title": "Bộ đề thi Aptis tổng quát số 1",
                "description": "Mô tả ngắn về bộ đề",
                "created_by_user_id": 1,
                "is_active": True,
                "created_at": "2025-06-15T09:00:00",
                "updated_at": "2025-06-15T09:00:00",
                "is_locked": True, 
                "exams": [
                    {
                        "id": 10,
                        "exam_code": "RD001",
                        "exam_type": "READING",
                        "description": "Đề kiểm tra kỹ năng đọc",
                        "time_limit": 40
                    }
                ]
            }
        }


# -----------------------------
# Schema trả về danh sách exam sets (có phân trang)
# -----------------------------
class ExamSetListResponseSchema(BaseModel):
    items: List[ExamSetResponseSchema]
    total: int
    total_pages: int
