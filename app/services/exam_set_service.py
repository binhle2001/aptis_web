# Tương tự như user_service, nhưng cho ExamSets
# Các hàm: create_exam_set, get_exam_set_by_id, get_exam_set_by_code, get_exam_sets_list, update_exam_set, ...
# Ví dụ hàm create:
import psycopg2
from fastapi import HTTPException, status
from app.schemas.exam_set_schema import ExamSetCreateSchema
from app.schemas.user_schema import MessageResponseSchema
from app.services.auth_service import get_db_connection
from typing import Optional, Dict, Any, List

from app.services.exam_service import delete_exam_data
async def create_exam_set(set_data: ExamSetCreateSchema, created_by_user_id: int) -> dict:
    
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM exam_sets WHERE set_code = %s",
                (set_data.set_code,)
            )
            if cur.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"ExamSet with code '{set_data.set_code}' already exists."
                )
            print(set_data.set_code, set_data.title, set_data.description, created_by_user_id)
            cur.execute(
                """
                INSERT INTO exam_sets (set_code, title, description, created_by_user_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id, set_code, title, description, created_by_user_id, is_active, created_at, updated_at;
                """,
                (set_data.set_code, set_data.title, set_data.description,  created_by_user_id)
            )
            
            created_set = cur.fetchone()
            conn.commit()
            if not created_set:
                raise HTTPException(status_code=500, detail="Failed to create exam set.")
            
            created_set['created_at'] = created_set['created_at'].isoformat()
            created_set['updated_at'] = created_set['updated_at'].isoformat()
            return dict(created_set)
    except HTTPException:
        if conn: conn.rollback()
        raise
    except psycopg2.Error as db_err:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {db_err}")
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        if conn: conn.close()
        
import math


async def get_exam_set(
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 100,
) -> Dict[str, Any]:
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            # 1) Build WHERE clause
            where_clauses: List[str] = []
            params: List[Any] = []
            if search:
                where_clauses.append("(set_code ILIKE %s OR title ILIKE %s)")
                like_pattern = f"%{search}%"
                params += [like_pattern, like_pattern]
            where_sql = ""
            if where_clauses:
                where_sql = "WHERE " + " AND ".join(where_clauses)

            # 2) Count tổng số bản ghi
            count_sql = f"SELECT COUNT(*) AS total FROM exam_sets {where_sql};"
            cur.execute(count_sql, params)
            total = cur.fetchone()["total"]

            # 3) Tính tổng số page
            total_pages = math.ceil(total / limit) if limit > 0 else 0

            # 4) Truy vấn dữ liệu từng page
            offset = (page-1) * limit
            data_sql = f"""
                SELECT 
                  id, set_code, title, description, created_by_user_id,
                  is_active, created_at, updated_at
                FROM exam_sets
                {where_sql}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s;
            """
            # thêm limit, offset vào params
            
            cur.execute(data_sql, params + [limit, offset])
            rows = cur.fetchall()

            # 5) Chuyển thành list of dict và isoformat cho timestamp
            items = []
            print(rows)
            for r in rows:
                item = dict(r)
                item["created_at"] = item["created_at"].isoformat()
                item["updated_at"] = item["updated_at"].isoformat()
                items.append(item)

            return {
                "items": items,
                "total": total,
                "total_pages": total_pages,
            }

    except psycopg2.Error as db_err:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {db_err}")
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()


async def get_exam_set_by_id(exam_set_id: int) -> dict:
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            # Lấy thông tin exam_set
            cur.execute("""
                SELECT id, set_code, title, description, created_by_user_id, is_active, created_at, updated_at
                FROM exam_sets
                WHERE id = %s and is_active = %s
            """, (exam_set_id, True))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail=f"Exam set with id {exam_set_id} not found.")

            row["created_at"] = row["created_at"].isoformat()
            row["updated_at"] = row["updated_at"].isoformat()

            # Lấy danh sách các bài thi (exams) thuộc exam_set này
            cur.execute("""
                SELECT id, exam_code, exam_type, description, time_limit
                FROM exams
                WHERE examset_id = %s and is_active = %s
            """, (exam_set_id, True))
            exams = cur.fetchall()

            row["exams"] = exams  # thêm vào kết quả
            return dict(row)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()

async def deactivate_exam_set(exam_set_id: int, deleted_by_user_id: int) -> None:
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # 1) Kiểm tra tồn tại & active
            cur.execute(
                "SELECT is_active FROM exam_sets WHERE id = %s",
                (exam_set_id,)
            )
            row = cur.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Exam set not found.")
            
            if not row["is_active"]:
                # đã inactive rồi
                raise HTTPException(status_code=400, detail="Exam set has been inactive")
            
            # 2) Soft‑delete + ghi deleted_by_user_id + cập nhật updated_at
            cur.execute(
                """
                UPDATE exam_sets
                   SET is_active = %s,
                       deleted_by_user_id = %s,
                       updated_at = now()
                 WHERE id = %s
                """,
                (False, deleted_by_user_id, exam_set_id)
            )
            
            conn.commit()

    except HTTPException:
        if conn:
            conn.rollback()
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()

async def reactivate_exam_set(exam_set_id: int) -> None:
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # 1) Kiểm tra tồn tại & active
            cur.execute(
                "SELECT is_active FROM exam_sets WHERE id = %s",
                (exam_set_id,)
            )
            row = cur.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Exam set not found.")
            
            if row["is_active"]:
                # đã inactive rồi
                
                raise HTTPException(status_code=400, detail="Exam set have already actived")
            
            # 2) Soft‑delete + ghi deleted_by_user_id + cập nhật updated_at
            cur.execute(
                """
                UPDATE exam_sets
                   SET is_active = %s,
                       updated_at = now()
                 WHERE id = %s
                """,
                (True,  exam_set_id)
            )
            
            conn.commit()
        return True
    except HTTPException:
        if conn:
            conn.rollback()
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()

def delete_exam_set(exam_set_id: int):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # 1) Kiểm tra tồn tại & active
            cur.execute(
                "SELECT id FROM exams WHERE examset_id = %s",
                (exam_set_id,)
            )
            rows = cur.fetchall()
            
            for row in rows:
                exam_id = row["id"]
                
                delete_exam_data(exam_id)
            cur.execute(
                "DELETE FROM exam_sets WHERE id = %s", (exam_set_id, )
            )
        conn.commit()
    except HTTPException:
        if conn:
            conn.rollback()
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close()