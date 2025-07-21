from pydantic import BaseModel, Field

class UserLoginSchema(BaseModel):
    username: str = Field(..., example="testuser", description="Login username")
    password: str = Field(..., example="password123", description="Login password")
    device_id: str = Field(..., example="device1", description="Device id for login")
    class Config:
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "password": "strongpassword",
                "device_id": "device_id"
            }
        }

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenDataSchema(BaseModel):
    username: str = None
    role: str = None