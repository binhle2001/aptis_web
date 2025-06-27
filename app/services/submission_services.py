import base64
import os
from typing import Optional
from fastapi import HTTPException, UploadFile, status
import psycopg2
from services.auth_service import get_db_connection
import json

def put_exam_submission(user_id, exam_id, submission_data, score = None,):
    
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id, username, role, is_active FROM Users WHERE id = %s", (user_id,))
        user = cur.fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found."
            )
    with conn.cursor() as cur_validator:
        cur_validator.execute("SELECT id FROM exams WHERE id = %s", (exam_id,))
        row = cur_validator.fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exam with ID {exam_id} not found."
            )
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, exam_id FROM exam_submission WHERE user_id = %s and exam_id = %s;", (user_id, exam_id))
    row = cursor.fetchone()
    if row:
        submission_id = row["id"]
        return update_exam_submission(submission_id, submission_data, score)
        
    try:
        
        answer_string = json.dumps(submission_data)
        if score is not None:
            cursor.execute("""INSERT INTO exam_submission (user_id, exam_id, score, answer_string, is_scored) 
                           VALUES (%s, %s, %s, %s, %s) 
                           RETURNING id, user_id, exam_id, score, is_scored;""", 
                           (user_id, exam_id, score, answer_string, True))
        else:
            cursor.execute("""INSERT INTO exam_submission (user_id, exam_id, answer_string) 
                           VALUES (%s, %s, %s, %s, %s) 
                           RETURNING id, user_id, exam_id, score, is_scored;""", 
                           (user_id, exam_id, answer_string))
        conn.commit()
        row = cursor.fetchone()
        return {
            "id": row["id"],
            "user_id": row["user_id"],
            "exam_id": row["exam_id"],
            "score": row["score"],
            "is_scored": row["is_scored"]
        }
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def update_exam_submission(submission_id, submission_data, score = None):
    
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM exam_submission WHERE id = %s", (submission_id,))
        user_to_delete = cur.fetchone()

        if not user_to_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Exam submission with ID {submission_id} not found."
            )
    cursor = conn.cursor()
    try:
        answer_string = json.dumps(submission_data)
        if score is None:
            cursor.execute("UPDATE exam_submission SET answer_string = %s, is_scored = %s, score = %s WHERE id = %s", (answer_string, False, None, submission_id))
        else:
            cursor.execute("UPDATE exam_submission SET answer_string = %s, score = %s, is_scored = %s WHERE id = %s", (answer_string, score, True, submission_id))
        conn.commit()
        return {"message": "success"}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def get_submission_by_id(submission_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, exam_id, answer_string, score FROM exam_submission WHERE id = %s;", (submission_id,))
    row = cursor.fetchone()
    item = dict(row)
    item["answer"] = json.loads(item["answer_string"])
    del item["answer_string"]
    conn.close()
    cursor.close()
    return item

import psycopg2.extras

def get_list_submission(exam_id=None, is_scored=None, examset_id=None, fullname=None, page=1, limit=10):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    filters = []
    params = []

    # Xây dựng điều kiện lọc
    if exam_id is not None:
        filters.append("es.exam_id = %s")
        params.append(exam_id)

    if is_scored is not None:
        filters.append("es.is_scored = %s")
        params.append(is_scored)

    if examset_id is not None:
        filters.append("e.examset_id = %s")
        params.append(examset_id)

    if fullname:
        filters.append("u.fullname ILIKE %s")
        params.append(f"%{fullname}%")

    where_clause = " AND ".join(filters)
    if where_clause:
        where_clause = "WHERE " + where_clause

    # Truy vấn total (không phân trang)
    count_query = f"""
        SELECT COUNT(*) AS total
        FROM exam_submission es
        JOIN users u ON es.user_id = u.id
        JOIN exams e ON es.exam_id = e.id
        {where_clause}
    """
    cursor.execute(count_query, params)
    total = cursor.fetchone()["total"]

    # Truy vấn danh sách items (có phân trang)
    offset = (page - 1) * limit
    paginated_query = f"""
        SELECT
            es.id,
            es.user_id,
            es.exam_id,
            u.fullname AS user_name,
            es.score,
            es.is_scored
        FROM exam_submission es
        JOIN users u ON es.user_id = u.id
        JOIN exams e ON es.exam_id = e.id
        {where_clause}
        ORDER BY es.created_at DESC
        LIMIT %s OFFSET %s
    """
    cursor.execute(paginated_query, params + [limit, offset])
    rows = cursor.fetchall()

    conn.close()
    cursor.close()

    return {
        "total": total,
        "page": page,
        "items": [dict(row) for row in rows]
    }


def save_base64_to_audio_file(base64_str: str, output_path: str) -> None:
    """
    Giải mã chuỗi base64 và lưu thành file audio.

    Args:
        base64_str (str): Chuỗi base64 đại diện cho file âm thanh.
        output_path (str): Đường dẫn để lưu file đầu ra (ví dụ: "output.mp3").
    """
    try:
        audio_data = base64.b64decode(base64_str)
        with open(output_path, "wb") as f:
            f.write(audio_data)
    except Exception as e:
        raise RuntimeError(f"Cannot save audio file to [{output_path}]: {e}")


