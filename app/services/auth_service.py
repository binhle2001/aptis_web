import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import timedelta
from helpers.common import get_env_var
from fastapi import HTTPException, status
import time
from schemas.auth_schema import UserLoginSchema
from core.security import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_password_hash # Import để có thể tạo user mẫu
)



DB_NAME = get_env_var("DB", "POSTGRES_DB")
DB_USER = get_env_var("DB", "POSTGRES_USER")
DB_PASSWORD = get_env_var("DB", "POSTGRES_PASSWORD")
DB_HOST = get_env_var("DB", "DB_HOST")
DB_PORT = get_env_var("DB", "DB_PORT")


def get_db_connection():
    for i in range(10):
        try:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                cursor_factory=RealDictCursor # Trả về kết quả dạng dictionary
            )
            return conn
        except psycopg2.OperationalError as e:
            print(f"Database connection error: {e}")
            # Trong một ứng dụng thực tế, bạn có thể muốn log lỗi này
            # và có cơ chế retry hoặc báo lỗi nghiêm trọng hơn.
            time.sleep(2)
    raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service is unavailable."
            )


async def login_for_access_token(form_data: UserLoginSchema):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # 1. Lấy thông tin user
            cur.execute("""
                SELECT id, username, password_hash, role, fullname, is_active, deviceid1, deviceid2, is_commited
                FROM users
                WHERE LOWER(username) = LOWER(%s);
            """, (form_data.username,))
            user_in_db = cur.fetchone()
        
        # In a real app, ensure user_in_db['is_active'] is checked if you have such a field
        # if not user_in_db.get('is_active', True): # Giả sử is_active mặc định là True nếu không có
        #     raise HTTPException(status_code=400, detail="Inactive user")
            if not user_in_db:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if not user_in_db["is_active"]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User inactive",
                    headers={"is_active": "false"},
                )

            # 2. Xác thực mật khẩu
            if not verify_password(form_data.password, user_in_db["password_hash"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # 3. Kiểm tra giới hạn thiết bị, bỏ qua với admin và Phuc32
            username_lower = user_in_db["username"].lower()
            if username_lower not in ("admin", "phuc32"):
                device_id = form_data.device_id
                dev1 = user_in_db["deviceid1"]
                dev2 = user_in_db["deviceid2"]
                
                if dev1 and dev1 == device_id:
                    # đã match deviceid1 → pass
                    pass
                elif dev2 and dev2 == device_id:
                    # đã match deviceid2 → pass
                    pass
                else:
                    # chưa match cả hai
                    if not dev1:
                        # thêm vào deviceid1
                        cur.execute(
                            "UPDATE users SET deviceid1 = %s WHERE id = %s;",
                            (device_id, user_in_db["id"])
                        )
                        conn.commit()
                    elif not dev2:
                        # thêm vào deviceid2
                        cur.execute(
                            "UPDATE users SET deviceid2 = %s WHERE id = %s;",
                            (device_id, user_in_db["id"])
                        )
                        conn.commit()
                    else:
                        # cả hai cột đều đã có giá trị khác device_id → reject
                        raise HTTPException(
                            status_code=status.HTTP_403_FORBIDDEN,
                            detail="Device limit reached. Please use a registered device.",
                        )

        # 4. Tạo token và trả về
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_data = {
            "sub": user_in_db["username"],
            "id": user_in_db["id"],
            'is_active': user_in_db["is_active"],
            'is_commited': user_in_db["is_commited"],
            "role": user_in_db["role"],
            "fullname": user_in_db["fullname"],
        }
        access_token = create_access_token(
            data=access_token_data, expires_delta=access_token_expires
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_role": user_in_db["role"],
        }

    except HTTPException:
        raise  # Để FastAPI xử lý tiếp
    except Exception as e:
        print(f"Unexpected login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred during login."
        )
    finally:
        if conn:
            conn.close()
            
            
            
# --- Hàm tiện ích để tạo user mẫu (chạy một lần hoặc khi cần) ---
async def create_sample_user(username, password, fullname, role="member"):
    """
    Tạo một user mẫu với password đã hash.
    Lưu ý: Chỉ chạy hàm này một lần để tạo user, hoặc khi cần.
    Không nên gọi trong luồng request thông thường trừ khi đó là API đăng ký.
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Kiểm tra xem user đã tồn tại chưa
            cur.execute("SELECT username FROM Users WHERE LOWER(username) = LOWER(%s)", (username,))
            if cur.fetchone():
                print(f"User '{username}' already exists.")
                return

            hashed_password = get_password_hash(password)
            cur.execute(
                """
                INSERT INTO Users (username, password_hash, fullname, role)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (username, hashed_password, fullname, role)
            )
            user_id = cur.fetchone()['id']
            conn.commit()
            print(f"User '{username}' created successfully with ID: {user_id} and role: {role}.")
            return {"id": user_id, "username": username, "role": role}
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error creating sample user '{username}': {e}")
    finally:
        if conn:
            conn.close()

# Ví dụ cách sử dụng hàm tạo user (chạy từ một script riêng hoặc Python shell)
# if __name__ == "__main__":
#     import asyncio
    # asyncio.run(create_sample_user("admin", "adminpass", "Administrator", "admin"))
    # asyncio.run(create_sample_user("member", "memberpass", "Normal Member", "member"))