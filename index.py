import os
import re
import psycopg2
import gdown

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import timedelta
from app.helpers.common import get_env_var
from fastapi import HTTPException, status


DB_NAME = get_env_var("DB", "POSTGRES_DB")
DB_USER = get_env_var("DB", "POSTGRES_USER")
DB_PASSWORD = get_env_var("DB", "POSTGRES_PASSWORD")
DB_HOST = "localhost"
DB_PORT = get_env_var("DB", "DB_PORT")


def get_db_connection():
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
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable."
        )
        
    
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
        
        # 2) Select lại các bản ghi mới insert
        cur.execute("""
            SELECT id, audio_path
              FROM listening_part_1
             WHERE exam_id = %s
        """, (exam_id,))
        rows = cur.fetchall()
        
        os.makedirs('raw_files/listening', exist_ok=True)
        
        for row in rows:
            # Skip non-http
            qid = row["id"]
            url = row["audio_path"]
            # Chuyển link Google Drive thành ID
            m = re.search(r'/d/([^/]+)/', url)
            if m:
                file_id = m.group(1)
                # gdown format: "https://drive.google.com/uc?id=<file_id>"
                download_url = f'https://drive.google.com/uc?id={file_id}'
                
            else:
                download_url = url
            
            # Tạo đường dẫn lưu
            # Gdown sẽ tự detect extension, nhưng ta mặc định .mp3
            local_fname = f"{exam_id}_part1_{qid}.mp3"
            local_path  = os.path.join('raw_files/listening', local_fname)
            
            # 3) Tải file bằng gdown
            # quiet=False để hiện progress, bạn có thể set True nếu không cần
            gdown.download(download_url, output=local_path, quiet=False)
            
            # 4) Cập nhật lại audio_path thành đường dẫn local
            cur.execute("""
                UPDATE listening_part_1
                   SET audio_path = %s
                 WHERE id = %s
            """, (local_path, qid))
        
        conn.commit()
        return "success"
    
    except Exception as e:
        conn.rollback()
        return f"error: {e}"
    
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

        # 2) Lấy lại các bản ghi cần download (chỉ những bản ghi có audio_path bắt đầu bằng http)
        cur.execute("""
            SELECT id, audio_path
              FROM listening_part_2
             WHERE exam_id = %s
               AND audio_path LIKE 'http%%'
        """, (exam_id,))
        records = cur.fetchall()

        os.makedirs('raw_files/listening', exist_ok=True)
        # 3) Download & cập nhật đường dẫn local
        for qid, url in records:
            
            # tách file_id từ link Drive
            m = re.search(r'/d/([^/]+)/', url)
            if m:
                file_id = m.group(1)
                download_url = f'https://drive.google.com/uc?id={file_id}'
            else:
                download_url = url

            # đặt tên file
            ext = '.mp3'
            local_fname = f"{exam_id}_part2_{qid}{ext}"
            local_path  = f'raw_files/listening/{local_fname}'
        
            
            gdown.download(download_url, output=local_path)
                
           


            # update đường dẫn trong DB
            cur.execute("""
                UPDATE listening_part_2
                   SET audio_path = %s
                 WHERE id = %s
            """, (local_path, qid))

        conn.commit()
        return "success"

    except Exception as e:
        conn.rollback()
        return f"error: {e}"

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

        # 2) Lấy lại id và audio_path ban đầu
        cur.execute("""
            SELECT id, audio_path
              FROM listening_part_3
             WHERE exam_id = %s
               AND audio_path LIKE 'http%%'
        """, (exam_id,))
        records = cur.fetchall()

        os.makedirs('raw_files/listening', exist_ok=True)

        # 3) Download & update đường dẫn local
        for row in records:
            qid, url = row["id"], row["audio_path"]
            # skip nếu url không phải link
            if not url.startswith('http'):
                continue
            m = re.search(r'/d/([^/]+)/', url)
            download_url = f'https://drive.google.com/uc?id={m.group(1)}' if m else url
            local_fname = f"{exam_id}_part3_{qid}.mp3"
            local_path  = f'raw_files/listening/{local_fname}'
            try:
                gdown.download(download_url, output=local_path, quiet=True)
            except Exception:
                continue
            if os.path.exists(local_path):
                cur.execute("""
                    UPDATE listening_part_3
                       SET audio_path = %s
                     WHERE id = %s
                """, (local_path, qid))
        conn.commit()
        return "success"

    except Exception as e:
        conn.rollback()
        return f"error: {e}"

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

        # 2) Lấy lại id và audio_path ban đầu
        cur.execute("""
            SELECT id, audio_path
              FROM listening_part_4
             WHERE exam_id = %s
               AND audio_path LIKE 'http%%'
        """, (exam_id,))
        records = cur.fetchall()

        os.makedirs('raw_files/listening', exist_ok=True)

        # 3) Download & update đường dẫn local\
        
        for row in records:
            
            qid, url = row["id"], row["audio_path"]
            # Skip non-http
            if not url.startswith('http'):
                continue
            # extract drive file ID
            m = re.search(r'/d/([^/]+)/', url)
            download_url = f'https://drive.google.com/uc?id={m.group(1)}' if m else url

            # đặt tên file, mặc định .mp3
            local_fname = f"{exam_id}_part4_{qid}.mp3"
            local_path = f'raw_files/listening/{local_fname}'

            try:
                gdown.download(download_url, output=local_path, quiet=True)
            except Exception as e:
                raise e

            if os.path.exists(local_path):
                cur.execute("""
                    UPDATE listening_part_4
                       SET audio_path = %s
                     WHERE id = %s
                """, (local_path, qid))
        conn.commit()
        return "success"

    except Exception as e:
        conn.rollback()
        return f"error: {e}"

    finally:
        cur.close()
        conn.close()
        
import json
with open("aptis_listening.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)
print(insert_listening_part4_json(json_data["part4"], 2))

