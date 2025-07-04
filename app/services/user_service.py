import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException, status


from schemas.user_schema import UserCreateSchema, UserResponseSchema, UserUpdatePasswordSchema
from core.security import get_password_hash
from services.auth_service import get_db_connection # Tái sử dụng
from typing import List, Dict, Any, Optional


async def create_new_user(user_data: UserCreateSchema) -> dict: # Trả về dict thay vì UserResponseSchema
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # 1. Kiểm tra username đã tồn tại chưa
            cur.execute("SELECT id FROM Users WHERE LOWER(username) = LOWER(%s)", (user_data.username,))
            if cur.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Username '{user_data.username}' already registered."
                )

            # 2. Hash password
            hashed_password = get_password_hash(user_data.password)

            # 3. Lưu thông tin tài khoản mới với role "member"
            cur.execute(
                """
                INSERT INTO Users (username, password_hash, fullname, phone_number, role)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, username, fullname, phone_number, role, created_at, updated_at, is_active;
                """,
                (
                    user_data.username,
                    hashed_password,
                    user_data.fullname,
                    user_data.phone_number,
                    "member"  # Role được cố định là 'member'
                )
            )
            created_user_data = cur.fetchone()
            conn.commit()

            if not created_user_data:
                # Trường hợp hiếm gặp, nhưng nên xử lý
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user after insert."
                )
            
            # Chuyển đổi datetime sang string nếu cần thiết cho response
            created_user_data['created_at'] = created_user_data['created_at'].isoformat()
            created_user_data['updated_at'] = created_user_data['updated_at'].isoformat()
            
            return created_user_data # Trả về dict

    except HTTPException:
        if conn:
            conn.rollback() # Rollback nếu là lỗi do logic nghiệp vụ (vd: username tồn tại)
        raise
    except psycopg2.Error as db_error: # Bắt lỗi cụ thể của psycopg2
        if conn:
            conn.rollback()
        print(f"Database error during user creation: {db_error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while creating the user."
        )
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Unexpected error during user creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
    finally:
        if conn:
            conn.close()

async def update_user_password_by_admin(user_id_to_update: int, password_data: UserUpdatePasswordSchema) -> bool:
    """
    Admin updates a user's password.
    Only 'member' roles can have their password updated by admin via this function for safety.
    Admin should update their own password via a different mechanism if needed.
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # 1. Kiểm tra xem user có tồn tại và có phải là 'member' không
            cur.execute("SELECT id, username, role FROM Users WHERE id = %s", (user_id_to_update,))
            user_to_update = cur.fetchone()

            if not user_to_update:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {user_id_to_update} not found."
                )

            # Theo yêu cầu, Admin chỉ sửa password của Member.
            # Bạn có thể bỏ qua kiểm tra này nếu Admin được phép sửa password của Admin khác.
            if user_to_update["role"] != "member":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Cannot update password for user '{user_to_update['username']}' with role '{user_to_update['role']}'. Admins can only update member passwords via this endpoint."
                )

            # 2. Hash password mới
            new_hashed_password = get_password_hash(password_data.new_password)

            # 3. Cập nhật password trong DB
            cur.execute(
                """
                UPDATE Users
                SET password_hash = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
                """,
                (new_hashed_password, user_id_to_update)
            )
            
            # Kiểm tra xem có hàng nào được cập nhật không
            if cur.rowcount == 0:
                # Điều này không nên xảy ra nếu user_to_update được tìm thấy ở trên,
                # nhưng là một biện pháp phòng ngừa.
                conn.rollback()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, # Hoặc 500 nếu là lỗi logic
                    detail=f"User with ID {user_id_to_update} not found during update, or no changes made."
                )

            conn.commit()
            return True

    except HTTPException:
        if conn:
            conn.rollback()
        raise
    except psycopg2.Error as db_error:
        if conn:
            conn.rollback()
        print(f"Database error during password update: {db_error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while updating the password."
        )
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Unexpected error during password update: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
    finally:
        if conn:
            conn.close()

async def deactivate_user_by_admin(user_id_to_deactivate: int, admin_username: str) -> bool:
    """
    Admin deactivates a member's account by setting is_active to False.
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # 1. Kiểm tra xem user có tồn tại không
            cur.execute("SELECT id, username, role, is_active FROM Users WHERE id = %s", (user_id_to_deactivate,))
            user_to_deactivate = cur.fetchone()

            if not user_to_deactivate:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {user_id_to_deactivate} not found."
                )

            # 2. Không cho Admin tự vô hiệu hóa chính mình qua API này (an toàn hơn)
            if user_to_deactivate["username"] == admin_username:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admins cannot deactivate their own account via this endpoint."
                )
            
            # 3. Chỉ cho phép vô hiệu hóa 'member'. Có thể mở rộng cho các role khác nếu cần.
            #    Hoặc không cho phép vô hiệu hóa Admin khác nếu bạn muốn.
            if user_to_deactivate["role"] != "member":
                 raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Cannot deactivate user '{user_to_deactivate['username']}' with role '{user_to_deactivate['role']}'. Only member accounts can be deactivated."
                )

            if not user_to_deactivate["is_active"]:
                # User đã bị vô hiệu hóa rồi
                # Bạn có thể chọn trả về lỗi hoặc thông báo thành công (idempotent)
                # Ở đây, coi như là thành công nếu đã bị vô hiệu hóa
                # raise HTTPException(
                #     status_code=status.HTTP_400_BAD_REQUEST,
                #     detail=f"User with ID {user_id_to_deactivate} is already inactive."
                # )
                print(f"User ID {user_id_to_deactivate} is already inactive. No action taken.")
                return True # Coi như thành công


            # 4. Cập nhật trường is_active thành False
            cur.execute(
                """
                UPDATE Users
                SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
                """,
                (user_id_to_deactivate,)
            )
            
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, # Hoặc 500
                    detail=f"User with ID {user_id_to_deactivate} not found during deactivation, or no changes made."
                )

            conn.commit()
            print(f"User ID {user_id_to_deactivate} deactivated by admin {admin_username}.")
            return True

    except HTTPException:
        if conn:
            conn.rollback()
        raise
    except psycopg2.Error as db_error:
        if conn:
            conn.rollback()
        print(f"Database error during user deactivation: {db_error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while deactivating the user."
        )
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Unexpected error during user deactivation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
    finally:
        if conn:
            conn.close()

