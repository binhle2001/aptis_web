# aptis_migration.py
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
import enum

Base = declarative_base()

# Enum cho loại bài thi
class ExamType(enum.Enum):
    READING = 'reading'
    LISTENING = 'listening'

# Bảng Người dùng
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    fullname = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    role = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

# Bảng Bộ đề thi
class ExamSet(Base):
    __tablename__ = 'exam_sets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    set_code = Column(String(50), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    created_by_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    created_by = relationship('User', backref='exam_sets')

# Bảng Bài thi
class Exam(Base):
    __tablename__ = 'exams'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    examset_id = Column(Integer, ForeignKey('exam_sets.id'), nullable=False)
    exam_code = Column(String(50), unique=True, nullable=False)
    exam_type = Column(String(20), nullable=False)
    description = Column(Text, nullable=True)
    time_limit = Column(Integer, nullable=False)  # Thời gian làm bài (phút)
    created_by_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    exam_set = relationship('ExamSet', backref='exams')
    created_by = relationship('User', backref='exams')

# Bảng Reading Part 1
class ReadingPart1(Base):
    __tablename__ = 'reading_part_1'
    
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey('exams.id'), nullable=False)
    group_id = Column(Integer, nullable=False)  # 1 hoặc 2
    question = Column(Text, nullable=False)
    correct_answer = Column(String(10), nullable=False)
    option1 = Column(Text, nullable=False)
    option2 = Column(Text, nullable=False)
    option3 = Column(Text, nullable=False)
    
    exam = relationship('Exam', backref='reading_part_1_questions')

# Bảng Reading Part 2
class ReadingPart2(Base):
    __tablename__ = 'reading_part_2'
    
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey('exams.id'), nullable=False)
    group_id = Column(Integer, nullable=False)  # 1, 2, 3 hoặc 4
    topic = Column(Text, nullable=True)
    sentence_text = Column(Text, nullable=False)
    sentence_key = Column(Integer, nullable=False)
    is_example_first = Column(Boolean, default=False)
    
    exam = relationship('Exam', backref='reading_part_2_questions')

# Bảng Reading Part 3
class ReadingPart3(Base):
    __tablename__ = 'reading_part_3'
    
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey('exams.id'), nullable=False)
    group_id = Column(Integer, nullable=False)  # 1 hoặc 2
    topic = Column(Text, nullable=True)
    question_text = Column(Text, nullable=False)
    correct_answer = Column(String(1), nullable=False)  # A, B, C, D
    person_a = Column(Text, nullable=False)
    person_b = Column(Text, nullable=False)
    person_c = Column(Text, nullable=False)
    person_d = Column(Text, nullable=False)
    
    exam = relationship('Exam', backref='reading_part_3_questions')

# Bảng Reading Part 4
class ReadingPart4(Base):
    __tablename__ = 'reading_part_4'
    
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey('exams.id'), nullable=False)
    topic = Column(Text, nullable=True)
    paragraph = Column(Text, nullable=False)
    correct_answer = Column(String(1), nullable=False)  # A, B, C, D, E, F, G, H
    option1 = Column(Text, nullable=False)
    option2 = Column(Text, nullable=False)
    option3 = Column(Text, nullable=False)
    option4 = Column(Text, nullable=False)
    option5 = Column(Text, nullable=False)
    option6 = Column(Text, nullable=False)
    option7 = Column(Text, nullable=False)
    option8 = Column(Text, nullable=False)
    
    exam = relationship('Exam', backref='reading_part_4_questions')

# Kết nối database và tạo bảng
if __name__ == "__main__":
    # Thay đổi chuỗi kết nối theo database của bạn
    DATABASE_URL = "postgresql://admin:qwerty@localhost/aptis_db"
    # Hoặc dùng SQLite: "sqlite:///aptis.db"
    
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    
    print("✅ Đã tạo xong các bảng cho phần Reading!")