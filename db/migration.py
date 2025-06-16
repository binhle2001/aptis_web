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

# Danh sách câu lệnh tạo bảng
create_tables = [

    # Bảng users
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        fullname VARCHAR(100) NOT NULL,
        phone_number VARCHAR(20),
        role VARCHAR(20) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE NOT NULL,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
    """,

    # Bảng exam_sets
    """
    CREATE TABLE IF NOT EXISTS exam_sets (
        id SERIAL PRIMARY KEY,
        set_code VARCHAR(50) UNIQUE NOT NULL,
        title VARCHAR(200) NOT NULL,
        description TEXT,
        created_by_user_id INTEGER REFERENCES users(id) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE NOT NULL,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
    """,

    # Bảng exams
    """
    CREATE TABLE IF NOT EXISTS exams (
        id SERIAL PRIMARY KEY,
        examset_id INTEGER REFERENCES exam_sets(id) NOT NULL,
        exam_code VARCHAR(50) UNIQUE NOT NULL,
        exam_type VARCHAR(20) NOT NULL,
        description TEXT,
        time_limit INTEGER NOT NULL,
        created_by_user_id INTEGER REFERENCES users(id) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE NOT NULL,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
    """,

    # Reading Part 1
    """
    CREATE TABLE IF NOT EXISTS reading_part_1 (
        question_id SERIAL PRIMARY KEY,
        exam_id INTEGER REFERENCES exams(id) NOT NULL,
        group_id INTEGER NOT NULL,
        question TEXT NOT NULL,
        correct_answer VARCHAR(10) NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL
    );
    """,

    # Reading Part 2
    """
    CREATE TABLE IF NOT EXISTS reading_part_2 (
        question_id SERIAL PRIMARY KEY,
        exam_id INTEGER REFERENCES exams(id) NOT NULL,
        group_id INTEGER NOT NULL,
        topic TEXT,
        sentence_text TEXT NOT NULL,
        sentence_key INTEGER NOT NULL,
        is_example_first BOOLEAN DEFAULT FALSE
    );
    """,

    # Reading Part 3
    """
    CREATE TABLE IF NOT EXISTS reading_part_3 (
        question_id SERIAL PRIMARY KEY,
        exam_id INTEGER REFERENCES exams(id) NOT NULL,
        group_id INTEGER NOT NULL,
        topic TEXT,
        question_text TEXT NOT NULL,
        correct_answer VARCHAR(1) NOT NULL,
        person_a TEXT NOT NULL,
        person_b TEXT NOT NULL,
        person_c TEXT NOT NULL,
        person_d TEXT NOT NULL
    );
    """,

    # Reading Part 4
    """
    CREATE TABLE IF NOT EXISTS reading_part_4 (
        question_id SERIAL PRIMARY KEY,
        exam_id INTEGER REFERENCES exams(id) NOT NULL,
        topic TEXT,
        paragraph TEXT NOT NULL,
        correct_answer VARCHAR(1) NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        option5 TEXT NOT NULL,
        option6 TEXT NOT NULL,
        option7 TEXT NOT NULL,
        option8 TEXT NOT NULL
    );
    """,

    # Listening Part 1
    """
    CREATE TABLE IF NOT EXISTS listening_part_1 (
        id SERIAL PRIMARY KEY,
        exam_id INTEGER REFERENCES exams(id) NOT NULL,
        question TEXT NOT NULL,
        audio_path TEXT NOT NULL,
        correct_answer VARCHAR(10) NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL
    );
    """,

    # Listening Part 2
        """
    CREATE TABLE IF NOT EXISTS listening_part_2 (
        id SERIAL PRIMARY KEY,
        exam_id INTEGER REFERENCES exams(id) NOT NULL,
        topic TEXT,
        audio_path TEXT,
        a INTEGER CHECK (a BETWEEN 1 AND 6),
        b INTEGER CHECK (b BETWEEN 1 AND 6),
        c INTEGER CHECK (c BETWEEN 1 AND 6),
        d INTEGER CHECK (d BETWEEN 1 AND 6),
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        option5 TEXT NOT NULL,
        option6 TEXT NOT NULL
    );
    """
,

    # Listening Part 3
    """
    CREATE TABLE IF NOT EXISTS listening_part_3 (
        id SERIAL PRIMARY KEY,
        exam_id INTEGER REFERENCES exams(id) NOT NULL,
        topic TEXT,
        question TEXT,
        correct_answer VARCHAR(10) NOT NULL,
        audio_path TEXT
    );
    """,

    # Listening Part 4
    """
    CREATE TABLE IF NOT EXISTS listening_part_4 (
        id SERIAL PRIMARY KEY,
        exam_id INTEGER REFERENCES exams(id) NOT NULL,
        topic TEXT,
        question TEXT,
        correct_answer VARCHAR(10) NOT NULL,
        audio_path TEXT,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL
    );
    """
]

# Thực thi từng câu lệnh
for sql in create_tables:
    cur.execute(sql)

conn.commit()
cur.close()
conn.close()

print("✅ Đã tạo xong tất cả các bảng cho hệ thống luyện thi Aptis.")
