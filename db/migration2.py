# migration_2.py
# Bổ sung các bảng guests, speaking, writing, và exam_submissions

import psycopg2

# --- Cấu hình kết nối ---
# (Đảm bảo các thông tin này khớp với môi trường của bạn)
conn = psycopg2.connect(
    dbname="aptis_db",
    user="admin",
    password="qwerty",
    host="localhost",
    port=5432
)
cur = conn.cursor()
print("🚀 Kết nối tới CSDL aptis_db thành công.")

# --- Danh sách các câu lệnh SQL để bổ sung bảng ---
add_new_tables = [

    # Bảng guests: Lưu thông tin khách vãng lai làm bài thi thử
    """
    CREATE TABLE IF NOT EXISTS guests (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(255) NOT NULL,
        phone_number VARCHAR(20) NOT NULL,
        is_called BOOLEAN DEFAULT FALSE NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """,

    # Bảng speaking: Chứa câu hỏi cho phần thi Speaking
    # Bảng này được đổi tên từ 'speaking_questions' để ngắn gọn hơn
    """
    CREATE TABLE IF NOT EXISTS speaking (
        id SERIAL PRIMARY KEY,
        exam_id INTEGER REFERENCES exams(id) ON DELETE CASCADE NOT NULL,
        part_id INTEGER NOT NULL,
        topic VARCHAR(255),
        instruction TEXT,
        question TEXT NOT NULL,
        image_path VARCHAR(255)
    );
    """,

    # Bảng writing: Chứa câu hỏi cho phần thi Writing
    # Bảng này được đổi tên từ 'writing_questions' để ngắn gọn hơn
    """
    CREATE TABLE IF NOT EXISTS writing (
        id SERIAL PRIMARY KEY,
        exam_id INTEGER REFERENCES exams(id) ON DELETE CASCADE NOT NULL,
        part_id INTEGER NOT NULL,
        topic VARCHAR(255),
        instruction TEXT,
        questions TEXT NOT NULL
    );
    """,

    # Bảng exam_submissions: Lưu trữ bài làm của người dùng đã đăng ký
    # Không có guest_id vì không lưu lịch sử của khách.
    # user_id có thể là NULL để xử lý bài nộp của khách, nhưng sẽ không được liên kết.
    """
    CREATE TABLE IF NOT EXISTS exam_submissions (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
        exam_id INTEGER REFERENCES exams(id) ON DELETE CASCADE NOT NULL,
        score FLOAT DEFAULT NULL,
        answer_string TEXT NOT NULL,
        is_scored BOOLEAN DEFAULT FALSE NOT NULL,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
    """
]

# --- Thực thi các câu lệnh SQL ---
try:
    print("⏳ Bắt đầu thực thi migration 2...")
    for sql_command in add_new_tables:
        cur.execute(sql_command)
        print(f"   -> Đã thực thi lệnh cho bảng: {sql_command.split(' ')[5]}")

    conn.commit()
    print("\n✅ Migration 2: Đã bổ sung thành công các bảng guests, speaking, writing, và exam_submissions.")

except psycopg2.Error as e:
    print(f"❌ Đã xảy ra lỗi: {e}")
    conn.rollback() # Hoàn tác các thay đổi nếu có lỗi

finally:
    # --- Đóng kết nối ---
    if cur:
        cur.close()
    if conn:
        conn.close()
    print("🔚 Đã đóng kết nối CSDL.")