# ... (imports và các hàm đã có) ...

async def reactivate_user_by_admin(user_id_to_reactivate: int, admin_username: str) -> bool:
    """
    Admin reactivates a member's account by setting is_active to True.
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # 1. Kiểm tra xem user có tồn tại không
            cur.execute("SELECT id, username, role, is_active FROM Users WHERE id = %s", (user_id_to_reactivate,))
            user_to_reactivate = cur.fetchone()

            if not user_to_reactivate:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {user_id_to_reactivate} not found."
                )

            # 2. Bạn có thể thêm các kiểm tra logic nghiệp vụ khác ở đây nếu cần
            # Ví dụ: chỉ cho phép kích hoạt lại 'member'
            if user_to_reactivate["role"] != "member":
                 raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Cannot reactivate user '{user_to_reactivate['username']}' with role '{user_to_reactivate['role']}'. Only member accounts can be reactivated."
                )

            if user_to_reactivate["is_active"]:
                # User đã active rồi
                print(f"User ID {user_id_to_reactivate} is already active. No action taken.")
                return True # Coi như thành công

            # 3. Cập nhật trường is_active thành TRUE
            cur.execute(
                """
                UPDATE Users
                SET is_active = TRUE, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
                """,
                (user_id_to_reactivate,)
            )
            
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, # Hoặc 500
                    detail=f"User with ID {user_id_to_reactivate} not found during reactivation, or no changes made."
                )

            conn.commit()
            print(f"User ID {user_id_to_reactivate} reactivated by admin {admin_username}.")
            return True

    except HTTPException:
        if conn:
            conn.rollback()
        raise
    except psycopg2.Error as db_error:
        if conn:
            conn.rollback()
        print(f"Database error during user reactivation: {db_error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while reactivating the user."
        )
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Unexpected error during user reactivation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
    finally:
        if conn:
            conn.close()

async def get_users_list(
    role: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 0,
    limit: int = 100 # Giới hạn mặc định để tránh trả về quá nhiều dữ liệu
) -> Dict[str, Any]: # Trả về dict để UserListResponseSchema có thể parse
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            base_query = "FROM Users u WHERE 1=1"
            count_query_str = "SELECT COUNT(u.id) " + base_query
            data_query_str = "SELECT u.id, u.username, u.fullname, u.phone_number, u.role, u.is_active, u.created_at, u.updated_at " + base_query

            conditions = []
            params = {} # Sử dụng dict cho named placeholders nếu psycopg2 hỗ trợ, hoặc list cho %s

            if role:
                conditions.append("u.role = %(role)s") # Hoặc u.role = %s
                params['role'] = role
            
            if search:
                # Tìm kiếm không phân biệt chữ hoa chữ thường
                conditions.append("(u.username ILIKE %(search)s OR u.fullname ILIKE %(search)s)")
                params['search'] = f"%{search}%"

            if conditions:
                data_query_str += " AND " + " AND ".join(conditions)
                count_query_str += " AND " + " AND ".join(conditions)
            
            # Thực hiện count query
            # Nếu dùng %s placeholders:
            # param_list_for_count = [val for key, val in params.items()] # Cẩn thận thứ tự
            # cur.execute(count_query_str.replace("%(search)s", "%s").replace("%(role)s", "%s"), param_list_for_count)
            # Dùng named placeholders (nếu psycopg2 hỗ trợ trực tiếp hoặc qua adapter)
            # Hiện tại, psycopg2 không hỗ trợ named placeholders trực tiếp trong execute,
            # nên chúng ta sẽ dùng %s và truyền tuple/list.
            
            param_values = []
            final_data_query = data_query_str
            final_count_query = count_query_str

            # Xây dựng lại query và params cho %s
            # Đây là cách đơn giản, nếu query phức tạp hơn cần cẩn thận
            if role:
                final_data_query = final_data_query.replace("%(role)s", "%s")
                final_count_query = final_count_query.replace("%(role)s", "%s")
                param_values.append(role)
            if search:
                search_term = f"%{search}%"
                final_data_query = final_data_query.replace("%(search)s", "%s") # username
                final_data_query = final_data_query.replace("%(search)s", "%s") # fullname (nếu vẫn còn)
                final_count_query = final_count_query.replace("%(search)s", "%s") # username
                final_count_query = final_count_query.replace("%(search)s", "%s") # fullname

                # Điều chỉnh logic này nếu bạn có nhiều placeholder %(search)s
                # Cách an toàn hơn là xây dựng chuỗi query với %s ngay từ đầu
                # và chỉ thêm giá trị vào param_values theo đúng thứ tự.
                # Ví dụ đơn giản hóa:
                # Giả sử luôn có search nếu nó được truyền vào:
                if 'search' in params: # chỉ thêm một lần cho mỗi
                    param_values.append(params['search'])
                    if final_data_query.count("%s") > len(param_values): # Nếu có 2 placeholder cho search
                         param_values.append(params['search'])


            # Tạm thời đơn giản hóa cho %s placeholders (cần cải thiện nếu có nhiều điều kiện phức tạp)
            # Cách an toàn hơn:
            query_conditions = []
            query_params_list = []
            if role:
                query_conditions.append("u.role = %s")
                query_params_list.append(role)
            if search:
                query_conditions.append("(u.username ILIKE %s OR u.fullname ILIKE %s)")
                search_like = f"%{search}%"
                query_params_list.append(search_like)
                query_params_list.append(search_like)

            where_clause = ""
            if query_conditions:
                where_clause = " AND " + " AND ".join(query_conditions)
            
            final_count_query_str = "SELECT COUNT(u.id) FROM Users u WHERE 1=1" + where_clause
            cur.execute(final_count_query_str, tuple(query_params_list))
            total_count = cur.fetchone()['count']


            # Thêm ORDER BY, LIMIT, OFFSET cho data query
            final_data_query_str = ("SELECT u.id, u.username, u.fullname, u.phone_number, u.role, u.is_active, "
                                 "u.created_at, u.updated_at FROM Users u WHERE 1=1" + where_clause +
                                 " ORDER BY u.id ASC LIMIT %s OFFSET %s") # Hoặc DESC
            
            data_params_list = query_params_list.copy()
            data_params_list.append(limit)
            data_params_list.append((page-1) * limit)
            
            cur.execute(final_data_query_str, tuple(data_params_list))
            users_data = cur.fetchall()

            # Chuyển đổi datetime sang string
            items = []
            for user_row in users_data:
                user_dict = dict(user_row) # Đảm bảo là dict
                user_dict['created_at'] = user_dict['created_at'].isoformat()
                user_dict['updated_at'] = user_dict['updated_at'].isoformat()
                items.append(user_dict)

            return {
                "items": items,
                "total": total_count,
                "limit": limit,
                "page": page
            }

    except psycopg2.Error as db_error:
        print(f"Database error while fetching users list: {db_error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while fetching users."
        )
    except Exception as e:
        print(f"Unexpected error while fetching users list: {e}")
        # import traceback
        # traceback.print_exc() # In traceback đầy đủ để debug
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
    finally:
        if conn:
            conn.close()
            
async def delete_user_by_admin(user_id: int, admin_username: str) -> bool:
    """
    Admin deletes a member's account by setting is_active to True.
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # 1. Kiểm tra xem user có tồn tại không
            cur.execute("SELECT id, username, role, is_active FROM Users WHERE id = %s", (user_id,))
            user_to_delete = cur.fetchone()

            if not user_to_delete:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {user_id} not found."
                )

            # 2. Bạn có thể thêm các kiểm tra logic nghiệp vụ khác ở đây nếu cần
            # Ví dụ: chỉ cho phép kích hoạt lại 'member'
            if user_to_delete["role"] != "member":
                 raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Cannot delete user '{user_to_delete['username']}' with role '{user_to_delete['role']}'. Only member accounts can be deleted."
                )
            user_id_to_delete = user_to_delete["id"]

          
            cur.execute(
                """
                DELETE FROM Users WHERE id = %s;
                """,
                (user_id_to_delete,)
            )
            cur.execute(
                """
                DELETE FROM exam_submission WHERE user_id = %s;
                """,
                (user_id_to_delete,)
            )
            
            
            if cur.rowcount == 0:
                conn.rollback()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, # Hoặc 500
                    detail=f"User with ID {user_id_to_delete} not found during reactivation, or no changes made."
                )

            conn.commit()
            print(f"User ID {user_id_to_delete} is deleted by admin {admin_username}.")
            return True

    except HTTPException:
        if conn:
            conn.rollback()
        raise
    except psycopg2.Error as db_error:
        if conn:
            conn.rollback()
        print(f"Database error during user reactivation: {db_error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while reactivating the user."
        )
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Unexpected error during user reactivation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        )
    finally:
        if conn:
            conn.close()
            

    
