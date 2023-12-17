from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from typing import Optional

class Base(DeclarativeBase):
    pass

class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class Base(DeclarativeBase):
    pass

class Users (Base, BaseModel):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username:Mapped[str] = mapped_column(String(200), unique=True)
    password:Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    created_by: Mapped[str] = mapped_column(String(200), ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    updated_by: Mapped[str] = mapped_column(String(200), ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    unique_id:Mapped[str] = mapped_column(String(100), unique=True)
    first_name:Mapped[str] = mapped_column(String(100))
    middle_name:Mapped[Optional[str]] = mapped_column(String(100))
    last_name:Mapped[str] = mapped_column(String(100))
    date_of_birth:Mapped[datetime] = mapped_column(DateTime)
    phone_number:Mapped[Optional[str]] = mapped_column(String(100))
    address:Mapped[Optional[str]] = mapped_column(String(100))
    city:Mapped[Optional[str]] = mapped_column(String(100))
    state:Mapped[Optional[str]] = mapped_column(String(100))
    zip_code:Mapped[Optional[str]] = mapped_column(String(100))
    country:Mapped[Optional[str]] = mapped_column(String(100))
    email:Mapped[str] = mapped_column(String(100))
    role:Mapped[str] = mapped_column(String(200))

class courses(BaseModel, Base):
    __tablename__ = "courses"
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_id: Mapped[str] = mapped_column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    unique_id: Mapped[str] = mapped_column(String(64),unique=True)
    course_name: Mapped[str]= mapped_column(String(64))
    course_description: Mapped[str] = mapped_column(String(255))

class course_materials(BaseModel, Base):
    __tablename__ = "course_materials"
    material_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[str] = mapped_column(Integer, ForeignKey("courses.course_id", onupdate="CASCADE", ondelete="CASCADE"))
    course_title: Mapped[str]= mapped_column(String(64))
    course_type: Mapped[str]= mapped_column(String(64))
    course_content: Mapped[str] = mapped_column(String(255))
    unique_id: Mapped[str] = mapped_column(String(64),unique=True)
    upload_date:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

class enrollments(BaseModel, Base):
    __tablename__ = "enrollments"
    enrollment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[str] = mapped_column(Integer, ForeignKey("courses.course_id", onupdate="CASCADE", ondelete="CASCADE"))
    student_id: Mapped[str] = mapped_column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    unique_id: Mapped[str] = mapped_column(String(64),unique=True)
    enrollment_date:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

class student_progress(BaseModel, Base):
    __tablename__ = "student_progress"
    progress_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enrollment_id: Mapped[str] = mapped_column(Integer, ForeignKey("enrollments.enrollment_id", onupdate="CASCADE", ondelete="CASCADE"))
    student_id: Mapped[str] = mapped_column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    material_id: Mapped[str] = mapped_column(Integer, ForeignKey("course_materials.material_id", onupdate="CASCADE", ondelete="CASCADE"))
    unique_id: Mapped[str] = mapped_column(String(64),unique=True)
    completion_status:Mapped[str] = mapped_column(String(200))

class performance_reports(BaseModel, Base):
    __tablename__ = "performance_reports"
    report_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[str] = mapped_column(Integer, ForeignKey("courses.course_id", onupdate="CASCADE", ondelete="CASCADE"))
    student_id: Mapped[str] = mapped_column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"))
    unique_id: Mapped[str] = mapped_column(String(64),unique=True)
    date_generated:Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    performance_data: Mapped[str] = mapped_column(String(255))