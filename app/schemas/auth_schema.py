from pydantic import BaseModel, Field

class UserLoginSchema(BaseModel):
    username: str = Field(..., example="testuser", description="Login username")
    password: str = Field(..., example="password123", description="Login password")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "testuser",
                "password": "strongpassword"
            }
        }

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenDataSchema(BaseModel):
    username: str = None
    role: str = None