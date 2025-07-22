from pydantic import BaseModel, Field, EmailStr # EmailStr nếu username là email
from typing import Optional

class UserCreateSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=100, example="newmember01")
    fullname: str = Field(..., min_length=1, max_length=255, example="New Member Name")
    password: str = Field(..., min_length=6, example="SecureP@ssw0rd1")
    phone_number: Optional[str] = Field(None, max_length=20, example="0912345678")
    # role sẽ được set mặc định là "member" bởi service

    class Config:
        json_schema_extra = {
            "example": {
                "username": "newmember01",
                "fullname": "New Member Full Name",
                "password": "verysecretpassword",
                "phone_number": "0987654321"
            }
        }

class UserResponseSchema(BaseModel):
    id: int
    username: str
    fullname: str
    phone_number: Optional[str] = None
    role: str
    created_at: str # Hoặc datetime, tùy bạn muốn format thế nào
    updated_at: str # Hoặc datetime
    is_active: bool
    class Config:
        # Nếu bạn dùng ORM và muốn trả về model trực tiếp
        # from_attributes = True # Pydantic V2
        # orm_mode = True # Pydantic V1
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "member01",
                "fullname": "Member Full Name",
                "phone_number": "0123456789",
                "role": "member",
                "created_at": "2023-10-27T10:00:00Z",
                "updated_at": "2023-10-27T10:00:00Z",
                "is_active": True
            }
        }

        # ... (Các schema UserCreateSchema, UserResponseSchema đã có) ...
from pydantic import BaseModel, Field

class UserUpdatePasswordSchema(BaseModel):
    new_password: str = Field(..., min_length=6, example="NewS3cureP@ss!")

    class Config:
        json_schema_extra = {
            "example": {
                "new_password": "aVeryStrongNewPassword123"
            }
        }

class MessageResponseSchema(BaseModel): # Schema chung cho các thông báo đơn giản
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation successful."
            }
        }

# ... (Các schema UserCreateSchema, UserResponseSchema, UserUpdatePasswordSchema, MessageResponseSchema đã có) ...
from typing import List, Optional

class UserListResponseSchema(BaseModel):
    items: List[UserResponseSchema]
    total: int # Tổng số lượng bản ghi khớp với query (trước khi phân trang)
    limit: Optional[int] = None
    page: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "username": "member01",
                        "fullname": "Member Full Name",
                        "phone_number": "0123456789",
                        "role": "member",
                        "created_at": "2023-10-27T10:00:00Z",
                        "updated_at": "2023-10-27T10:00:00Z"
                    },
                    {
                        "id": 2,
                        "username": "admin01",
                        "fullname": "Admin Full Name",
                        "phone_number": "0987654321",
                        "role": "admin",
                        "created_at": "2023-10-26T09:00:00Z",
                        "updated_at": "2023-10-26T09:00:00Z"
                    }
                ],
                "total": 25,
                "limit": 10,
                "page": 0
            }
        }
class GuestInsertSchema(BaseModel):
    fullname: str = Field(..., example="Nguyễn Văn A")
    phone_number: str = Field(..., example="0323245245")
    class Config:
        json_schema_extra = {
            "fullname": "Nguyễn Văn A",
            "phone_number": "023817211",
        }
class GuestSchema(BaseModel):
    id: int
    fullname: str = Field(..., example="Nguyễn Văn A")
    phone_number: str = Field(..., example="0323245245")
    is_called: bool
    class Config:
        json_schema_extra = {
            "id": 1,
            "fullname": "Nguyễn Văn A",
            "phone_number": "023817211",
            "is_called": True
        }
class GuestResponseSchema(BaseModel):
    items: List[GuestSchema]
    total: int # Tổng số lượng bản ghi khớp với query (trước khi phân trang)
    total_pages: Optional[int] = None
    class Config:
        json_schema_extra = {
            "example": {
                "items": {},
                "total": 25,
                "total_pages": 0
            }
        }
class ExamSubmissionSchema(BaseModel):
    json_data: dict = Field(..., example="Nguyễn Văn A")
    score: str = None
    class Config:
        json_schema_extra = {
            "example": {
                "json_data": "put json here",
                "score": "19/50"
            }
        }

class SpeakingAudioSchema(BaseModel):
    audio: str = Field(..., example = "base64")
    class Config:
        json_schema_extra = {
            "example": {
                "audio": "base64",
            }
        }


class CommitmentSchema(BaseModel):
    student_name: str = Field(..., example="Nguyễn Văn An")
    date_of_birth: str = Field(..., example="01/01/2000")
    national_id: str = Field(..., example="012345678910")
    issue_date: str = Field(..., example="15/06/2020")
    address: str = Field(..., example="Số 1, Đường ABC, Phường XYZ, Quận 1, TP. HCM")
    phone: str = Field(..., example="0987654321")
    email: str = Field(..., example="an.nguyen@email.com")
    start_date: str = Field(..., example="01/08/2025")
    end_date: str = Field(..., example="01/11/2025")
    target_output: str = Field(..., example="B1 Tương đương 4.0 IELTS")
    course_registered: str = Field(..., example="Luyện thi Aptis cấp tốc")
    fee_paid: str = Field(..., example="5,000,000")
    fee_deadline: str = Field(..., example="01/08/2025")
    commitment_output: str = Field(..., example="Đạt chứng chỉ Aptis B1")
    signature_base64: str = Field(..., description="Ảnh chữ ký dưới dạng chuỗi Base64 (có thể có hoặc không có tiền tố data URI)", example="data:image/png;base64,iVBORw0KGgoAAAANSUhEUg...")

    class Config:
        json_schema_extra = {
            "example": {
                "student_name": "Trần Thị B",
                "date_of_birth": "15/05/1999",
                "national_id": "098765432109",
                "issue_date": "10/10/2021",
                "address": "123 Đường Cầu Giấy, Dịch Vọng, Cầu Giấy, Hà Nội",
                "phone": "0123456789",
                "email": "b.tran@gmail.com",
                "start_date": "20/07/2025",
                "end_date": "20/09/2025",
                "target_output": "Aptis B2",
                "course_registered": "Aptis Nâng cao",
                "fee_paid": "4,500,000 VNĐ",
                "fee_deadline": "20/07/2025",
                "commitment_output": "Đảm bảo đầu ra Aptis B2",
                "signature_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPoAAABkCAYAAACfIFoNAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAEYSURBVHhe7cExAQAAAMKg9U9tB2+g408gAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP4NIgAAAZS7q3kAAAAASUVORK5CYII="
            }
        }
