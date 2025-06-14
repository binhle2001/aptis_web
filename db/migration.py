import os
import psycopg2
from psycopg2 import sql, extras
from dotenv import load_dotenv
import time
from configparser import ConfigParser


def get_env_var(group, var_name): 
    config = ConfigParser()
    file_path = "app/.env"
    if os.path.exists(file_path):
        config.read(file_path)
        return  config[group][var_name]
    return os.environ.get(var_name)


DB_NAME = get_env_var("DB", "POSTGRES_DB")
DB_USER = get_env_var("DB", "POSTGRES_USER")
DB_PASSWORD = get_env_var("DB", "POSTGRES_PASSWORD")
DB_HOST = get_env_var("DB", "DB_HOST")
DB_PORT = get_env_var("DB", "DB_PORT")

def create_schema():
    conn = None
    for i in range(5): # Retry connection a few times
        try:
            print(f"Attempting to connect to database (attempt {i+1})...")
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            print("Successfully connected to the database.")
            break
        except psycopg2.OperationalError as e:
            print(f"Connection failed: {e}")
            if i < 4:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("Max connection attempts reached. Exiting.")
                return

    if not conn:
        return

    try:
        with conn.cursor() as cur:
            print("Creating ENUM types...")
            cur.execute("""
                DO $$ BEGIN
                    CREATE TYPE user_role_enum AS ENUM ('admin', 'member');
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;

                DO $$ BEGIN
                    CREATE TYPE exam_type_enum AS ENUM ('reading', 'listening');
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;

                DO $$ BEGIN
                    CREATE TYPE question_type_enum AS ENUM (
                        'MCQ_SINGLE',
                        'MCQ_MULTIPLE',
                        'FILL_IN_BLANK',
                        'ORDERING',
                        'MATCHING'
                        -- Add other Aptis specific question types as needed
                    );
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;

                DO $$ BEGIN
                    CREATE TYPE exam_attempt_status_enum AS ENUM (
                        'started',
                        'in_progress',
                        'submitted',
                        'auto_submitted',
                        'abandoned'
                    );
                EXCEPTION
                    WHEN duplicate_object THEN null;
                END $$;
            """)
            print("ENUM types created or already exist.")

            print("Creating function to auto-update updated_at columns...")
            cur.execute("""
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                   NEW.updated_at = NOW();
                   RETURN NEW;
                END;
                $$ language 'plpgsql';
            """)
            print("Function update_updated_at_column created or replaced.")


            print("Creating table: Users")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(255) NOT NULL,
                    phone_number VARCHAR(20),
                    role user_role_enum NOT NULL DEFAULT 'member',
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
                );
            """)
            cur.execute("""
                DROP TRIGGER IF EXISTS update_users_updated_at ON Users;
                CREATE TRIGGER update_users_updated_at
                BEFORE UPDATE ON Users
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();
            """)

            print("Creating table: Exams")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Exams (
                    exam_id SERIAL PRIMARY KEY,
                    exam_code VARCHAR(50) UNIQUE NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    exam_type exam_type_enum NOT NULL,
                    description TEXT,
                    time_limit_minutes INTEGER,
                    created_by_user_id INTEGER NOT NULL,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    CONSTRAINT fk_exams_created_by_user
                        FOREIGN KEY(created_by_user_id)
                        REFERENCES Users(user_id)
                        ON DELETE SET NULL ON UPDATE NO ACTION -- Or restrict, or handle in app logic
                );
            """)
            cur.execute("""
                DROP TRIGGER IF EXISTS update_exams_updated_at ON Exams;
                CREATE TRIGGER update_exams_updated_at
                BEFORE UPDATE ON Exams
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();
            """)

            print("Creating table: ExamParts")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS ExamParts (
                    part_id SERIAL PRIMARY KEY,
                    exam_id INTEGER NOT NULL,
                    part_number INTEGER NOT NULL,
                    part_title VARCHAR(255),
                    instructions TEXT,
                    part_audio_url VARCHAR(255),
                    CONSTRAINT fk_examparts_exam
                        FOREIGN KEY(exam_id)
                        REFERENCES Exams(exam_id)
                        ON DELETE CASCADE ON UPDATE CASCADE,
                    CONSTRAINT idx_exam_part_number_unique UNIQUE (exam_id, part_number)
                );
            """)

            print("Creating table: Questions")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Questions (
                    question_id SERIAL PRIMARY KEY,
                    part_id INTEGER NOT NULL,
                    question_sequence INTEGER NOT NULL,
                    question_text TEXT,
                    question_image_url VARCHAR(255),
                    question_audio_url VARCHAR(255),
                    question_type question_type_enum NOT NULL,
                    points INTEGER NOT NULL DEFAULT 1,
                    raw_data_from_word JSONB, -- Use JSONB for better indexing in PostgreSQL
                    CONSTRAINT fk_questions_part
                        FOREIGN KEY(part_id)
                        REFERENCES ExamParts(part_id)
                        ON DELETE CASCADE ON UPDATE CASCADE,
                    CONSTRAINT idx_part_question_sequence_unique UNIQUE (part_id, question_sequence)
                );
            """)

            print("Creating table: QuestionOptions")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS QuestionOptions (
                    option_id SERIAL PRIMARY KEY,
                    question_id INTEGER NOT NULL,
                    option_text TEXT NOT NULL,
                    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
                    display_order INTEGER DEFAULT 0,
                    CONSTRAINT fk_questionoptions_question
                        FOREIGN KEY(question_id)
                        REFERENCES Questions(question_id)
                        ON DELETE CASCADE ON UPDATE CASCADE
                );
            """)

            print("Creating table: CorrectAnswers")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS CorrectAnswers (
                    answer_id SERIAL PRIMARY KEY,
                    question_id INTEGER NOT NULL UNIQUE, -- Unique as per schema note
                    correct_text TEXT NOT NULL,
                    explanation TEXT,
                    CONSTRAINT fk_correctanswers_question
                        FOREIGN KEY(question_id)
                        REFERENCES Questions(question_id)
                        ON DELETE CASCADE ON UPDATE CASCADE
                );
            """)

            print("Creating table: ExamAttempts")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS ExamAttempts (
                    attempt_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    exam_id INTEGER NOT NULL,
                    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
                    end_time TIMESTAMP WITH TIME ZONE,
                    score DECIMAL(5,2),
                    score_details JSONB, -- Use JSONB
                    status exam_attempt_status_enum NOT NULL DEFAULT 'started',
                    submitted_at TIMESTAMP WITH TIME ZONE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    CONSTRAINT fk_examattempts_user
                        FOREIGN KEY(user_id)
                        REFERENCES Users(user_id)
                        ON DELETE CASCADE ON UPDATE NO ACTION, -- Cascade delete attempts if user is deleted
                    CONSTRAINT fk_examattempts_exam
                        FOREIGN KEY(exam_id)
                        REFERENCES Exams(exam_id)
                        ON DELETE NO ACTION ON UPDATE NO ACTION -- Prevent deleting exam if attempts exist
                );
            """)

            print("Creating table: UserAnswers")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS UserAnswers (
                    user_answer_id SERIAL PRIMARY KEY,
                    attempt_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    selected_option_id INTEGER, -- FK to QuestionOptions.option_id
                    answered_text TEXT,
                    is_correct BOOLEAN,
                    points_awarded DECIMAL(4,2) DEFAULT 0,
                    answered_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    CONSTRAINT fk_useranswers_attempt
                        FOREIGN KEY(attempt_id)
                        REFERENCES ExamAttempts(attempt_id)
                        ON DELETE CASCADE ON UPDATE CASCADE,
                    CONSTRAINT fk_useranswers_question
                        FOREIGN KEY(question_id)
                        REFERENCES Questions(question_id)
                        ON DELETE NO ACTION ON UPDATE NO ACTION, -- Prevent deleting question if answers exist
                    CONSTRAINT fk_useranswers_selected_option
                        FOREIGN KEY(selected_option_id)
                        REFERENCES QuestionOptions(option_id)
                        ON DELETE SET NULL ON UPDATE NO ACTION,
                    CONSTRAINT idx_attempt_question_unique UNIQUE (attempt_id, question_id)
                );
            """)
            

            # ... (sau khi tạo Users và các ENUMs) ...

            print("Creating table: ExamSets")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS ExamSets (
                    exam_set_id SERIAL PRIMARY KEY,
                    set_code VARCHAR(50) UNIQUE NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    overall_time_limit_minutes INTEGER,
                    created_by_user_id INTEGER NOT NULL,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
                    CONSTRAINT fk_examsets_created_by_user
                        FOREIGN KEY(created_by_user_id)
                        REFERENCES Users(user_id)
                        ON DELETE SET NULL ON UPDATE NO ACTION -- Hoặc RESTRICT
                );
            """)
            cur.execute("""
                DROP TRIGGER IF EXISTS update_examsets_updated_at ON ExamSets;
                CREATE TRIGGER update_examsets_updated_at
                BEFORE UPDATE ON ExamSets
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();
            """)

            print("Altering table: Exams (adding exam_set_id)")
            # Kiểm tra xem cột exam_set_id đã tồn tại chưa
            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM   information_schema.columns
                        WHERE  table_name = 'exams' -- tên bảng viết thường
                        AND    column_name = 'exam_set_id'
                    ) THEN
                        ALTER TABLE Exams ADD COLUMN exam_set_id INTEGER;
                        RAISE NOTICE 'Column exam_set_id added to Exams table.';

                        ALTER TABLE Exams
                        ADD CONSTRAINT fk_exams_exam_set
                            FOREIGN KEY(exam_set_id)
                            REFERENCES ExamSets(exam_set_id)
                            ON DELETE CASCADE ON UPDATE CASCADE; -- Hoặc SET NULL/RESTRICT tùy logic
                        RAISE NOTICE 'Foreign key fk_exams_exam_set added to Exams table.';
                    ELSE
                        RAISE NOTICE 'Column exam_set_id and/or FK already exists in Exams table.';
                    END IF;
                END
                $$;
            """)

            # ... (phần còn lại của migrate.py cho Exams, ExamParts, etc.) ...
            # Đảm bảo lệnh CREATE TABLE Exams không bị chạy lại và báo lỗi nếu bảng đã tồn tại với cột mới.
            # `CREATE TABLE IF NOT EXISTS Exams` vẫn ổn.
            print("Creating additional indexes...")
            # Example: Index for faster lookup of exams by type or creator
            cur.execute("CREATE INDEX IF NOT EXISTS idx_exams_exam_type ON Exams (exam_type);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_exams_created_by_user_id ON Exams (created_by_user_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_examattempts_user_id ON ExamAttempts (user_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_examattempts_exam_id ON ExamAttempts (exam_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_useranswers_question_id ON UserAnswers (question_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_questionoptions_question_id ON QuestionOptions (question_id);")


            conn.commit()
            print("Schema creation complete.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error during schema creation: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")
    
if __name__ == "__main__":
    create_schema()