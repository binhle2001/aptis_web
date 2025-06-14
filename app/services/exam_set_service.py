# Tương tự như user_service, nhưng cho ExamSets
# Các hàm: create_exam_set, get_exam_set_by_id, get_exam_set_by_code, get_exam_sets_list, update_exam_set, ...
# Ví dụ hàm create:
import psycopg2
from fastapi import HTTPException, status
from app.schemas.exam_set_schema import ExamSetCreateSchema
from app.services.auth_service import get_db_connection

async def create_exam_set(set_data: ExamSetCreateSchema, created_by_user_id: int) -> dict:
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT exam_set_id FROM ExamSets WHERE set_code = %s",
                (set_data.set_code,)
            )
            if cur.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"ExamSet with code '{set_data.set_code}' already exists."
                )
            
            cur.execute(
                """
                INSERT INTO ExamSets (set_code, title, description, overall_time_limit_minutes, created_by_user_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING exam_set_id, set_code, title, description, overall_time_limit_minutes, created_by_user_id, is_active, created_at, updated_at;
                """,
                (set_data.set_code, set_data.title, set_data.description, 
                 set_data.overall_time_limit_minutes, created_by_user_id)
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