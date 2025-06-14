from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.services.auth_service import get_db_connection
from app.core.security import decode_access_token, TokenData

security = HTTPBearer()

async def get_current_user_from_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> TokenData:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload_data = decode_access_token(token)
        if payload_data is None or payload_data.sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return payload_data

async def get_current_active_user(
    current_user_token_payload: Annotated[TokenData, Depends(get_current_user_from_token)]
) -> dict:
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT user_id, username, full_name, role, phone_number, is_active, created_at, updated_at " # Thêm is_active
                "FROM Users WHERE username = %s", (current_user_token_payload.sub,)
            )
            user_in_db = cur.fetchone()
        if not user_in_db:
            raise HTTPException(status_code=404, detail="User not found")
        
        # <<< KIỂM TRA is_active Ở ĐÂY >>>
        if not user_in_db.get('is_active', False): # Mặc định là False nếu không có trường (an toàn)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, # Hoặc 403 Forbidden
                detail="Inactive user. Account has been deactivated."
            )
        return user_in_db
    finally:
        if conn:
            conn.close()


# Dependency để kiểm tra role Admin
async def get_current_admin_user(
    current_user: Annotated[dict, Depends(get_current_active_user)]
) -> dict:
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted: Requires admin privileges"
        )
    return current_user