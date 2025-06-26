import base64
import re
import shutil
from typing import Optional
from fastapi import HTTPException, UploadFile, status
import gdown
import psycopg2
import os
from psycopg2.extras import execute_values
import requests
from helpers.excel_parser import aptis_listening_to_json, aptis_reading_to_json
from services.auth_service import get_db_connection
READING_FILES_DIR = "/app/raw_file/reading"
LISTENING_FILES_DIR = "/app/raw_file/listening"
AUDIO_FILES_DIR = "/app/raw_file/audio"
os.makedirs(READING_FILES_DIR, exist_ok=True)
os.makedirs(LISTENING_FILES_DIR, exist_ok=True)
os.makedirs(AUDIO_FILES_DIR, exist_ok=True)
def insert_reading_part1_json(json_data, exam_id):
    """
    Chèn dữ liệu Part 1 Reading từ JSON vào bảng reading_part_1.
    
    :param json_data: Dữ liệu JSON đầu vào (danh sách các group và câu hỏi)
    :param exam_id: ID của bài thi
    :param db_config: dict chứa thông tin kết nối DB (dbname, user, password, host, port)
    """
    insert_query = """
        INSERT INTO reading_part_1 (exam_id, group_id, question, correct_answer, option1, option2, option3)
        VALUES %s
    """
    conn = get_db_connection()
    values = []
    for group in json_data:
        group_id = int(group["group"])
        for q in group["questions"]:
            question = q["sentence"]
            correct_answer = q["correct_answer"]
            # Đảm bảo có đủ 3 lựa chọn, nếu thiếu thì thêm chuỗi rỗng
            options = q["options"] + [""] * (3 - len(q["options"]))
            values.append((
                exam_id,
                group_id,
                question,
                correct_answer,
                options[0],
                options[1],
                options[2]
            ))

    try:
        
        cursor = conn.cursor()
        execute_values(cursor, insert_query, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Dữ liệu Part 4 đã được chèn thành công.")
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
            exam_id, group_id, topic, sentence_text, sentence_key, is_example_first
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
                sentence["is_example_first"]
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
            person_a, person_b, person_c, person_d
        )
        VALUES %s
    """

    # Mapping Person_A → A, Person_B → B, ...
    person_map = {
        "Person_A": "A",
        "Person_B": "B",
        "Person_C": "C",
        "Person_D": "D"
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
            correct_person = q["correct_answer"]
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
                person_d
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
            option5, option6, option7, option8
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
            correct_answer_letter = index_to_letter(correct_answer_index)

            values.append((
                exam_id,
                topic,
                paragraph,
                correct_answer_letter,
                *padded_options
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
            "listening_part_4"
            "speaking",
            "writing",
            "exam_submission",
            'exams'
        ]

        for table in tables[:-1]:
            cursor.execute(f"DELETE FROM {table} WHERE exam_id = %s", (exam_id,))

        # Xóa exam cuối cùng
        cursor.execute("DELETE FROM exams WHERE id = %s", (exam_id,))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Đã xóa toàn bộ dữ liệu của exam_id = {exam_id}")
    except Exception as e:
        print("❌ Lỗi khi xóa dữ liệu:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Reading exam part with code '{exam_id}' Error.")

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
        SELECT group_id, question, option1, option2, option3, correct_answer
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
            "options": [r["option1"], r["option2"], r["option3"]]
        })
    for grp, qs in sorted(part1_groups.items()):
        result["part1"].append({
            "group": grp,
            "questions": qs
        })

    # ===== Part 2 =====
    cur.execute("""
        SELECT group_id, topic, sentence_text, sentence_key, is_example_first
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
            "sentences": []
        })["sentences"].append({
            "key": float(r["sentence_key"]),
            "text": r["sentence_text"],
            "is_example_first": r["is_example_first"]
        })
    for grp in sorted(part2_groups):
        result["part2"].append(part2_groups[grp])

    # ===== Part 3 =====
    cur.execute("""
        SELECT group_id, topic,
                question_text, correct_answer,
                person_a, person_b, person_c, person_d
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
            "correct_answer": f"Person_{r['correct_answer']}"
        })
    for grp in sorted(part3_groups):
        result["part3"].append(part3_groups[grp])

    # ===== Part 4 =====
    cur.execute("""
        SELECT topic,
                option1, option2, option3, option4,
                option5, option6, option7, option8,
                paragraph, correct_answer
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
                "correct_answer": idx
            })
        result["part4"].append({
            "topic": rows[0]["topic"],
            "options": opts,
            "questions": questions
        })
    cur.close()
    conn.close()
    
    return result

