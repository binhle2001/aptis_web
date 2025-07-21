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
    ALTER TABLE users
    ADD COLUMN IF NOT EXISTS deviceId1 VARCHAR;
    """,
    """
    ALTER TABLE users
    ADD COLUMN IF NOT EXISTS deviceId2 VARCHAR;
    """,
    """
    ALTER TABLE users
    ADD COLUMN IF NOT EXISTS is_commited BOOLEAN DEFAULT FALSE NOT NULL;
    """
]

# Thực thi từng câu lệnh
for sql in alter_table_queries:
    cur.execute(sql)

conn.commit()
cur.close()
conn.close()

print("✅ Đã thêm deviceid1, deviceid2 và is_commited vào bảng users.")
