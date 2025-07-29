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
    ALTER TABLE exam_submission
    ADD COLUMN IF NOT EXISTS ai_reviewed BOOLEAN default false;
    """,
    """
    ALTER TABLE listening_part_1
    ADD COLUMN IF NOT EXISTS transcript VARCHAR;
    """,
    """
    ALTER TABLE listening_part_1
    ADD COLUMN IF NOT EXISTS explain VARCHAR;
    """,
    """
    ALTER TABLE listening_part_2
    ADD COLUMN IF NOT EXISTS transcript VARCHAR;
    """,
    """
    ALTER TABLE listening_part_2
    ADD COLUMN IF NOT EXISTS explain VARCHAR;
    """,
    """
    ALTER TABLE listening_part_3
    ADD COLUMN IF NOT EXISTS transcript VARCHAR;
    """,
    """
    ALTER TABLE listening_part_3
    ADD COLUMN IF NOT EXISTS explain VARCHAR;
    """,
    """
    ALTER TABLE listening_part_4
    ADD COLUMN IF NOT EXISTS explain VARCHAR;
    """,
    """
    ALTER TABLE listening_part_4
    ADD COLUMN IF NOT EXISTS transcript VARCHAR;
    """,
    """
    ALTER TABLE reading_part_1
    ADD COLUMN IF NOT EXISTS explain VARCHAR;
    """,
    """
    ALTER TABLE reading_part_2
    ADD COLUMN IF NOT EXISTS explain VARCHAR;
    """,
    """
    ALTER TABLE reading_part_3
    ADD COLUMN IF NOT EXISTS explain VARCHAR;
    """,
    """
    ALTER TABLE reading_part_4
    ADD COLUMN IF NOT EXISTS explain VARCHAR;
    """,
]

# Thực thi từng câu lệnh
for sql in alter_table_queries:
    cur.execute(sql)

conn.commit()
cur.close()
conn.close()

print("✅ Đã thêm deviceid1, deviceid2 và is_commited vào bảng users.")
