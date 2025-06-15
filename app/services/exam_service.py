import shutil
from typing import Optional
from fastapi import HTTPException, UploadFile, status
import psycopg2
import os
from psycopg2.extras import execute_values
from app.helpers.excel_parser import aptis_reading_to_json
from app.services.auth_service import get_db_connection
READING_FILES_DIR = "raw_file/reading"
os.makedirs(READING_FILES_DIR, exist_ok=True)

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

        # Thứ tự xóa: bảng phụ → bảng chính (foreign key)
        tables = [
            'reading_part_1',
            'reading_part_2',
            'reading_part_3',
            'reading_part_4',
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
            ORDER BY group_id, sentence_key
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


def get_listening_exam_by_id(exam_id):
    pass

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
            print("ngungungungu")
            part1 = json_content["part1"]
            part2 = json_content["part2"]
            part3 = json_content["part3"]
            part4 = json_content["part4"]
            insert_reading_part1_json(part1, exam_id)
            insert_reading_part2_json(part2, exam_id)
            insert_reading_part3_json(part3, exam_id)
            insert_reading_part4_json(part4, exam_id)  
            return get_reading_exam_by_id(exam_id)
        
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
            
        