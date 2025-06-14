from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # Dùng cái này tiện hơn UserLoginSchema cho form data

from app.schemas.auth_schema import TokenSchema, UserLoginSchema
from app.services import auth_service

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login", response_model=TokenSchema)
async def login_for_access_token_endpoint(
    # Sử dụng UserLoginSchema nếu bạn muốn gửi JSON body
    form_data: UserLoginSchema
    # Hoặc sử dụng OAuth2PasswordRequestForm nếu bạn muốn gửi form data (x-www-form-urlencoded)
    # form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Đăng nhập để nhận access token.
    Hệ thống sẽ xác thực username và password.
    """
    # Khi dùng UserLoginSchema (JSON body):
    token_data = await auth_service.login_for_access_token(form_data)

    # Khi dùng OAuth2PasswordRequestForm (form data):
    # user_login_data = UserLoginSchema(username=form_data.username, password=form_data.password)
    # token_data = await auth_service.login_for_access_token(user_login_data)

    if not token_data: # auth_service.login_for_access_token sẽ raise HTTPException, nên dòng này có thể không cần
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password or inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenSchema(access_token=token_data["access_token"], token_type=token_data["token_type"])
    # Hoặc trả về đầy đủ hơn nếu client cần role:
    # return token_data

# Ví dụ thêm endpoint để tạo user mẫu (chỉ dùng cho mục đích dev)
# Bạn nên bảo vệ endpoint này hoặc chỉ chạy từ script
@router.post("/create-dev-user", include_in_schema=False) # include_in_schema=False để ẩn khỏi Swagger UI
async def create_dev_user_endpoint(username: str, password: str, full_name: str, role: str = "member"):
    # CẢNH BÁO: Endpoint này không an toàn cho production. Chỉ dùng để dev.
    # Trong thực tế, bạn sẽ có một quy trình đăng ký user riêng.
    user = await auth_service.create_sample_user(username, password, full_name, role)
    if user:
        return {"message": f"User {username} created/verified.", "user": user}
    return {"message": f"Failed to create user {username}."}