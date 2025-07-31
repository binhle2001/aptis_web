import base64
import json
import logging
import re
import shutil
from typing import Optional
from fastapi import HTTPException, UploadFile, status
import gdown
import psycopg2
import os
from psycopg2.extras import execute_values
import requests
from ai_tools.EN.inference import speak_EN
from helpers.ai_review import generate_speaking_correction_gemini, generate_speaking_suggestion_gemini, generate_writing_review, generate_writing_suggestion_gemini, transcript_text
from helpers.excel_parser import aptis_g_v_to_json, aptis_listening_to_json, aptis_reading_to_json, aptis_speaking_to_json, aptis_writing_to_json
from services.auth_service import get_db_connection
from .google_auth_service import download_drive_file, download_drive_file_as_base64, get_google_credentials
READING_FILES_DIR = "/app/raw_file/reading"
SPEAKING_FILES_DIR = "/app/raw_file/speaking/excel"
SPEAKING_IMAGES_DIR = "/app/raw_file/speaking/image"
LISTENING_FILES_DIR = "/app/raw_file/listening"
AUDIO_FILES_DIR = "/app/raw_file/audio"
WRITING_FILE_DIR = "/app/raw_file/writing"
GV_FILES_DIR = "/app/raw_file/GV"
os.makedirs(READING_FILES_DIR, exist_ok=True)
os.makedirs(LISTENING_FILES_DIR, exist_ok=True)
os.makedirs(AUDIO_FILES_DIR, exist_ok=True)
os.makedirs(SPEAKING_IMAGES_DIR, exist_ok=True)
os.makedirs(SPEAKING_FILES_DIR, exist_ok=True)
os.makedirs(WRITING_FILE_DIR, exist_ok=True)
os.makedirs(GV_FILES_DIR, exist_ok=True)


