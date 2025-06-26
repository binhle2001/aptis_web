import os
from typing import Optional
from fastapi import HTTPException, UploadFile, status
from services.auth_service import get_db_connection
import json

async def put_exam_submission(user_id, exam_id, submission_data, score = None,):
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, role, is_active FROM Users WHERE id = %s", (user_id,))
            user_to_delete = cur.fetchone()

            if not user_to_delete:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {user_id} not found."
                )
        with conn.cursor() as cur_validator:
            cur.execute("SELECT id FROM exam WHERE id = %s", (exam_id,))
            row = cur_validator.fetchone()
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Exam with ID {exam_id} not found."
                )
        cursor = conn.cursor()
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
async def update_exam_submission(submission_id, submission_data, score = None):
    try:
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
        answer_string = json.dumps(submission_data)
        if score is None:
            cursor.execute("UPDATE exam_submission SET answer_string = %s WHERE id = %s", (answer_string, submission_id))
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
SPEAKING_AUDIO_PATH = "raw_file/speaking"
os.makedirs(SPEAKING_AUDIO_PATH, exist_ok=True)
async def put_speaking(user_id, question_id, audio_file: Optional[UploadFile]):
    if not audio_file.filename or not audio_file.filename.lower().endswith((".mp3", ".wav")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only Excel files (.mp3, .wav) allowed.")
    file_content = await audio_file.read()
    saved_audio_file_path_str = f"{SPEAKING_AUDIO_PATH}/{user_id}_{question_id}.mp3"
    with open(saved_audio_file_path_str, "wb") as file_object: # Mở ở chế độ "wb" (write bytes)
        file_object.write(file_content) # Ghi nội dung bytes
        print(f"Uploaded Excel file saved to: {saved_audio_file_path_str}")
    return {"audio_path": saved_audio_file_path_str}



