import json
import psycopg2
from psycopg2.extras import RealDictCursor
from app.helpers.common import get_env_var
from fastapi import HTTPException, status

DB_NAME     = get_env_var("DB", "POSTGRES_DB")
DB_USER     = get_env_var("DB", "POSTGRES_USER")
DB_PASSWORD = get_env_var("DB", "POSTGRES_PASSWORD")
DB_HOST     = "localhost"
DB_PORT     = get_env_var("DB", "DB_PORT")

def get_db_connection():
    try:
        return psycopg2.connect(
            dbname        = DB_NAME,
            user          = DB_USER,
            password      = DB_PASSWORD,
            host          = DB_HOST,
            port          = DB_PORT,
            cursor_factory= RealDictCursor
        )
    except psycopg2.OperationalError as e:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail      = f"Database unavailable: {e}"
        )

def get_listening_json_by_exam_id(exam_id: int) -> dict:
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


# Ví dụ sử dụng:
if __name__ == "__main__":
    data = get_listening_json_by_exam_id(1)
    print(json.dumps(data, ensure_ascii=False, indent=2))
