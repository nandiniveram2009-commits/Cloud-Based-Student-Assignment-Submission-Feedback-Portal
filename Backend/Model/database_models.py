from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from services.cloud_db import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False) # 'student', 'teacher', 'admin'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_name = Column(String(150), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Assignment(Base):
    __tablename__ = "assignments"
    assignment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime(timezone=True), nullable=False)
    max_marks = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Submission(Base):
    __tablename__ = "submissions"
    submission_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_url = Column(Text, nullable=False)
    storage_path = Column(Text, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    submission_status = Column(String(30), default="SUBMITTED") # SUBMITTED, LATE, GRADED
    marks = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    graded_at = Column(DateTime(timezone=True), nullable=True)