def insert_reading_part1_json(json_data, exam_id):
    """
    Chèn dữ liệu Part 1 Reading từ JSON vào bảng reading_part_1.
    
    :param json_data: Dữ liệu JSON đầu vào (danh sách các group và câu hỏi)
    :param exam_id: ID của bài thi
    :param db_config: dict chứa thông tin kết nối DB (dbname, user, password, host, port)
    """
    insert_query = """
        INSERT INTO reading_part_1 (exam_id, group_id, question, correct_answer, option1, option2, option3, explain)
        VALUES %s
    """
    conn = get_db_connection()
    values = []
    for group in json_data:
        group_id = int(group["group"])
        for q in group["questions"]:
            question = q["sentence"]
            correct_answer = q["correct_answer"]
            explain = q["explain"]
            # Đảm bảo có đủ 3 lựa chọn, nếu thiếu thì thêm chuỗi rỗng
            options = q["options"] + [""] * (3 - len(q["options"]))
            values.append((
                exam_id,
                group_id,
                question,
                correct_answer,
                options[0],
                options[1],
                options[2],
                explain
            ))

    try:
        
        cursor = conn.cursor()
        execute_values(cursor, insert_query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Dữ liệu Part 1 đã được chèn thành công.")
    except Exception as e:
        print("Lỗi khi chèn dữ liệu:", e)
        
def insert_reading_part2_json(json_data, exam_id):
    """
    Chèn dữ liệu Part 2 Reading từ JSON vào bảng reading_part_2.
    
    :param json_data: Dữ liệu JSON đầu vào (list các nhóm với topic và câu)
    :param exam_id: ID của bài thi
    :param db_config: dict chứa thông tin kết nối DB (dbname, user, password, host, port)
    """
    insert_query = """
        INSERT INTO reading_part_2 (
            exam_id, group_id, topic, sentence_text, sentence_key, is_example_first, explain
        )
        VALUES %s
    """

    values = []
    for group_index, group in enumerate(json_data, start=1):  # group_id: 1 -> 4
        topic = group.get("topic", "")
        for sentence in group["sentences"]:
            values.append((
                exam_id,
                group_index,                    # group_id
                topic,
                sentence["text"],
                int(sentence["key"]),
                sentence["is_example_first"],
                group["explain"]
            ))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        execute_values(cursor, insert_query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Dữ liệu Part 2 đã được chèn thành công.")
    except Exception as e:
        print("❌ Lỗi khi chèn dữ liệu Part 2:", e)


def insert_reading_part3_json(json_data, exam_id):
    """
    Chèn dữ liệu Part 3 Reading từ JSON vào bảng reading_part_3.
    
    :param json_data: Dữ liệu JSON đầu vào (list các nhóm chủ đề và câu hỏi)
    :param exam_id: ID của bài thi
    :param db_config: dict chứa thông tin kết nối DB (dbname, user, password, host, port)
    """
    insert_query = """
        INSERT INTO reading_part_3 (
            exam_id, group_id, topic, question_text, correct_answer,
            person_a, person_b, person_c, person_d, explain
        )
        VALUES %s
    """

    # Mapping Person_A → A, Person_B → B, ...
    person_map = {
        "Person_A": "A",
        "Person_B": "B",
        "Person_C": "C",
        "Person_D": "D",
        "Person A": "A",
        "Person B": "B",
        "Person C": "C",
        "Person D": "D",
    }

    values = []
    for group_idx, group in enumerate(json_data, start=1):  # group_id: 1, 2, ...
        topic = group.get("topic", "").replace("TOPIC:", "").strip()
        person_a = group.get("person_A", "")
        person_b = group.get("person_B", "")
        person_c = group.get("person_C", "")
        person_d = group.get("person_D", "")

        for q in group["questions"]:
            question_text = q["text"]
            correct_person = q["correct_answer"].strip()
            explain = q["explain"]
            correct_answer = person_map.get(correct_person, "?")  # fallback ?

            values.append((
                exam_id,
                group_idx,
                topic,
                question_text,
                correct_answer,
                person_a,
                person_b,
                person_c,
                person_d,
                explain
            ))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        execute_values(cursor, insert_query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Dữ liệu Part 3 đã được chèn thành công.")
    except Exception as e:
        print("❌ Lỗi khi chèn dữ liệu Part 3:", e)
import psycopg2
from psycopg2.extras import execute_values

def insert_reading_part4_json(json_data, exam_id):
    """
    Chèn dữ liệu Part 4 Reading từ JSON vào bảng reading_part_4.
    
    :param json_data: Dữ liệu JSON đầu vào (danh sách chủ đề và câu hỏi)
    :param exam_id: ID của bài thi
    :param db_config: dict chứa thông tin kết nối DB (dbname, user, password, host, port)
    """
    insert_query = """
        INSERT INTO reading_part_4 (
            exam_id, topic, paragraph, correct_answer,
            option1, option2, option3, option4,
            option5, option6, option7, option8, explain
        )
        VALUES %s
    """

    # Chuyển 0 → A, 1 → B, ..., 7 → H
    index_to_letter = lambda i: chr(ord('A') + i)

    values = []
    for group in json_data:
        topic = group.get("topic", "").strip()
        options = group.get("options", [])

        # Chỉ lấy 8 lựa chọn đầu tiên (theo cấu trúc bảng)
        padded_options = (options + [""] * 8)[:8]

        for q in group["questions"]:
            paragraph = q["text"]
            correct_answer_index = q["correct_answer"]
            explain = q["explain"]
            correct_answer_letter = index_to_letter(correct_answer_index)

            values.append((
                exam_id,
                topic,
                paragraph,
                correct_answer_letter,
                *padded_options,
                explain
            ))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        execute_values(cursor, insert_query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Dữ liệu Part 4 đã được chèn thành công.")
    except Exception as e:
        print("❌ Lỗi khi chèn dữ liệu Part 4:", e)
        
def delete_exam_data(exam_id):
    """
    Xóa toàn bộ dữ liệu liên quan đến một exam_id trong tất cả các bảng đọc hiểu và bảng Exam.

    :param exam_id: ID của bài thi cần xóa
    :param db_config: dict thông tin kết nối DB (dbname, user, password, host, port)
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur_validate:
            cur_validate.execute("SELECT id, exam_type FROM exams WHERE id = %s", (exam_id,))
            row = cur_validate.fetchone()
            if not row:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exam with ID {exam_id} not found.")
        # Thứ tự xóa: bảng phụ → bảng chính (foreign key)
        tables = [
            'reading_part_1',
            'reading_part_2',
            'reading_part_3',
            'reading_part_4',
            "listening_part_1",
            "listening_part_2",
            "listening_part_3",
            "listening_part_4",
            "speaking",
            "writing",
            "exam_submission",
            'g_v_part1',
            'g_v_part2'
        ]

        for table in tables:
            cursor.execute(f"DELETE FROM {table} WHERE exam_id = %s", (exam_id,))

        # Xóa exam cuối cùng
        cursor.execute("DELETE FROM exams WHERE id = %s", (exam_id,))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Đã xóa toàn bộ dữ liệu của exam_id = {exam_id}")
    except Exception as e:
        print("❌ Lỗi khi xóa dữ liệu:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f" exam part with code '{exam_id}' Error.")

async def create_reading_exam_from_excel( # Đổi tên từ _from_excel hoặc _from_pdf
    exam_set_id: int,
    exam_part_code: str,
    descriptions: str, # Tiêu đề chung cho phần Reading này
    time_limit_for_part: int,
    excel_file: Optional[UploadFile], # Đây là JSON đầy đủ {"part1": ..., "part2": ...}
    created_by_user_id: int,
    original_file_path: Optional[str] = None # Đường dẫn đến file gốc đã lưu (nếu có)
) -> dict:
    conn = None

    conn = get_db_connection() 
    # --- VALIDATE EXAM SET AND EXAM PART CODE (như cũ) ---
    with conn.cursor() as cur_validate:
        cur_validate.execute("SELECT id FROM exam_sets WHERE id = %s", (exam_set_id,))
        if not cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ExamSet with ID {exam_set_id} not found.")
        cur_validate.execute(
            "SELECT id FROM exams WHERE exam_code = %s AND examset_id = %s AND exam_type = %s ", (exam_part_code, exam_set_id, 'reading')
        ) 
        if cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Reading exam part with code '{exam_part_code}' already exists in ExamSet ID {exam_set_id}.")

    # --- Bắt đầu transaction chính ---
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO Exams (examset_id, exam_code, exam_type, description,  time_limit, created_by_user_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, exam_code, exam_type, description, time_limit, is_active;
            """,
            (exam_set_id, exam_part_code, "reading", descriptions, 
                time_limit_for_part, created_by_user_id, True) 
        )
        exam_record = cur.fetchone()
        if not exam_record:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create exam record in database.")
        
        exam_id = exam_record['id']
        print(f"Created Exam (Reading Part) record with ID: {exam_id} for ExamSet ID: {exam_set_id}")
        conn.commit()
    if not excel_file.filename or not excel_file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only Excel files (.xlsx, .xls) allowed.")
    saved_excel_file_path_str =  f"{READING_FILES_DIR}/{excel_file.filename}"
    try:
        # ĐỌC NỘI DUNG FILE UPLOAD VÀ GHI
        file_content = await excel_file.read() # <<<< SỬA Ở ĐÂY: await read()
        with open(saved_excel_file_path_str, "wb") as file_object: # Mở ở chế độ "wb" (write bytes)
            file_object.write(file_content) # Ghi nội dung bytes
        print(f"Uploaded Excel file saved to: {saved_excel_file_path_str}")
    except Exception as e_save:
        # Nếu có lỗi khi lưu, xóa file nếu nó đã được tạo một phần (hiếm)
        if os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise HTTPException(status_code=500, detail=f"Could not save uploaded Excel file: {e_save}")
    finally:
        await excel_file.close() # Luôn đóng file upload
    try:
        reading_json_data = aptis_reading_to_json(saved_excel_file_path_str)
        
        part1 = reading_json_data["part1"]
        part2 = reading_json_data["part2"]
        part3 = reading_json_data["part3"]
        part4 = reading_json_data["part4"]
        insert_reading_part1_json(part1, exam_id)
        insert_reading_part2_json(part2, exam_id)
        insert_reading_part3_json(part3, exam_id)
        insert_reading_part4_json(part4, exam_id)   
        print(f"Successfully committed all parts from Excel for exam_id {exam_id}")
        return exam_record
    except HTTPException as http_exc: 
        if conn: conn.rollback() 
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise http_exc 
    except psycopg2.Error as db_err:
        if conn: conn.rollback()
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Database error during exam creation from Excel: {db_err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error (Excel): {str(db_err)}")
    except ValueError as val_err: 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Excel parsing error: {val_err}")
        delete_exam_data(exam_id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error parsing Excel file: {str(val_err)}")
    except Exception as e:
        if conn: conn.rollback()
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Unexpected error during exam creation from Excel: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred (Excel): {str(e)}")
    finally:
        if conn: conn.close()
        if excel_file: 
            try:
                await excel_file.close()
            except Exception: pass 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            try:
                os.remove(saved_excel_file_path_str)
            except Exception as e_remove:
                print(f"Error removing temp Excel file {saved_excel_file_path_str}: {e_remove}")
    
        
# delete_reading_exam_data(8)
def get_reading_exam_by_id(exam_id):
    conn = get_db_connection() 
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    result = {
        "part1": [],
        "part2": [],
        "part3": [],
        "part4": []
    }

    # ===== Part 1 =====
    # note: column is named "question", not "question_text", and only 3 options
    cur.execute("""
        SELECT group_id, question, option1, option2, option3, correct_answer, explain
            FROM reading_part_1
            WHERE exam_id = %s
            ORDER BY group_id, question_id
    """, (exam_id,))
    rows = cur.fetchall()
    # group by group_id
    part1_groups = {}
    for r in rows:
        grp = float(r["group_id"])
        part1_groups.setdefault(grp, []).append({
            "sentence": r["question"],
            "correct_answer": r["correct_answer"],
            "explain": r["explain"],
            "options": [r["option1"], r["option2"], r["option3"]]
        })
    for grp, qs in sorted(part1_groups.items()):
        result["part1"].append({
            "group": grp,
            "questions": qs
        })

    # ===== Part 2 =====
    cur.execute("""
        SELECT group_id, topic, sentence_text, sentence_key, is_example_first, explain
            FROM reading_part_2
            WHERE exam_id = %s
            ORDER BY group_id
    """, (exam_id,))
    rows = cur.fetchall()
    part2_groups = {}
    for r in rows:
        grp = float(r["group_id"])
        part2_groups.setdefault(grp, {
            "topic": r["topic"],
            "explain": r["explain"],
            "sentences": []
        })["sentences"].append({
            "key": float(r["sentence_key"]),
            "text": r["sentence_text"],
            "is_example_first": r["is_example_first"],
        })
    for grp in sorted(part2_groups):
        result["part2"].append(part2_groups[grp])

    # ===== Part 3 =====
    cur.execute("""
        SELECT group_id, topic,
                question_text, correct_answer,
                person_a, person_b, person_c, person_d, explain
            FROM reading_part_3
            WHERE exam_id = %s
            ORDER BY group_id, question_id
    """, (exam_id,))
    rows = cur.fetchall()
    part3_groups = {}
    for r in rows:
        grp = float(r["group_id"])
        part3_groups.setdefault(grp, {
            "topic": r["topic"],
            "person_A": r["person_a"],
            "person_B": r["person_b"],
            "person_C": r["person_c"],
            "person_D": r["person_d"],
            "questions": []
        })["questions"].append({
            "text": r["question_text"],
            "correct_answer": f"Person_{r['correct_answer']}",
            "explain": r["explain"]
        })
    for grp in sorted(part3_groups):
        result["part3"].append(part3_groups[grp])

    # ===== Part 4 =====
    cur.execute("""
        SELECT topic,
                option1, option2, option3, option4,
                option5, option6, option7, option8,
                paragraph, correct_answer, explain
            FROM reading_part_4
            WHERE exam_id = %s
            ORDER BY question_id
    """, (exam_id,))
    rows = cur.fetchall()
    if rows:
        opts = [
            rows[0]["option1"], rows[0]["option2"], rows[0]["option3"], rows[0]["option4"],
            rows[0]["option5"], rows[0]["option6"], rows[0]["option7"], rows[0]["option8"]
        ]
        questions = []
        for r in rows:
            idx = ord(r["correct_answer"]) - ord('A')
            questions.append({
                "text": r["paragraph"],
                "correct_answer": idx,
                "explain": r["explain"]
            })
        result["part4"].append({
            "topic": rows[0]["topic"],
            "options": opts,
            "questions": questions
        })
    cur.close()
    conn.close()
    
    return result

def get_exam_by_id(exam_id, current_user):
    try:
        conn = get_db_connection() 
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT id, exam_type, examset_id from exams WHERE id = %s", (exam_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Exam id {exam_id} not found")
        examset_id = row["examset_id"]
        role = current_user.get('role')
        if role == "guest":
            cur_set = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur_set.execute("SELECT id FROM exam_sets WHERE is_locked = false AND id = %s", (examset_id, ))
            row_set = cur_set.fetchone()
            if not row_set:
                raise HTTPException(status_code=403, detail="You do not have permission to access this resource.")
        exam_type = row["exam_type"]
        if exam_type == "reading":
            return get_reading_exam_by_id(exam_id)
        elif exam_type == "listening": 
            return get_listening_exam_by_id(exam_id)
        elif exam_type == "speaking": 
            return get_speaking_exam_by_id(exam_id)
        elif exam_type == "writing":
            return get_writing_exam_by_id(exam_id)
        elif exam_type == "g_v":
            return get_gv_exam_by_id(exam_id)
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
            cur.close()
            
def update_exam_by_id(exam_id, json_content):
    try:
        conn = get_db_connection() 
        # --- VALIDATE EXAM SET AND EXAM PART CODE (như cũ) ---
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur_validate:
            cur_validate.execute("SELECT id, exam_type FROM exams WHERE id = %s", (exam_id,)) 
            row = cur_validate.fetchone()
            if not row:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exam with ID {exam_id} not found.")
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if row["exam_type"] == "reading":
            
            tables = [
                'reading_part_1',
                'reading_part_2',
                'reading_part_3',
                'reading_part_4',
            ]

            for table in tables:
                cursor.execute(f"DELETE FROM {table} WHERE exam_id = %s", (exam_id,))
            conn.commit()
            
            part1 = json_content["part1"]
            part2 = json_content["part2"]
            part3 = json_content["part3"]
            part4 = json_content["part4"]
            insert_reading_part1_json(part1, exam_id)
            insert_reading_part2_json(part2, exam_id)
            insert_reading_part3_json(part3, exam_id)
            insert_reading_part4_json(part4, exam_id)  
            return get_reading_exam_by_id(exam_id)
        
        if row["exam_type"] == "listening":
            tables = [
                'listening_part_1',
                'listening_part_2',
                'listening_part_3',
                'listening_part_4',
            ]

            for table in tables:
                cursor.execute(f"DELETE FROM {table} WHERE exam_id = %s", (exam_id,))
            conn.commit()
            
            part1 = json_content["part1"]
            part2 = json_content["part2"]
            part3 = json_content["part3"]
            part4 = json_content["part4"]
            insert_listening_part1_json(part1, exam_id)
            
            insert_listening_part2_json(part2, exam_id)
            insert_listening_part3_json(part3, exam_id)
            insert_listening_part4_json(part4, exam_id)  
            return get_listening_exam_by_id(exam_id)
        if row["exam_type"] == "speaking":
            tables = [
                'speaking',
            ]

            for table in tables:
                cursor.execute(f"DELETE FROM {table} WHERE exam_id = %s", (exam_id,))
            conn.commit()
            insert_speaking_exam(json_content, exam_id)
            return "success"
        if row["exam_type"] == "writing":
            tables = [
                'writing',
            ]

            for table in tables:
                cursor.execute(f"DELETE FROM {table} WHERE exam_id = %s", (exam_id,))
            conn.commit()
            insert_writing_exam(json_content, exam_id)
            return "success"
        if row["exam_type"] == "g_v":
            tables = [
                'g_v_part1',
                'g_v_part2'
            ]

            for table in tables:
                cursor.execute(f"DELETE FROM {table} WHERE exam_id = %s", (exam_id,))
            conn.commit()
            insert_g_v_exam(json_content, exam_id)
            return "success"
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
            

async def update_reading_exam_from_excel( # Đổi tên từ _from_excel hoặc _from_pdf
    exam_id: int,
    excel_file: Optional[UploadFile], # Đây là JSON đầy đủ {"part1": ..., "part2": ...}
) -> dict:
    conn = None

    conn = get_db_connection() 
    # --- VALIDATE EXAM SET AND EXAM PART CODE (như cũ) ---
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur_validate:
        cur_validate.execute("SELECT id FROM exams WHERE id = %s", (exam_id,))
        if not cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exam with ID {exam_id} not found.")

    # --- Bắt đầu transaction chính ---
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """
            UPDATE Exams SET updated_at = now()
            WHERE id = %s
            RETURNING id, examset_id, exam_code, exam_type, description, time_limit, is_active;
            """,
            (exam_id, ) 
        )
        exam_record = cur.fetchone()
        if not exam_record:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update exam record in database.")
        
        exam_id = exam_record['id']
        examset_id = exam_record['examset_id']
        print(f"UPDATE Exam (Reading Part) record with ID: {exam_id} for Exam ID: {examset_id}")
        conn.commit()
    if not excel_file.filename or not excel_file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only Excel files (.xlsx, .xls) allowed.")
    saved_excel_file_path_str =  f"{READING_FILES_DIR}/{excel_file.filename}"
    try:
        # ĐỌC NỘI DUNG FILE UPLOAD VÀ GHI
        file_content = await excel_file.read() # <<<< SỬA Ở ĐÂY: await read()
        with open(saved_excel_file_path_str, "wb") as file_object: # Mở ở chế độ "wb" (write bytes)
            file_object.write(file_content) # Ghi nội dung bytes
        print(f"Uploaded Excel file saved to: {saved_excel_file_path_str}")
    except Exception as e_save:
        # Nếu có lỗi khi lưu, xóa file nếu nó đã được tạo một phần (hiếm)
        if os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise HTTPException(status_code=500, detail=f"Could not save uploaded Excel file: {e_save}")
    finally:
        await excel_file.close() # Luôn đóng file upload
    try:
        reading_json_data = aptis_reading_to_json(saved_excel_file_path_str)
        
        update_exam_by_id(exam_id, reading_json_data)
        return exam_record
    except HTTPException as http_exc: 
        if conn: conn.rollback() 
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise http_exc 
    except psycopg2.Error as db_err:
        if conn: conn.rollback()
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Database error during exam creation from Excel: {db_err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error (Excel): {str(db_err)}")
    except ValueError as val_err: 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Excel parsing error: {val_err}")
        # delete_exam_data(exam_id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error parsing Excel file: {str(val_err)}")
    except Exception as e:
        if conn: conn.rollback()
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Unexpected error during exam creation from Excel: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred (Excel): {str(e)}")
    finally:
        if conn: conn.close()
        if excel_file: 
            try:
                await excel_file.close()
            except Exception: pass 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            try:
                os.remove(saved_excel_file_path_str)
            except Exception as e_remove:
                print(f"Error removing temp Excel file {saved_excel_file_path_str}: {e_remove}")
                
                
def insert_listening_part1_json(json_data, exam_id):
    """
    json_data: list of dict như bạn đưa vào
    exam_id: integer
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    try:
        # 1) Insert tạm JSON vào DB (audio_path = link gốc)
        insert_sql = """
            INSERT INTO listening_part_1
                (exam_id, question, audio_path, correct_answer, option1, option2, option3, transcript, explain)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for item in json_data:
            q       = item['question']
            link    = item['audio_link']
            ans     = int(item['correct_answer'])
            opt1, opt2, opt3 = item['options']
            transcript = item["transcript"]
            
            explain = item["explain"]
            cur.execute(insert_sql, (
                exam_id, q, link, ans, opt1, opt2, opt3, transcript, explain
            ))
        conn.commit()
        
        return "success"
    
    except Exception as e:
        conn.rollback()
        raise f"error: {e}"
    
    finally:
        cur.close()
        conn.close()
        
def insert_listening_part2_json(json_data, exam_id):
    """
    json_data: list of dict có keys: topic, audio_link, a, b, c, d, options[6]
    exam_id: integer
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        # 1) Insert tạm vào DB (a,b,c,d = giá trị answer, audio_path = link gốc)
        insert_sql = """
            INSERT INTO listening_part_2
              (exam_id, topic, audio_path, a, b, c, d,
               option1, option2, option3, option4, option5, option6, transcript, explain)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        for item in json_data:
            
            topic = item['topic']
            # hỗ trợ cả key audio_link và lỡ JSON chứa audio_path
            link  = item.get('audio_link') or item.get('audio_path')
            a = int(item['a'])
            b = int(item['b'])
            c = int(item['c'])
            d = int(item['d'])
            transcript = item["transcript"]
            explain = item["explain"]
            
            opts = item.get('options', [])
            # unpack 6 options, nếu thiếu thì None
            o1,o2,o3,o4,o5,o6 = (opts + [None]*6)[:6]
            
            cur.execute(insert_sql, (
                exam_id, topic, link,
                a, b, c, d,
                o1, o2, o3, o4, o5, o6, transcript, explain
            ))
        conn.commit()
        return "success"
    except Exception as e:
        conn.rollback()
        raise f"error: {e}"

    finally:
        cur.close()
        conn.close()


def insert_listening_part3_json(json_data, exam_id):
    """
    json_data: list of dict có keys: topic, questions[list], correct_answers[list], audio_link
    exam_id: integer
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # 1) Insert tạm vào DB (audio_path = link gốc)
        insert_sql = """
            INSERT INTO listening_part_3
              (exam_id, topic, question, correct_answer, audio_path, transcript, explain)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        for item in json_data:
            topic = item.get('topic')
            link  = item.get('audio_link')
            questions = item.get('questions', [])
            answers   = item.get('correct_answers', [])
            transcript = item.get("transcript")
            explains = item.get("explains", [])
            # mỗi item chứa 4 câu liên tiếp
            for q_text, ans, explain in zip(questions, answers, explains):
                cur.execute(insert_sql, (
                    exam_id,
                    topic,
                    q_text,
                    ans,
                    link, 
                    transcript,
                    explain
                ))
        conn.commit()
        return "success"

    except Exception as e:
        conn.rollback()
        raise f"error: {e}"

    finally:
        cur.close()
        conn.close()
def insert_listening_part4_json(json_data, exam_id):
    """
    json_data: list of dict có keys: topic, audio_link, questions[list], correct_answers[list], options[list of lists]
    exam_id: integer
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # 1) Insert tạm vào DB (audio_path = link gốc)
        insert_sql = """
            INSERT INTO listening_part_4
              (exam_id, topic, question, correct_answer, audio_path,
               option1, option2, option3, transcript, explain)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for item in json_data:
            topic = item.get('topic')
            link  = item.get('audio_link')
            questions = item.get('questions', [])
            answers   = item.get('correct_answers', [])
            opts_list = item.get('options', [])
            transcript = item.get("transcript")
            explains = item.get('explains', [])
            # Mỗi item chứa n câu (ở ví dụ là 2)
            for idx, (q_text, ans, opts, explain) in enumerate(zip(questions, answers, opts_list, explains), start=1):
                o1,o2,o3 = (opts + [None]*3)[:3]
                cur.execute(insert_sql, (
                    exam_id,
                    topic,
                    q_text,
                    int(ans),
                    link,
                    o1, o2, o3,
                    transcript,
                    explain
                ))
        conn.commit()
        return "success"

    except Exception as e:
        conn.rollback()
        raise f"error: {e}"

    finally:
        cur.close()
        conn.close()
        
async def create_listening_exam_from_excel( # Đổi tên từ _from_excel hoặc _from_pdf
    exam_set_id: int,
    exam_part_code: str,
    descriptions: str, # Tiêu đề chung cho phần Reading này
    time_limit_for_part: int,
    excel_file: Optional[UploadFile], # Đây là JSON đầy đủ {"part1": ..., "part2": ...}
    created_by_user_id: int,
    original_file_path: Optional[str] = None # Đường dẫn đến file gốc đã lưu (nếu có)
) -> dict:
    conn = None

    conn = get_db_connection() 
    # --- VALIDATE EXAM SET AND EXAM PART CODE (như cũ) ---
    with conn.cursor() as cur_validate:
        cur_validate.execute("SELECT id FROM exam_sets WHERE id = %s", (exam_set_id,))
        if not cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ExamSet with ID {exam_set_id} not found.")
        cur_validate.execute(
            "SELECT id FROM exams WHERE exam_code = %s AND examset_id = %s AND exam_type = %s ", (exam_part_code, exam_set_id, 'listening')
        ) 
        if cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Reading exam part with code '{exam_part_code}' already exists in ExamSet ID {exam_set_id}.")

    # --- Bắt đầu transaction chính ---
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO Exams (examset_id, exam_code, exam_type, description,  time_limit, created_by_user_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, exam_code, exam_type, description, time_limit, is_active;
            """,
            (exam_set_id, exam_part_code, "listening", descriptions, 
                time_limit_for_part, created_by_user_id, True) 
        )
        exam_record = cur.fetchone()
        if not exam_record:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create exam record in database.")
        
        exam_id = exam_record['id']
        print(f"Created Exam (Listening Part) record with ID: {exam_id} for ExamSet ID: {exam_set_id}")
        conn.commit()
    if not excel_file.filename or not excel_file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only Excel files (.xlsx, .xls) allowed.")
    saved_excel_file_path_str =  f"{LISTENING_FILES_DIR}/{excel_file.filename}"
    try:
        # ĐỌC NỘI DUNG FILE UPLOAD VÀ GHI
        file_content = await excel_file.read() # <<<< SỬA Ở ĐÂY: await read()
        with open(saved_excel_file_path_str, "wb") as file_object: # Mở ở chế độ "wb" (write bytes)
            file_object.write(file_content) # Ghi nội dung bytes
        print(f"Uploaded Excel file saved to: {saved_excel_file_path_str}")
    except Exception as e_save:
        # Nếu có lỗi khi lưu, xóa file nếu nó đã được tạo một phần (hiếm)
        if os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise HTTPException(status_code=500, detail=f"Could not save uploaded Excel file: {e_save}")
    finally:
        await excel_file.close() # Luôn đóng file upload
    try:
        listening_json_data = aptis_listening_to_json(saved_excel_file_path_str)
        
        part1 = listening_json_data["part1"]
        part2 = listening_json_data["part2"]
        part3 = listening_json_data["part3"]
        part4 = listening_json_data["part4"]
        result_1 = insert_listening_part1_json(part1, exam_id)
        result_2 = insert_listening_part2_json(part2, exam_id)
        result_3 = insert_listening_part3_json(part3, exam_id)
        result_4 = insert_listening_part4_json(part4, exam_id)   
        print(f"Successfully committed all parts from Excel for exam_id {exam_id}")
        return exam_record
    except HTTPException as http_exc: 
        if conn: conn.rollback() 
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise http_exc 
    except psycopg2.Error as db_err:
        if conn: conn.rollback()
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Database error during exam creation from Excel: {db_err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error (Excel): {str(db_err)}")
    except ValueError as val_err: 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Excel parsing error: {val_err}")
        delete_exam_data(exam_id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error parsing Excel file: {str(val_err)}")
    except Exception as e:
        if conn: conn.rollback()
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Unexpected error during exam creation from Excel: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred (Excel): {str(e)}")
    finally:
        if conn: conn.close()
        if excel_file: 
            try:
                await excel_file.close()
            except Exception: pass 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            try:
                os.remove(saved_excel_file_path_str)
            except Exception as e_remove:
                print(f"Error removing temp Excel file {saved_excel_file_path_str}: {e_remove}")
                
                
async def update_listening_exam_from_excel( # Đổi tên từ _from_excel hoặc _from_pdf
    exam_id: int,
    excel_file: Optional[UploadFile], # Đây là JSON đầy đủ {"part1": ..., "part2": ...}
) -> dict:
    conn = None

    conn = get_db_connection() 
    # --- VALIDATE EXAM SET AND EXAM PART CODE (như cũ) ---
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur_validate:
        cur_validate.execute("SELECT id FROM exams WHERE id = %s", (exam_id,))
        if not cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exam with ID {exam_id} not found.")
    
    # --- Bắt đầu transaction chính ---
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """
            UPDATE Exams SET updated_at = now()
            WHERE id = %s
            RETURNING id, examset_id, exam_code, exam_type, description, time_limit, is_active;
            """,
            (exam_id,) 
        )
   
        exam_record = cur.fetchone()
        if not exam_record:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update exam record in database.")
        
        exam_id = exam_record['id']
        examset_id = exam_record['examset_id']
        print(f"UPDATE Exam (Listening Part) record with ID: {exam_id} for Exam ID: {examset_id}")
        conn.commit()
    if not excel_file.filename or not excel_file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only Excel files (.xlsx, .xls) allowed.")
    saved_excel_file_path_str =  f"{LISTENING_FILES_DIR}/{excel_file.filename}"
    try:
        # ĐỌC NỘI DUNG FILE UPLOAD VÀ GHI
        file_content = await excel_file.read() # <<<< SỬA Ở ĐÂY: await read()
        with open(saved_excel_file_path_str, "wb") as file_object: # Mở ở chế độ "wb" (write bytes)
            file_object.write(file_content) # Ghi nội dung bytes
        print(f"Uploaded Excel file saved to: {saved_excel_file_path_str}")
    except Exception as e_save:
        # Nếu có lỗi khi lưu, xóa file nếu nó đã được tạo một phần (hiếm)
        if os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise HTTPException(status_code=500, detail=f"Could not save uploaded Excel file: {e_save}")
    finally:
        await excel_file.close() # Luôn đóng file upload
    try:
        listening_json_data = aptis_listening_to_json(saved_excel_file_path_str)
        
        update_exam_by_id(exam_id, listening_json_data)
        return exam_record
    except HTTPException as http_exc: 
        if conn: conn.rollback() 
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise http_exc 
    except psycopg2.Error as db_err:
        if conn: conn.rollback()
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Database error during exam creation from Excel: {db_err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error (Excel): {str(db_err)}")
    except ValueError as val_err: 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Excel parsing error: {val_err}")
        # delete_exam_data(exam_id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error parsing Excel file: {str(val_err)}")
    except Exception as e:
        if conn: conn.rollback()
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Unexpected error during exam creation from Excel: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred (Excel): {str(e)}")
    finally:
        if conn: conn.close()
        if excel_file: 
            try:
                await excel_file.close()
            except Exception: pass 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            try:
                os.remove(saved_excel_file_path_str)
            except Exception as e_remove:
                print(f"Error removing temp Excel file {saved_excel_file_path_str}: {e_remove}")
                
                
def get_listening_exam_by_id(exam_id: int) -> dict:
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        result = {}

        # --- Part 1
        cur.execute("""
            SELECT question,
                   audio_path  AS audio_link,
                   correct_answer,
                   ARRAY[option1, option2, option3] AS options,
                   transcript,
                   explain
              FROM listening_part_1
             WHERE exam_id = %s
             ORDER BY id
        """, (exam_id,))
        result['part1'] = cur.fetchall()

        # --- Part 2
        cur.execute("""
            SELECT topic,
                   audio_path  AS audio_link,
                   a, b, c, d,
                   ARRAY[option1, option2, option3, option4, option5, option6] AS options,
                   transcript,
                   explain
              FROM listening_part_2
             WHERE exam_id = %s
             ORDER BY id
        """, (exam_id,))
        
        rows2 = cur.fetchall()
        part2 = []
        for r in rows2:
            part2.append({
                "topic":      r['topic'],
                "audio_link": r['audio_link'],
                "a":          r['a'],
                "b":          r['b'],
                "c":          r['c'],
                "d":          r['d'],
                "options":    r['options'],
                "transcript": r["transcript"],
                "explain":    r["explain"],
            })
        result['part2'] = part2
       
        # --- Part 3: chỉ tạo 1 block cho mỗi audio_link
        cur.execute("""
            SELECT topic,
                   question,
                   correct_answer,
                   audio_path AS audio_link,
                   transcript,
                   explain
              FROM listening_part_3
             WHERE exam_id = %s
             ORDER BY id
        """, (exam_id,))
        rows3 = cur.fetchall()

        if rows3:
            # Lấy topic và audio_link từ bản ghi đầu
            first = rows3[0]
            block3 = {
                "topic":           first['topic'],
                "audio_link":      first['audio_link'],
                "transcript":      first["transcript"],
                "questions":       [r['question']        for r in rows3],
                "correct_answers": [r['correct_answer'].strip()  for r in rows3],
                "explains":        [r['explain'] for r in rows3]
            }
            result['part3'] = [block3]
        else:
            result['part3'] = []
        
        # --- Part 4: gom theo audio_link nhưng giữ nhiều block nếu link khác nhau
        cur.execute("""
            SELECT topic,
                   question,
                   correct_answer,
                   audio_path  AS audio_link,
                   option1, option2, option3,
                   transcript, explain
              FROM listening_part_4
             WHERE exam_id = %s
             ORDER BY id
        """, (exam_id,))
        rows4 = cur.fetchall()

        part4 = []
        seen4 = set()
        for row in rows4:
            link = row['audio_link']
            if link not in seen4:
                seen4.add(link)
                part4.append({
                    "topic":           row['topic'],
                    "audio_link":      link,
                    "questions":       [],
                    "correct_answers": [],
                    "options":         [],
                    "transcript": row["transcript"],
                    "explain": []
                })
            # tìm block tương ứng
            blk = next(b for b in part4 if b['audio_link'] == link)
            blk['questions'].append(row['question'])
            blk['correct_answers'].append(row['correct_answer'])
            blk['options'].append([row['option1'], row['option2'], row['option3']])
            blk['explain'].append(row['explain'])
        result['part4'] = part4

        return result

    finally:
        cur.close()
        conn.close()

def load_audio_as_base64(path_or_url: str) -> str:
    """
    Nếu path_or_url là URL Google Drive thì dùng API để tải về bằng credentials,
    nếu là đường dẫn local thì mở file từ disk.
    Trả về chuỗi Base64 của file.
    """
    try:
        if path_or_url.lower().startswith("http"):
            # Xử lý URL từ Google Drive
            base64_data = download_drive_file_as_base64(path_or_url)
            if base64_data is None:
                raise Exception("Không thể tải hoặc mã hóa file từ Google Drive.")
            return base64_data
        else:
            # Đọc file local
            with open(path_or_url, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode("utf-8")
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail      = f"Cannot load audio [{path_or_url}]: {e}"
        )


def _ensure_drive_url(url: str) -> str:
    m = re.search(r'/d/([^/]+)/', url)
    return f"https://drive.google.com/uc?id={m.group(1)}" if m else url


def _download_file(url: str, local_path: str):
    if os.path.exists(local_path):
        return
    try:
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in resp.iter_content(1024 * 8):
                f.write(chunk)
        print(f"Downloaded: {url} -> {local_path}")
    except Exception as e:
        print(f"Download failed [{url}]: {e}")

# --- Main download function



def download_all_listening():
    conn = get_db_connection()
    cur  = conn.cursor()
    creds = get_google_credentials()
    if not creds:
        print("❌ Không thể xác thực Google. Dừng tiến trình.")
        return

    for part in range(1, 5):
        table = f"listening_part_{part}"
        cur.execute(f"SELECT id, exam_id, audio_path FROM {table} WHERE audio_path IS NOT NULL ORDER BY id")
        rows = cur.fetchall()

        for row in rows:
            rec_id, exam_id, path_in = row['id'], row['exam_id'], row['audio_path']

            # Kiểm tra URL Google Drive hay file local
            is_drive_url = path_in.strip().lower().startswith('http')
            local_fname = f"{exam_id}_part{part}_{rec_id}.mp3"
            local_path  = f"/app/raw_file/audio/{local_fname}"
            
            if is_drive_url:
                
                try:
                    # Tải dữ liệu và ghi ra file local
                    print(f"🔽 Đang tải từ Google Drive: {path_in}")
                    base64_data = download_drive_file_as_base64(path_in, creds)
                    if not base64_data:
                        raise Exception("Không thể tải hoặc mã hóa từ Google Drive.")

                    # Giải mã Base64 và lưu ra file
                    file_bytes = base64.b64decode(base64_data)
                    with open(local_path, "wb") as f:
                        f.write(file_bytes)

                    print(f"✅ Đã lưu: {local_path}")

                    # Cập nhật đường dẫn mới vào database
                    cur.execute(f"""
                        UPDATE {table}
                           SET audio_path = %s
                         WHERE id = %s
                    """, (local_path, rec_id))
                    conn.commit()

                except Exception as e:
                    print(f"❌ Lỗi khi tải file từ Google Drive: {e}")
                    cur.close()
                    conn.close()
                    return
            else:
                # Đường dẫn local
                if os.path.exists(path_in):
                    print(f"📁 File local tồn tại: {path_in}")
                else:
                    print(f"❌ Thiếu file local: {path_in}")

    cur.close()
    conn.close()



def download_all_images():
    conn = get_db_connection()
    cur  = conn.cursor()
    table = "speaking"

    creds = get_google_credentials()
    if not creds:
        print("❌ Không thể xác thực Google. Dừng tiến trình.")
        return

    cur.execute(f"SELECT id, exam_id, image_path1, image_path2 FROM {table}")
    rows = cur.fetchall()

    for row in rows:
        rec_id, exam_id, image_path1, image_path2 = row['id'], row['exam_id'], row['image_path1'], row['image_path2']

        for idx, img_url in enumerate([image_path1, image_path2], start=1):
            if img_url and img_url.lower().startswith('http'):
                try:
                    print(f"🔽 Đang tải ảnh {idx} cho record #{rec_id}: {img_url}")
                    base64_data = download_drive_file_as_base64(img_url, creds)
                    if not base64_data:
                        raise Exception("Không thể tải hoặc mã hóa file ảnh từ Google Drive.")

                    # Giải mã và lưu ảnh ra file
                    local_path = f"{SPEAKING_IMAGES_DIR}/{rec_id}_{idx}.jpg"
                    with open(local_path, "wb") as f:
                        f.write(base64.b64decode(base64_data))
                    print(f"✅ Đã lưu ảnh {idx} tại: {local_path}")

                    # Cập nhật lại đường dẫn ảnh trong DB
                    field = f"image_path{idx}"
                    cur.execute(f"""
                        UPDATE {table}
                           SET {field} = %s
                         WHERE id = %s
                    """, (local_path, rec_id))
                    conn.commit()
                except Exception as e:
                    print(f"❌ Lỗi khi tải ảnh {idx} của record #{rec_id}: {e}")

    cur.close()
    conn.close()

def create_instruction_audio():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for i in range(1, 5):
        cursor.execute("SELECT id, instruction, topic, instruction_audio, question FROM speaking WHERE part_id = %s", (i,))
        rows = cursor.fetchall()
        for k, row in enumerate(rows):
            if row["instruction_audio"] is None:
                question_id = row["id"]
                output_path = f"/app/raw_file/speaking/instruction/{question_id}.mp3"
                instruction = row["instruction"]
                question = row["question"]
                topic = row["topic"]
                text = question
                audio_instruction = speak_EN(text, output_path = output_path)
                cursor.execute("UPDATE speaking SET instruction_audio = %s WHERE id = %s", (audio_instruction, question_id))
                conn.commit()
    cursor.close()
    conn.close()


# Giả sử bạn có hàm get_db_connection()
# from .database import get_db_connection

def insert_speaking_exam(json_data: str, exam_id: int):
    """
    Phân tích chuỗi JSON và ghi các câu hỏi vào bảng 'speaking'.
    Hàm này được thiết kế để hoạt động với CSDL có 2 cột ảnh riêng biệt:
    image_path_1 và image_path_2.

    Args:
        json_data (str): Chuỗi JSON chứa dữ liệu các phần thi Speaking.
        exam_id (int): ID của bài thi (exam) mà các câu hỏi này thuộc về.

    Returns:
        int: Số lượng câu hỏi đã được thêm thành công.
    """
    conn = None
    questions_added_count = 0

    try:
        # Parse chuỗi JSON
        exam_parts = json.loads(json_data)
        if not isinstance(exam_parts, list):
            raise ValueError("JSON đầu vào phải là một danh sách (list).")

        conn = get_db_connection()
        with conn.cursor() as cur:
            for part_data in exam_parts:
                part_id = part_data.get("part")
                topic = part_data.get("topic")
                instruction = part_data.get("instruction")
                questions = part_data.get("question", [])

                # Lấy URL ảnh từ JSON
                image_url_1 = part_data.get("image_url_1")
                image_url_2 = part_data.get("image_url_2")
                
                # Lặp qua các câu hỏi
                for index, question_text in enumerate(questions):
                    
                    # Chỉ gán ảnh cho câu hỏi đầu tiên (index == 0) của Part 2, 3, 4
                    final_image_1 = None
                    final_image_2 = None
                    if index == 0 and part_id in [2, 3, 4]:
                        final_image_1 = image_url_1
                        final_image_2 = image_url_2
                    
                    # Các câu hỏi tiếp theo sẽ có cả hai trường ảnh là None
                    
                    sql_command = """
                        INSERT INTO speaking 
                        (exam_id, part_id, topic, instruction, question, image_path1, image_path2) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """
                    cur.execute(sql_command, (
                        exam_id, part_id, topic, instruction, 
                        question_text, final_image_1, final_image_2
                    ))
                    questions_added_count += 1
            
            conn.commit()
            print(f"Thành công! Đã thêm {questions_added_count} câu hỏi vào CSDL cho exam_id={exam_id}.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Lỗi! Giao dịch sẽ được rollback. Chi tiết: {error}")
        if conn:
            conn.rollback()
        raise error
    finally:
        if conn:
            conn.close()
    
    return questions_added_count
   
async def create_speaking_exam_from_excel( # Đổi tên từ _from_excel hoặc _from_pdf
    exam_set_id: int,
    exam_part_code: str,
    descriptions: str, # Tiêu đề chung cho phần Reading này
    time_limit_for_part: int,
    excel_file: Optional[UploadFile], # Đây là JSON đầy đủ {"part1": ..., "part2": ...}
    created_by_user_id: int,
    original_file_path: Optional[str] = None # Đường dẫn đến file gốc đã lưu (nếu có)
) -> dict:
    conn = None

    conn = get_db_connection() 
    # --- VALIDATE EXAM SET AND EXAM PART CODE (như cũ) ---
    with conn.cursor() as cur_validate:
        cur_validate.execute("SELECT id FROM exam_sets WHERE id = %s", (exam_set_id,))
        if not cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ExamSet with ID {exam_set_id} not found.")
        cur_validate.execute(
            "SELECT id FROM exams WHERE exam_code = %s AND examset_id = %s AND exam_type = %s ", (exam_part_code, exam_set_id, 'speaking')
        ) 
        if cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Speaking exam part with code '{exam_part_code}' already exists in ExamSet ID {exam_set_id}.")

    # --- Bắt đầu transaction chính ---
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO Exams (examset_id, exam_code, exam_type, description,  time_limit, created_by_user_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, exam_code, exam_type, description, time_limit, is_active;
            """,
            (exam_set_id, exam_part_code, "speaking", descriptions, 
                time_limit_for_part, created_by_user_id, True) 
        )
        exam_record = cur.fetchone()
        if not exam_record:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create exam record in database.")
        
        exam_id = exam_record['id']
        print(f"Created Exam (SPEAKING Part) record with ID: {exam_id} for ExamSet ID: {exam_set_id}")
        conn.commit()
    if not excel_file.filename or not excel_file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only Excel files (.xlsx, .xls) allowed.")
    saved_excel_file_path_str =  f"{SPEAKING_FILES_DIR}/{excel_file.filename}"
    print("📦 File exists:", os.path.exists(saved_excel_file_path_str))
    try:
        # ĐỌC NỘI DUNG FILE UPLOAD VÀ GHI
        file_content = await excel_file.read() # <<<< SỬA Ở ĐÂY: await read()
        with open(saved_excel_file_path_str, "wb") as file_object: # Mở ở chế độ "wb" (write bytes)
            file_object.write(file_content) # Ghi nội dung bytes
        print(f"Uploaded Excel file saved to: {saved_excel_file_path_str}")
    except Exception as e_save:
        # Nếu có lỗi khi lưu, xóa file nếu nó đã được tạo một phần (hiếm)
        if os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise HTTPException(status_code=500, detail=f"Could not save uploaded Excel file: {e_save}")
    finally:
        await excel_file.close() # Luôn đóng file upload
    try:
        speaking_json_data = aptis_speaking_to_json(saved_excel_file_path_str)
        
        insert_speaking_exam(speaking_json_data, exam_id)
        print(f"Successfully committed all parts from Excel for exam_id {exam_id}")
        return exam_record
    except HTTPException as http_exc: 
        if conn: conn.rollback() 
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise http_exc 
    except psycopg2.Error as db_err:
        if conn: conn.rollback()
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Database error during exam creation from Excel: {db_err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error (Excel): {str(db_err)}")
    except ValueError as val_err: 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Excel parsing error: {val_err}")
        delete_exam_data(exam_id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error parsing Excel file: {str(val_err)}")
    except Exception as e:
        if conn: conn.rollback()
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Unexpected error during exam creation from Excel: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred (Excel): {str(e)}")
    finally:
        if conn: conn.close()
        if excel_file: 
            try:
                await excel_file.close()
            except Exception: pass 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            try:
                os.remove(saved_excel_file_path_str)
            except Exception as e_remove:
                print(f"Error removing temp Excel file {saved_excel_file_path_str}: {e_remove}")
                

            

async def update_speaking_exam_from_excel( # Đổi tên từ _from_excel hoặc _from_pdf
    exam_id: int,
    excel_file: Optional[UploadFile], # Đây là JSON đầy đủ {"part1": ..., "part2": ...}
) -> dict:
    conn = None

    conn = get_db_connection() 
    # --- VALIDATE EXAM SET AND EXAM PART CODE (như cũ) ---
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur_validate:
        cur_validate.execute("SELECT id FROM exams WHERE id = %s", (exam_id,))
        if not cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exam with ID {exam_id} not found.")
    
    # --- Bắt đầu transaction chính ---
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """
            UPDATE Exams SET updated_at = now()
            WHERE id = %s
            RETURNING id, examset_id, exam_code, exam_type, description, time_limit, is_active;
            """,
            (exam_id,) 
        )
   
        exam_record = cur.fetchone()
        if not exam_record:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update exam record in database.")
        
        exam_id = exam_record['id']
        examset_id = exam_record['examset_id']
        print(f"UPDATE Exam (speaking Part) record with ID: {exam_id} for Exam ID: {examset_id}")
        conn.commit()
    if not excel_file.filename or not excel_file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only Excel files (.xlsx, .xls) allowed.")
    saved_excel_file_path_str =  f"{SPEAKING_FILES_DIR}/{excel_file.filename}"
    try:
        # ĐỌC NỘI DUNG FILE UPLOAD VÀ GHI
        file_content = await excel_file.read() # <<<< SỬA Ở ĐÂY: await read()
        with open(saved_excel_file_path_str, "wb") as file_object: # Mở ở chế độ "wb" (write bytes)
            file_object.write(file_content) # Ghi nội dung bytes
        print(f"Uploaded Excel file saved to: {saved_excel_file_path_str}")
        print("📦 File exists:", os.path.exists(saved_excel_file_path_str))
    except Exception as e_save:
        # Nếu có lỗi khi lưu, xóa file nếu nó đã được tạo một phần (hiếm)
        if os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise HTTPException(status_code=500, detail=f"Could not save uploaded Excel file: {e_save}")
    finally:
        await excel_file.close() # Luôn đóng file upload
    try:
        speaking_json_data = aptis_speaking_to_json(saved_excel_file_path_str)
        
        update_exam_by_id(exam_id, speaking_json_data)
        return exam_record
    except HTTPException as http_exc: 
        if conn: conn.rollback() 
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise http_exc 
    except psycopg2.Error as db_err:
        if conn: conn.rollback()
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Database error during exam creation from Excel: {db_err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error (Excel): {str(db_err)}")
    except ValueError as val_err: 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Excel parsing error: {val_err}")
        # delete_exam_data(exam_id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error parsing Excel file: {str(val_err)}")
    except Exception as e:
        if conn: conn.rollback()
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Unexpected error during exam creation from Excel: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred (Excel): {str(e)}")
    finally:
        if conn: conn.close()
        if excel_file: 
            try:
                await excel_file.close()
            except Exception: pass 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            try:
                os.remove(saved_excel_file_path_str)
            except Exception as e_remove:
                print(f"Error removing temp Excel file {saved_excel_file_path_str}: {e_remove}")

def get_speaking_exam_by_id(exam_id):
    """
    Lấy dữ liệu đề thi speaking từ CSDL và tái tạo lại cấu trúc JSON gốc.

    Args:
        exam_id (int): ID của bài thi (exam) cần lấy.

    Returns:
        str: Một chuỗi JSON đại diện cho đề thi. 
             Trả về một chuỗi JSON danh sách rỗng '[]' nếu không tìm thấy đề thi.
    """
    conn = None
    try:
        conn = get_db_connection()
        # RealDictCursor trả về kết quả dưới dạng dictionary, rất tiện lợi
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            # Lấy tất cả câu hỏi của exam, sắp xếp theo part và id để đảm bảo thứ tự
            cur.execute("""
                SELECT id, part_id, topic, instruction, instruction_audio, question, image_path1, image_path2 
                FROM speaking
                WHERE exam_id = %s
                ORDER BY part_id, id;
            """, (exam_id,))
            
            rows = cur.fetchall()
            
            if not rows:
                # Nếu không có câu hỏi nào, trả về danh sách rỗng
                return "[]"

            # Dictionary để nhóm các câu hỏi theo part_id
            parts_data = {}

            # Lặp qua các hàng kết quả để xây dựng lại cấu trúc JSON
            for row in rows:
                part_id = row['part_id']
                
                # Nếu đây là lần đầu tiên gặp part_id này
                if part_id not in parts_data:
                    # Tạo một mục mới cho phần này
                    # Vì ảnh chỉ được lưu ở câu hỏi đầu tiên, ta có thể lấy luôn
                    parts_data[part_id] = {
                        "part": part_id,
                        "topic": row['topic'],
                        "instruction": row['instruction'],
                        "instruction_audio": [],
                        "question": [], # Khởi tạo danh sách câu hỏi rỗng
                        "image_url_1": row['image_path1'],
                        "image_url_2": row['image_path2']
                    }
                
                parts_data[part_id]["question"].append({"id": row["id"], "text": row['question'], "audio": row['instruction_audio']})

            # Chuyển đổi dictionary các giá trị thành một danh sách
            final_result = list(parts_data.values())

            # Chuyển đổi danh sách Python thành chuỗi JSON
            return final_result

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Lỗi khi lấy dữ liệu đề thi: {error}")
        # Ném lại lỗi để lớp cao hơn xử lý
        raise error
    finally:
        if conn:
            conn.close()

def insert_writing_exam(json_data: json, exam_id: int):
    """
    Phân tích chuỗi JSON và ghi các câu hỏi vào bảng 'writing'.
    Hàm này được thiết kế để hoạt động với CSDL có 2 cột ảnh riêng biệt:
    image_path_1 và image_path_2.

    Args:
        json_data (str): Chuỗi JSON chứa dữ liệu các phần thi writing.
        exam_id (int): ID của bài thi (exam) mà các câu hỏi này thuộc về.

    Returns:
        int: Số lượng câu hỏi đã được thêm thành công.
    """
    conn = None
    questions_added_count = 0

    try:
        # Parse chuỗi JSON
        try:
            exam_parts = json_data
            if not isinstance(exam_parts, list):
                raise ValueError("JSON đầu vào phải là một danh sách (list).")
        except json.JSONDecodeError:
            raise ValueError("Chuỗi JSON không hợp lệ.")

        conn = get_db_connection()
        with conn.cursor() as cur:
            # Lặp qua từng phần trong JSON
            for part_data in exam_parts:
                part_id = part_data.get("part_id")
                topic = part_data.get("topic")
                instruction = part_data.get("instruction")
                questions_list = part_data.get("questions", [])

                if not isinstance(questions_list, list):
                    continue

                # Lặp qua từng câu hỏi trong danh sách để tạo một hàng trong CSDL
                for question_text in questions_list:
                    sql_command = """
                        INSERT INTO writing 
                        (exam_id, part_id, topic, instruction, questions) 
                        VALUES (%s, %s, %s, %s, %s);
                    """
                    cur.execute(sql_command, (
                        exam_id, 
                        part_id, 
                        topic, 
                        instruction, 
                        question_text
                    ))
                    questions_added_count += 1
            
            # Nếu mọi thứ thành công, commit giao dịch
            conn.commit()
            print(f"Thành công! Đã thêm {questions_added_count} câu hỏi vào CSDL cho exam_id={exam_id}.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Lỗi! Giao dịch sẽ được rollback. Chi tiết: {error}")
        if conn:
            conn.rollback()
        raise error
    finally:
        if conn:
            conn.close()
    
    return questions_added_count

async def create_writing_exam_from_excel( # Đổi tên từ _from_excel hoặc _from_pdf
    exam_set_id: int,
    exam_part_code: str,
    descriptions: str, # Tiêu đề chung cho phần Reading này
    time_limit_for_part: int,
    excel_file: Optional[UploadFile], # Đây là JSON đầy đủ {"part1": ..., "part2": ...}
    created_by_user_id: int,
    original_file_path: Optional[str] = None # Đường dẫn đến file gốc đã lưu (nếu có)
) -> dict:
    conn = None

    conn = get_db_connection() 
    # --- VALIDATE EXAM SET AND EXAM PART CODE (như cũ) ---
    with conn.cursor() as cur_validate:
        cur_validate.execute("SELECT id FROM exam_sets WHERE id = %s", (exam_set_id,))
        if not cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ExamSet with ID {exam_set_id} not found.")
        cur_validate.execute(
            "SELECT id FROM exams WHERE exam_code = %s AND examset_id = %s AND exam_type = %s ", (exam_part_code, exam_set_id, 'writing')
        ) 
        if cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"writing exam part with code '{exam_part_code}' already exists in ExamSet ID {exam_set_id}.")

    # --- Bắt đầu transaction chính ---
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO Exams (examset_id, exam_code, exam_type, description,  time_limit, created_by_user_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, exam_code, exam_type, description, time_limit, is_active;
            """,
            (exam_set_id, exam_part_code, "writing", descriptions, 
                time_limit_for_part, created_by_user_id, True) 
        )
        exam_record = cur.fetchone()
        if not exam_record:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create exam record in database.")
        
        exam_id = exam_record['id']
        print(f"Created Exam (WRITING Part) record with ID: {exam_id} for ExamSet ID: {exam_set_id}")
        conn.commit()
    if not excel_file.filename or not excel_file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only Excel files (.xlsx, .xls) allowed.")
    saved_excel_file_path_str =  f"{WRITING_FILE_DIR}/{excel_file.filename}"
    print("📦 File exists:", os.path.exists(saved_excel_file_path_str))
    try:
        # ĐỌC NỘI DUNG FILE UPLOAD VÀ GHI
        file_content = await excel_file.read() # <<<< SỬA Ở ĐÂY: await read()
        with open(saved_excel_file_path_str, "wb") as file_object: # Mở ở chế độ "wb" (write bytes)
            file_object.write(file_content) # Ghi nội dung bytes
        print(f"Uploaded Excel file saved to: {saved_excel_file_path_str}")
    except Exception as e_save:
        # Nếu có lỗi khi lưu, xóa file nếu nó đã được tạo một phần (hiếm)
        if os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise HTTPException(status_code=500, detail=f"Could not save uploaded Excel file: {e_save}")
    finally:
        await excel_file.close() # Luôn đóng file upload
    try:
        writing_json_data = aptis_writing_to_json(saved_excel_file_path_str)
        
        insert_writing_exam(writing_json_data, exam_id)
        print(f"Successfully committed all parts from Excel for exam_id {exam_id}")
        return exam_record
    except HTTPException as http_exc: 
        if conn: conn.rollback() 
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise http_exc 
    except psycopg2.Error as db_err:
        if conn: conn.rollback()
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Database error during exam creation from Excel: {db_err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error (Excel): {str(db_err)}")
    except ValueError as val_err: 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Excel parsing error: {val_err}")
        delete_exam_data(exam_id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error parsing Excel file: {str(val_err)}")
    except Exception as e:
        if conn: conn.rollback()
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Unexpected error during exam creation from Excel: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred (Excel): {str(e)}")
    finally:
        if conn: conn.close()
        if excel_file: 
            try:
                await excel_file.close()
            except Exception: pass 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            try:
                os.remove(saved_excel_file_path_str)
            except Exception as e_remove:
                print(f"Error removing temp Excel file {saved_excel_file_path_str}: {e_remove}")
                

            

async def update_writing_exam_from_excel( # Đổi tên từ _from_excel hoặc _from_pdf
    exam_id: int,
    excel_file: Optional[UploadFile], # Đây là JSON đầy đủ {"part1": ..., "part2": ...}
) -> dict:
    conn = None

    conn = get_db_connection() 
    # --- VALIDATE EXAM SET AND EXAM PART CODE (như cũ) ---
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur_validate:
        cur_validate.execute("SELECT id FROM exams WHERE id = %s", (exam_id,))
        if not cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exam with ID {exam_id} not found.")
    
    # --- Bắt đầu transaction chính ---
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """
            UPDATE Exams SET updated_at = now()
            WHERE id = %s
            RETURNING id, examset_id, exam_code, exam_type, description, time_limit, is_active;
            """,
            (exam_id,) 
        )
   
        exam_record = cur.fetchone()
        if not exam_record:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update exam record in database.")
        
        exam_id = exam_record['id']
        examset_id = exam_record['examset_id']
        print(f"UPDATE Exam (Writing Part) record with ID: {exam_id} for Exam ID: {examset_id}")
        conn.commit()
    if not excel_file.filename or not excel_file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only Excel files (.xlsx, .xls) allowed.")
    saved_excel_file_path_str =  f"{WRITING_FILE_DIR}/{excel_file.filename}"
    try:
        # ĐỌC NỘI DUNG FILE UPLOAD VÀ GHI
        file_content = await excel_file.read() # <<<< SỬA Ở ĐÂY: await read()
        with open(saved_excel_file_path_str, "wb") as file_object: # Mở ở chế độ "wb" (write bytes)
            file_object.write(file_content) # Ghi nội dung bytes
        print(f"Uploaded Excel file saved to: {saved_excel_file_path_str}")
        print("📦 File exists:", os.path.exists(saved_excel_file_path_str))
    except Exception as e_save:
        # Nếu có lỗi khi lưu, xóa file nếu nó đã được tạo một phần (hiếm)
        if os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise HTTPException(status_code=500, detail=f"Could not save uploaded Excel file: {e_save}")
    finally:
        await excel_file.close() # Luôn đóng file upload
    try:
        writing_json_data = aptis_writing_to_json(saved_excel_file_path_str)
        
        update_exam_by_id(exam_id, writing_json_data)
        return exam_record
    except HTTPException as http_exc: 
        if conn: conn.rollback() 
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise http_exc 
    except psycopg2.Error as db_err:
        if conn: conn.rollback()
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Database error during exam creation from Excel: {db_err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error (Excel): {str(db_err)}")
    except ValueError as val_err: 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Excel parsing error: {val_err}")
        # delete_exam_data(exam_id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error parsing Excel file: {str(val_err)}")
    except Exception as e:
        if conn: conn.rollback()
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Unexpected error during exam creation from Excel: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred (Excel): {str(e)}")
    finally:
        if conn: conn.close()
        if excel_file: 
            try:
                await excel_file.close()
            except Exception: pass 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            try:
                os.remove(saved_excel_file_path_str)
            except Exception as e_remove:
                print(f"Error removing temp Excel file {saved_excel_file_path_str}: {e_remove}")

def get_writing_exam_by_id(exam_id: int) -> str:
    """
    Lấy dữ liệu đề thi writing từ CSDL và tái tạo lại cấu trúc JSON gốc.

    Args:
        exam_id (int): ID của bài thi (exam) cần lấy.

    Returns:
        str: Một chuỗi JSON đại diện cho đề thi. 
             Trả về một chuỗi JSON danh sách rỗng '[]' nếu không tìm thấy đề thi.
    """
    conn = None
    try:
        conn = get_db_connection()
        # RealDictCursor giúp làm việc với kết quả dưới dạng dictionary
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            # Lấy tất cả câu hỏi của exam, sắp xếp theo part và id
            # ORDER BY là mệnh đề cực kỳ quan trọng ở đây
            cur.execute("""
                SELECT id, part_id, topic, instruction, questions 
                FROM writing
                WHERE exam_id = %s
                ORDER BY part_id, id;
            """, (exam_id,))
            
            rows = cur.fetchall()
            
            if not rows:
                # Nếu không có câu hỏi nào, trả về danh sách JSON rỗng
                return "[]"

            # Dictionary để nhóm các câu hỏi theo part_id
            parts_data = {}

            # Lặp qua từng hàng kết quả để xây dựng lại cấu trúc JSON
            for row in rows:
                part_id = row['part_id']
                
                # Nếu đây là lần đầu tiên gặp part_id này, tạo khung cho nó
                if part_id not in parts_data:
                    parts_data[part_id] = {
                        "part_id": part_id,
                        "topic": row['topic'],
                        "instruction": row['instruction'],
                        "questions": [] # Khởi tạo danh sách câu hỏi rỗng
                    }
                
                # Thêm câu hỏi của hàng hiện tại vào danh sách của phần đó
                # Giả định cột chứa câu hỏi tên là 'questions' như trong migration
                parts_data[part_id]["questions"].append(row['questions'])

            # Chuyển đổi các giá trị của dictionary thành một danh sách
            final_result = list(parts_data.values())

            # Chuyển đổi danh sách Python thành chuỗi JSON đẹp mắt
            return final_result

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Lỗi khi lấy dữ liệu đề thi writing: {error}")
        raise error
    finally:
        if conn:
            conn.close()

def cleanup_orphaned_files():
    """
    Hàm duy nhất để thực hiện toàn bộ quá trình dọn dẹp file mồ côi.
    Hàm này được thiết kế để chạy tự động bởi một cron job.
    """
    logging.info("--- Bắt đầu phiên dọn dẹp file mồ côi ---")

    # Xác định các đường dẫn tuyệt đối
    raw_file_path = "/app/raw_file"

    # Định nghĩa các tác vụ dọn dẹp
    cleanup_tasks = [
        {
            "name": "Listening Audio",
            "directory": os.path.join(raw_file_path, 'audio'),
            "query": (
                "SELECT audio_path FROM listening_part_1 WHERE audio_path IS NOT NULL "
                "UNION ALL "
                "SELECT audio_path FROM listening_part_2 WHERE audio_path IS NOT NULL "
                "UNION ALL "
                "SELECT audio_path FROM listening_part_3 WHERE audio_path IS NOT NULL "
                "UNION ALL "
                "SELECT audio_path FROM listening_part_4 WHERE audio_path IS NOT NULL"
            )
        },
        {
            "name": "Speaking Images",
            "directory": os.path.join(raw_file_path, 'speaking', 'image'),
            "query": (
                "SELECT image_path1 FROM speaking WHERE image_path1 IS NOT NULL "
                "UNION ALL "
                "SELECT image_path2 FROM speaking WHERE image_path2 IS NOT NULL"
            )
        },
        {
            "name": "Speaking Instruction Audio",
            "directory": os.path.join(raw_file_path, 'speaking', 'instruction'),
            "query": "SELECT instruction_audio FROM speaking WHERE instruction_audio IS NOT NULL;"
        },
        {
            "name": "Speaking Submission",
            "directory": os.path.join(raw_file_path, 'speaking', 'submission'),
            "query": "SELECT answer_string FROM exam_submission;"
        }
    ]

    conn = None
    try:
        # Bước 1: Kết nối CSDL
        conn = get_db_connection()

        # Bước 2: Lặp qua từng tác vụ dọn dẹp
        for task in cleanup_tasks:
            logging.info(f"--- Bắt đầu xử lý tác vụ: {task['name']} ---")

            used_files = set()
            with conn.cursor() as cur:
                try:
                    cur.execute(task['query'])
                    rows = cur.fetchall()

                    if task['name'] == 'Speaking Submission':
                        # Phân tích JSON từ answer_string để lấy audioPaths
                        for row in rows:
                            try:
                                answer_string = row["answer_string"]
                                data = json.loads(answer_string or '{}')
                                for path in data.get('audioPaths', []):
                                    used_files.add(os.path.basename(path))
                            except json.JSONDecodeError:
                                logging.warning(f"Không đọc được JSON submission: {answer_string}")
                    else:
                        for row in rows:
                            item = dict(row)
                            if row[list(item)[0]]:
                                used_files.add(os.path.basename(row[list(item)[0]]))
                except psycopg2.Error as db_err:
                    logging.error(f"Lỗi truy vấn CSDL cho tác vụ '{task['name']}': {db_err}")
                    continue

            logging.info(
                f"Tìm thấy {len(used_files)} file hợp lệ trong CSDL cho tác vụ '{task['name']}'."
            )

            # 2b. Quét thư mục và xóa file mồ côi
            dir_path = task['directory']
            if not os.path.isdir(dir_path):
                logging.warning(f"Thư mục '{dir_path}' không tồn tại. Bỏ qua tác vụ.")
                continue

            files_on_disk = os.listdir(dir_path)
            files_on_disk_count = 0
            deleted_count = 0

            for filename in files_on_disk:
                full_path = os.path.join(dir_path, filename)
                if os.path.isfile(full_path):
                    files_on_disk_count += 1
                    if filename not in used_files:
                        try:
                            os.remove(full_path)
                            logging.info(f"Đã xóa file mồ côi: {full_path}")
                            deleted_count += 1
                        except OSError as os_err:
                            logging.error(f"Lỗi khi xóa file '{full_path}': {os_err}")

            logging.info(
                f"Hoàn thành tác vụ '{task['name']}'. Quét {files_on_disk_count} file, đã xóa {deleted_count} file."
            )

    except psycopg2.OperationalError as e:
        logging.critical(f"Lỗi nghiêm trọng: Không thể kết nối tới CSDL. {e}")
    except Exception as e:
        logging.error(
            f"Đã xảy ra lỗi không mong muốn trong quá trình dọn dẹp: {e}",
            exc_info=True
        )
    finally:
        if conn:
            conn.close()
        logging.info("--- Kết thúc phiên dọn dẹp file mồ côi ---\n")

def insert_g_v_exam(json_data, exam_id):
    # Kết nối database
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Đọc dữ liệu từ file JSON
    
    try:
        # Xử lý part1
        for item in json_data['part1']:
            cur.execute("""
                INSERT INTO g_v_part1
                (exam_id, question, correct_answer, opt1, opt2, opt3)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                exam_id,
                item['question'],
                item['correct_answer'],
                item['A'],
                item['B'],
                item['C']
            ))
        
        # Xử lý part2
        for group in json_data['part2']:
            # Tạo mapping cho options
            options = group['options']
            option_map = {
                'A': options.get('A', ''),
                'B': options.get('B', ''),
                'C': options.get('C', ''),
                'D': options.get('D', ''),
                'E': options.get('E', ''),
                'F': options.get('F', ''),
                'G': options.get('G', ''),
                'H': options.get('H', ''),
                'I': options.get('I', ''),
                'K': options.get('K', '')
            }
            
            for question in group['questions']:
                cur.execute("""
                    INSERT INTO g_v_part2 
                    (exam_id, group_id, topic, question, correct_answer,
                     opt1, opt2, opt3, opt4, opt5, 
                     opt6, opt7, opt8, opt9, opt10)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    exam_id,
                    int(group['group']),  # Chuyển thành integer
                    group['topic'],
                    question['question'],
                    question['correct_answer'],
                    option_map['A'],
                    option_map['B'],
                    option_map['C'],
                    option_map['D'],
                    option_map['E'],
                    option_map['F'],
                    option_map['G'],
                    option_map['H'],
                    option_map['I'],
                    option_map['K']
                ))
        
        conn.commit()
        print(f"✅ Đã nhập thành công dữ liệu cho exam_id {exam_id}")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Lỗi: {str(e)}")
    finally:
        cur.close()
        conn.close()
        

async def create_g_v_exam_from_excel( # Đổi tên từ _from_excel hoặc _from_pdf
    exam_set_id: int,
    exam_part_code: str,
    descriptions: str, # Tiêu đề chung cho phần Reading này
    time_limit_for_part: int,
    excel_file: Optional[UploadFile], # Đây là JSON đầy đủ {"part1": ..., "part2": ...}
    created_by_user_id: int,
    original_file_path: Optional[str] = None # Đường dẫn đến file gốc đã lưu (nếu có)
) -> dict:
    conn = None

    conn = get_db_connection() 
    # --- VALIDATE EXAM SET AND EXAM PART CODE (như cũ) ---
    with conn.cursor() as cur_validate:
        cur_validate.execute("SELECT id FROM exam_sets WHERE id = %s", (exam_set_id,))
        if not cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ExamSet with ID {exam_set_id} not found.")
        cur_validate.execute(
            "SELECT id FROM exams WHERE exam_code = %s AND examset_id = %s AND exam_type = %s ", (exam_part_code, exam_set_id, 'g_v')
        ) 
        if cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Speaking exam part with code '{exam_part_code}' already exists in ExamSet ID {exam_set_id}.")

    # --- Bắt đầu transaction chính ---
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO Exams (examset_id, exam_code, exam_type, description,  time_limit, created_by_user_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, exam_code, exam_type, description, time_limit, is_active;
            """,
            (exam_set_id, exam_part_code, "g_v", descriptions, 
                time_limit_for_part, created_by_user_id, True) 
        )
        exam_record = cur.fetchone()
        if not exam_record:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create exam record in database.")
        
        exam_id = exam_record['id']
        print(f"Created Exam (GV Part) record with ID: {exam_id} for ExamSet ID: {exam_set_id}")
        conn.commit()
    if not excel_file.filename or not excel_file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only Excel files (.xlsx, .xls) allowed.")
    saved_excel_file_path_str =  f"{GV_FILES_DIR}/{excel_file.filename}"
    print("📦 File exists:", os.path.exists(saved_excel_file_path_str))
    try:
        # ĐỌC NỘI DUNG FILE UPLOAD VÀ GHI
        file_content = await excel_file.read() # <<<< SỬA Ở ĐÂY: await read()
        with open(saved_excel_file_path_str, "wb") as file_object: # Mở ở chế độ "wb" (write bytes)
            file_object.write(file_content) # Ghi nội dung bytes
        print(f"Uploaded Excel file saved to: {saved_excel_file_path_str}")
    except Exception as e_save:
        # Nếu có lỗi khi lưu, xóa file nếu nó đã được tạo một phần (hiếm)
        if os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise HTTPException(status_code=500, detail=f"Could not save uploaded Excel file: {e_save}")
    finally:
        await excel_file.close() # Luôn đóng file upload
    try:
        g_v_json_data = aptis_g_v_to_json(saved_excel_file_path_str)
        
        insert_g_v_exam(g_v_json_data, exam_id)
        print(f"Successfully committed all parts from Excel for exam_id {exam_id}")
        return exam_record
    except HTTPException as http_exc: 
        if conn: conn.rollback() 
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise http_exc 
    except psycopg2.Error as db_err:
        if conn: conn.rollback()
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Database error during exam creation from Excel: {db_err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error (Excel): {str(db_err)}")
    except ValueError as val_err: 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Excel parsing error: {val_err}")
        delete_exam_data(exam_id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error parsing Excel file: {str(val_err)}")
    except Exception as e:
        if conn: conn.rollback()
        delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Unexpected error during exam creation from Excel: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred (Excel): {str(e)}")
    finally:
        if conn: conn.close()
        if excel_file: 
            try:
                await excel_file.close()
            except Exception: pass 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            try:
                os.remove(saved_excel_file_path_str)
            except Exception as e_remove:
                print(f"Error removing temp Excel file {saved_excel_file_path_str}: {e_remove}")
                
                
                
async def update_g_v_exam_from_excel( # Đổi tên từ _from_excel hoặc _from_pdf
    exam_id: int,
    excel_file: Optional[UploadFile], # Đây là JSON đầy đủ {"part1": ..., "part2": ...}
) -> dict:
    conn = None

    conn = get_db_connection() 
    # --- VALIDATE EXAM SET AND EXAM PART CODE (như cũ) ---
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur_validate:
        cur_validate.execute("SELECT id FROM exams WHERE id = %s", (exam_id,))
        if not cur_validate.fetchone():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exam with ID {exam_id} not found.")
    
    # --- Bắt đầu transaction chính ---
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """
            UPDATE Exams SET updated_at = now()
            WHERE id = %s
            RETURNING id, examset_id, exam_code, exam_type, description, time_limit, is_active;
            """,
            (exam_id,) 
        )
   
        exam_record = cur.fetchone()
        if not exam_record:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update exam record in database.")
        
        exam_id = exam_record['id']
        examset_id = exam_record['examset_id']
        print(f"UPDATE Exam (Writing Part) record with ID: {exam_id} for Exam ID: {examset_id}")
        conn.commit()
    if not excel_file.filename or not excel_file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only Excel files (.xlsx, .xls) allowed.")
    saved_excel_file_path_str =  f"{WRITING_FILE_DIR}/{excel_file.filename}"
    try:
        # ĐỌC NỘI DUNG FILE UPLOAD VÀ GHI
        file_content = await excel_file.read() # <<<< SỬA Ở ĐÂY: await read()
        with open(saved_excel_file_path_str, "wb") as file_object: # Mở ở chế độ "wb" (write bytes)
            file_object.write(file_content) # Ghi nội dung bytes
        print(f"Uploaded Excel file saved to: {saved_excel_file_path_str}")
        print("📦 File exists:", os.path.exists(saved_excel_file_path_str))
    except Exception as e_save:
        # Nếu có lỗi khi lưu, xóa file nếu nó đã được tạo một phần (hiếm)
        if os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise HTTPException(status_code=500, detail=f"Could not save uploaded Excel file: {e_save}")
    finally:
        await excel_file.close() # Luôn đóng file upload
    try:
        g_v_json_data = aptis_g_v_to_json(saved_excel_file_path_str)
        
        update_exam_by_id(exam_id, g_v_json_data)
        return exam_record
    except HTTPException as http_exc: 
        if conn: conn.rollback() 
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        raise http_exc 
    except psycopg2.Error as db_err:
        if conn: conn.rollback()
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Database error during exam creation from Excel: {db_err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error (Excel): {str(db_err)}")
    except ValueError as val_err: 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Excel parsing error: {val_err}")
        # delete_exam_data(exam_id)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error parsing Excel file: {str(val_err)}")
    except Exception as e:
        if conn: conn.rollback()
        # delete_exam_data(exam_id)
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            os.remove(saved_excel_file_path_str)
        print(f"Unexpected error during exam creation from Excel: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred (Excel): {str(e)}")
    finally:
        if conn: conn.close()
        if excel_file: 
            try:
                await excel_file.close()
            except Exception: pass 
        if saved_excel_file_path_str and os.path.exists(saved_excel_file_path_str):
            try:
                os.remove(saved_excel_file_path_str)
            except Exception as e_remove:
                print(f"Error removing temp Excel file {saved_excel_file_path_str}: {e_remove}")
                
                
                
def get_gv_exam_by_id(exam_id):
    # Kết nối database
    conn = get_db_connection()
    cur = conn.cursor()
    
    result = {"part1": [], "part2": []}
    
    try:
        # Lấy dữ liệu part1
        cur.execute("""
            SELECT question, correct_answer, opt1, opt2, opt3 
            FROM g_v_part1
            WHERE exam_id = %s
        """, (exam_id,))
        
        for row in cur.fetchall():
            result["part1"].append({
                "question": row["question"],
                "correct_answer": row["correct_answer"],
                "A": row["opt1"],
                "B": row["opt2"],
                "C": row["opt3"]
            })
        
        # Lấy dữ liệu part2
        # Bước 1: Lấy danh sách các group
        cur.execute("""
            SELECT DISTINCT group_id, topic 
            FROM g_v_part2
            WHERE exam_id = %s
            ORDER BY group_id
        """, (exam_id,))
        
        groups = []
        for row in cur.fetchall():
            groups.append({
                "group": row["group_id"],
                "topic": row["topic"],
                "questions": []
            })
        
        # Bước 2: Lấy options cho từng group (lấy từ bất kỳ bản ghi nào trong group)
        for group in groups:
            cur.execute("""
                SELECT opt1, opt2, opt3, opt4, opt5, 
                       opt6, opt7, opt8, opt9, opt10
                FROM g_v_part2
                WHERE exam_id = %s AND group_id = %s
                LIMIT 1
            """, (exam_id, group["group"]))
            
            options_row = cur.fetchone()
            if options_row:
                group["options"] = {
                    "A": options_row["opt1"],
                    "B": options_row["opt2"],
                    "C": options_row["opt3"],
                    "D": options_row["opt4"],
                    "E": options_row["opt5"],
                    "F": options_row["opt6"],
                    "G": options_row["opt7"],
                    "H": options_row["opt8"],
                    "I": options_row["opt9"],
                    "K": options_row["opt10"]
                }
            else:
                group["options"] = {}
        
        # Bước 3: Lấy câu hỏi cho từng group
        for group in groups:
            cur.execute("""
                SELECT question, correct_answer
                FROM g_v_part2
                WHERE exam_id = %s AND group_id = %s
                ORDER BY id
            """, (exam_id, group["group"]))
            
            for row in cur.fetchall():
                
                group["questions"].append({
                    "question": row["question"],
                    "correct_answer": row["correct_answer"]
                })
        
        result["part2"] = groups
        
        return result
        
    except Exception as e:
        print(f"❌ Lỗi khi lấy dữ liệu: {str(e)}")
        raise e
    finally:
        cur.close()
        conn.close()
        
        
def scoring_writing_exam_by_AI():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM exams WHERE exam_type = %s;", ("writing",))
    rows = cursor.fetchall()
    
    if not rows: 
        return None
    for row in rows:
        exam_id = row["id"]
        cursor.execute("SELECT id, exam_id, answer_string FROM exam_submission WHERE ai_reviewed = %s AND exam_id = %s AND is_scored = false;", (False, exam_id))
        row = cursor.fetchone()
        if not row:
            continue
        submission_id = row["id"]
        
        answer_string = json.loads(row["answer_string"])
        use_answers = answer_string["userAnswers"]
        writing_data = get_writing_exam_by_id(exam_id)
        ai_reviews = {}
        for part_id, part in enumerate(writing_data):
            instruction = part["instruction"]
            for question_id, question in enumerate(part["questions"]):
                key_user = f"w_p{part_id+1}_q{question_id+1}"
                user_answer = use_answers.get(key_user, None)
                if user_answer is not None:
                    ai_reviews[key_user] = generate_writing_review(instruction, question, user_answer)
        answer_string["ai_review"] = ai_reviews
        submission_data_string = json.dumps(answer_string, ensure_ascii=False)
        cursor.execute("UPDATE exam_submission SET answer_string = %s, ai_reviewed = %s WHERE id = %s", (submission_data_string, True, submission_id))
        conn.commit()
        conn.close()
        cursor.close()
        return None
    
def scoring_speaking_exam_by_AI():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM exams WHERE exam_type = %s;", ("speaking",))
    rows = cursor.fetchall()
    
    if not rows: 
        return None
    for row in rows:
        exam_id = row["id"]
        cursor.execute("SELECT id, exam_id, answer_string FROM exam_submission WHERE ai_reviewed = %s AND exam_id = %s AND is_scored = false;", (False, exam_id))
        row = cursor.fetchone()
        if not row:
            continue
        submission_id = row["id"]
        transcripts = []
        ai_reviews = []
        image_paths = []
        answer_string = json.loads(row["answer_string"])
        use_answers = answer_string["audioPaths"]
        speaking_data = get_speaking_exam_by_id(exam_id)
        for part_id, part in enumerate(speaking_data):
            instruction = part["instruction"]
            
            if part["image_url_1"]:
                if "http" in part["image_url_1"]:
                    download_drive_file(part["image_url_1"], output_path="image_url_1.jpg")
                    image_paths.append("image_url_1.jpg")
                else:
                    image_paths.append(part["image_url_1"])
                    
                    
            if part["image_url_2"]:
                if "http" in part["image_url_2"]:
                    download_drive_file(part["image_url_2"], output_path="image_url_2.jpg")
                    image_paths.append("image_url_2.jpg")
                else:
                    image_paths.append(part["image_url_2"])
                
            k = 0
            for answer_audio_path, question in zip(use_answers, part["question"]):
                transcript = transcript_text(answer_audio_path)
                if transcript is not None:
                    transcripts.append(transcript)
                    if k == 0:
                        ai_review = generate_speaking_correction_gemini(instruction, question["text"], transcript, image_paths)
                    else: 
                        ai_review = generate_speaking_correction_gemini(instruction, question["text"], transcript, [])
                    ai_reviews.append(ai_review)
                k += 1
                    
        answer_string["ai_review"] = ai_reviews
        answer_string["transcript"] = transcripts
        submission_data_string = json.dumps(answer_string, ensure_ascii=False)
        cursor.execute("UPDATE exam_submission SET answer_string = %s, ai_reviewed = %s WHERE id = %s", (submission_data_string, True, submission_id))
        conn.commit()
        conn.close()
        cursor.close()
        return None    

def generate_writing_suggestion(instruction, question, context):
    return generate_writing_suggestion_gemini(instruction, question, context)

def generate_speaking_suggestion(instruction, question, context, image_paths):
    return generate_speaking_suggestion_gemini(instruction, question, context, image_paths)


    
    
    
                
        
    
    
    