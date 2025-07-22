import psycopg2

# Cấu hình kết nối
conn = psycopg2.connect(
    dbname="aptis_db",
    user="admin",
    password="qwerty",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# Danh sách câu lệnh ALTER TABLE để thêm cột
alter_table_queries = [
    """
    CREATE TABLE IF NOT EXISTS public."g_v_part1" (
    id SERIAL PRIMARY KEY,
    exam_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    opt1 TEXT,
    opt2 TEXT,
    opt3 TEXT
);
""",
"""
CREATE TABLE IF NOT EXISTS public."g_v_part2" (
    id SERIAL PRIMARY KEY,
    exam_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    topic TEXT NOT NULL,
    question TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    opt1 TEXT,
    opt2 TEXT,
    opt3 TEXT,
    opt4 TEXT,
    opt5 TEXT,
    opt6 TEXT,
    opt7 TEXT,
    opt8 TEXT,
    opt9 TEXT,
    opt10 TEXT
);
    """
]

# Thực thi từng câu lệnh
for sql in alter_table_queries:
    cur.execute(sql)

conn.commit()
cur.close()
conn.close()

print("✅ Đã thêm deviceid1, deviceid2 và is_commited vào bảng users.")
