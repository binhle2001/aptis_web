from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# Có thể bạn sẽ cần các schema chi tiết hơn cho từng loại câu hỏi sau này
# Ví dụ:
# class QuestionOptionSchema(BaseModel):
#     option_text: str
#     is_correct: bool
#     display_order: int

# class QuestionSchema(BaseModel):
#     question_text: str
#     question_type: str # 'MCQ_SINGLE', 'ORDERING', 'MATCHING', 'FILL_IN_BLANK'
#     points: int = 1
#     options: Optional[List[QuestionOptionSchema]] = None
#     correct_answer_text: Optional[str] = None # For FILL_IN_BLANK
#     correct_order: Optional[List[str]] = None # For ORDERING
#     correct_matches: Optional[Dict[str, str]] = None # For MATCHING (e.g. paragraph_key: heading_id)

# class ExamPartSchema(BaseModel):
#     part_number: int
#     part_title: Optional[str] = None
#     instructions: Optional[str] = None
#     questions: List[QuestionSchema]

class ExamCreateResponseSchema(BaseModel):
    exam_id: int
    exam_code: str
    title: str
    exam_type: str
    time_limit_minutes: Optional[int] = None
    message: str = "Exam created successfully"

    class Config:
        json_schema_extra = {
            "example": {
                "exam_id": 1,
                "exam_code": "RD001",
                "title": "Đề thi Reading số 1",
                "exam_type": "reading",
                "time_limit_minutes": 60,
                "message": "Exam created successfully"
            }
        }

# Schema này không dùng trực tiếp cho request body vì có file upload
# Nhưng các trường Form data sẽ dựa trên đây
class ExamReadingFormParams(BaseModel): # Không dùng trực tiếp, chỉ để tham khảo
    title: str = Field(..., example="Đề thi Reading số 1")
    exam_code: str = Field(..., example="RD001_V2")
    time_limit_minutes: int = Field(..., gt=0, example=60)
    # file: UploadFile sẽ được xử lý riêng