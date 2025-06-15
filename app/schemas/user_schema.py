from pydantic import BaseModel, Field, EmailStr # EmailStr nếu username là email
from typing import Optional

class UserCreateSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=100, example="newmember01")
    full_name: str = Field(..., min_length=1, max_length=255, example="New Member Name")
    password: str = Field(..., min_length=6, example="SecureP@ssw0rd1")
    phone_number: Optional[str] = Field(None, max_length=20, example="0912345678")
    # role sẽ được set mặc định là "member" bởi service

    class Config:
        json_schema_extra = {
            "example": {
                "username": "newmember01",
                "full_name": "New Member Full Name",
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
                        "user_id": 1,
                        "username": "member01",
                        "full_name": "Member Full Name",
                        "phone_number": "0123456789",
                        "role": "member",
                        "created_at": "2023-10-27T10:00:00Z",
                        "updated_at": "2023-10-27T10:00:00Z"
                    },
                    {
                        "user_id": 2,
                        "username": "admin01",
                        "full_name": "Admin Full Name",
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