def get_exam_by_id(exam_id):
    try:
        conn = get_db_connection() 
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT id, exam_type from exams WHERE id = %s", (exam_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Exam id {exam_id} not found")
        exam_type = row["exam_type"]
        if exam_type == "reading":
            return get_reading_exam_by_id(exam_id)
        else:
            return get_listening_exam_by_id(exam_id)
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
                (exam_id, question, audio_path, correct_answer, option1, option2, option3)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        for item in json_data:
            q       = item['question']
            link    = item['audio_link']
            ans     = int(item['correct_answer'])
            opt1, opt2, opt3 = item['options']
            cur.execute(insert_sql, (
                exam_id, q, link, ans, opt1, opt2, opt3
            ))
        conn.commit()
        


        
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
               option1, option2, option3, option4, option5, option6)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            opts = item.get('options', [])
            # unpack 6 options, nếu thiếu thì None
            o1,o2,o3,o4,o5,o6 = (opts + [None]*6)[:6]
            
            cur.execute(insert_sql, (
                exam_id, topic, link,
                a, b, c, d,
                o1, o2, o3, o4, o5, o6
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
              (exam_id, topic, question, correct_answer, audio_path)
            VALUES (%s, %s, %s, %s, %s)
        """
        for item in json_data:
            topic = item.get('topic')
            link  = item.get('audio_link')
            questions = item.get('questions', [])
            answers   = item.get('correct_answers', [])
            # mỗi item chứa 4 câu liên tiếp
            for q_text, ans in zip(questions, answers):
                cur.execute(insert_sql, (
                    exam_id,
                    topic,
                    q_text,
                    ans,
                    link
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
               option1, option2, option3)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        for item in json_data:
            topic = item.get('topic')
            link  = item.get('audio_link')
            questions = item.get('questions', [])
            answers   = item.get('correct_answers', [])
            opts_list = item.get('options', [])

            # Mỗi item chứa n câu (ở ví dụ là 2)
            for idx, (q_text, ans, opts) in enumerate(zip(questions, answers, opts_list), start=1):
                o1,o2,o3 = (opts + [None]*3)[:3]
                cur.execute(insert_sql, (
                    exam_id,
                    topic,
                    q_text,
                    int(ans),
                    link,
                    o1, o2, o3
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
                   ARRAY[option1, option2, option3] AS options
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
                   ARRAY[option1, option2, option3, option4, option5, option6] AS options
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
            })
        result['part2'] = part2

        # --- Part 3: chỉ tạo 1 block cho mỗi audio_link
        cur.execute("""
            SELECT topic,
                   question,
                   correct_answer,
                   audio_path AS audio_link
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
                "questions":       [r['question']        for r in rows3],
                "correct_answers": [r['correct_answer']  for r in rows3]
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
                   option1, option2, option3
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
                    "options":         []
                })
            # tìm block tương ứng
            blk = next(b for b in part4 if b['audio_link'] == link)
            blk['questions'].append(row['question'])
            blk['correct_answers'].append(row['correct_answer'])
            blk['options'].append([row['option1'], row['option2'], row['option3']])
        result['part4'] = part4

        return result

    finally:
        cur.close()
        conn.close()

def load_audio_as_base64(path_or_url: str) -> str:
    """
    Nếu path_or_url bắt đầu bằng http thì tải file về memory,
    ngược lại mở file local.
    Trả về base64-encoded string.
    """
    try:
        if path_or_url.lower().startswith("http"):
            download_url = _ensure_drive_url(path_or_url)
            path_or_url = "temp.mp3"
            gdown.download(download_url, output=path_or_url, quiet=False)
        with open(path_or_url, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except Exception as e:
        # Tùy nhu cầu, có thể raise hoặc trả về None
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
def _ensure_drive_url(url: str) -> str:
    m = re.search(r'/d/([^/]+)/', url)
    if m:
        return f"https://drive.google.com/uc?id={m.group(1)}"
    return url

# --- Main download function
def download_all_listening():
    conn = get_db_connection()
    cur  = conn.cursor()

    for part in range(1, 5):
        table = f"listening_part_{part}"
        cur.execute(f"SELECT id, exam_id, audio_path FROM {table} WHERE audio_path IS NOT NULL ORDER BY id")
        rows = cur.fetchall()
        for row in rows:
            rec_id, exam_id, path_in = row['id'], row['exam_id'],  row['audio_path']
            # Build download URL
            if path_in.lower().startswith('http'):
                download_url = _ensure_drive_url(path_in)
            else:
                download_url = None

            # Local file path
            ext = os.path.splitext(download_url or path_in)[1] or '.mp3'
            local_fname = f"{exam_id}_part{part}_{rec_id}.mp3"
            local_path  = f'/app/raw_file/audio/{local_fname}'

            # Download via gdown for HTTP URLs, skip local
            if download_url:
                try:
                    gdown.download(download_url, output=local_path, quiet=False)
                    print(f"Downloaded: {download_url} -> {local_path}")
                except Exception as e:
                    print(f"Failed to download {download_url}: {e}")
                cur.execute(f"""
                UPDATE {table}
                   SET audio_path = %s
                 WHERE id = %s
            """, (local_path, rec_id))
            else:
                # Non-HTTP, assume local path, check exist
                if not os.path.exists(path_in):
                    print(f"Missing local file: {path_in}")
                else:
                    print(f"Local file exists: {path_in}")

    conn.commit()
    cur.close()
    conn.close()

