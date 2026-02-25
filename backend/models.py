from database import db
from datetime import datetime

class Uroks(db.Model):
    __tablename__ = 'uroks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    hours = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    teachers = db.relationship('Teacher', backref='subject', lazy=True, cascade='all, delete-orphan')
    schedules = db.relationship('Schedule', backref='subject', lazy=True, cascade='all, delete-orphan')
    grades = db.relationship('Grade', backref='subject', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Uroks {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'hours': self.hours,
            'teachers_count': len(self.teachers),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    qualification = db.Column(db.String(100), nullable=True)
    experience_years = db.Column(db.Integer, default=0)
    
    uroks_id = db.Column(db.Integer, db.ForeignKey('uroks.id', ondelete='SET NULL'), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    schedules = db.relationship('Schedule', backref='teacher', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Teacher {self.last_name} {self.first_name}>'
    
    def get_full_name(self):
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return ' '.join(parts)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'full_name': self.get_full_name(),
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'qualification': self.qualification,
            'experience_years': self.experience_years,
            'uroks_id': self.uroks_id,
            'subject_name': self.subject.name if self.subject else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class Class(db.Model):
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    grade_level = db.Column(db.Integer, nullable=False)
    letter = db.Column(db.String(1), nullable=False)
    academic_year = db.Column(db.String(9), nullable=False)
    room_number = db.Column(db.String(10), nullable=True)
    class_teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='SET NULL'), nullable=True)
    capacity = db.Column(db.Integer, default=30)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    class_teacher = db.relationship('Teacher', foreign_keys=[class_teacher_id])
    students = db.relationship('Student', backref='class_ref', lazy=True, cascade='all, delete-orphan')
    schedules = db.relationship('Schedule', backref='class_ref', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Class {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'grade_level': self.grade_level,
            'letter': self.letter,
            'academic_year': self.academic_year,
            'room_number': self.room_number,
            'class_teacher_id': self.class_teacher_id,
            'class_teacher_name': self.class_teacher.get_full_name() if self.class_teacher else None,
            'capacity': self.capacity,
            'students_count': len(self.students),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)
    
    enrollment_date = db.Column(db.Date, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    parent_name = db.Column(db.String(100), nullable=True)
    parent_phone = db.Column(db.String(20), nullable=True)
    medical_notes = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    grades = db.relationship('Grade', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.last_name} {self.first_name}>'
    
    def get_full_name(self):
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return ' '.join(parts)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'full_name': self.get_full_name(),
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else None,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'class_id': self.class_id,
            'class_name': self.class_ref.name if self.class_ref else None,
            'enrollment_date': self.enrollment_date.strftime('%Y-%m-%d') if self.enrollment_date else None,
            'is_active': self.is_active,
            'parent_name': self.parent_name,
            'parent_phone': self.parent_phone,
            'medical_notes': self.medical_notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class Schedule(db.Model):
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    uroks_id = db.Column(db.Integer, db.ForeignKey('uroks.id', ondelete='CASCADE'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id', ondelete='CASCADE'), nullable=False)
    
    # ас проведення
    day_of_week = db.Column(db.Integer, nullable=False)  # 1-7 (понеділок-неділя)
    lesson_number = db.Column(db.Integer, nullable=False)  # 1-8 (номер уроку)
    start_time = db.Column(db.String(5), nullable=False)  # "08:30"
    end_time = db.Column(db.String(5), nullable=False)  # "09:15"
    
    # одаткова інформація
    room = db.Column(db.String(10), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    semester = db.Column(db.Integer, default=1)  # 1 або 2
    academic_year = db.Column(db.String(9), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Schedule {self.day_of_week}-{self.lesson_number}: {self.subject.name}>'
    
    def to_dict(self):
        days = ['', 'онеділок', 'івторок', 'Середа', 'етвер', 'ʼятниця', 'Субота', 'еділя']
        return {
            'id': self.id,
            'day_of_week': self.day_of_week,
            'day_name': days[self.day_of_week] if 1 <= self.day_of_week <= 7 else 'евідомо',
            'lesson_number': self.lesson_number,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'room': self.room,
            'is_active': self.is_active,
            'semester': self.semester,
            'academic_year': self.academic_year,
            
            # в'язки
            'uroks_id': self.uroks_id,
            'subject_name': self.subject.name if self.subject else None,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher.get_full_name() if self.teacher else None,
            'class_id': self.class_id,
            'class_name': self.class_ref.name if self.class_ref else None,
            
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class Grade(db.Model):
    __tablename__ = 'grades'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    uroks_id = db.Column(db.Integer, db.ForeignKey('uroks.id', ondelete='CASCADE'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='SET NULL'), nullable=True)
    
    # цінка
    value = db.Column(db.Float, nullable=False)  # 1-12 або 1-100
    grade_type = db.Column(db.String(20), nullable=False, default='regular')  # regular, exam, test, homework
    weight = db.Column(db.Float, default=1.0)  # вага оцінки (для середнього)
    
    # ата
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    semester = db.Column(db.Integer, default=1)
    
    # оментар
    comment = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Grade {self.value} for {self.student.get_full_name()}>'
    
    def to_dict(self):
        grade_types = {
            'regular': 'вичайна',
            'exam': 'кзамен',
            'test': 'онтрольна',
            'homework': 'омашнє завдання'
        }
        return {
            'id': self.id,
            'value': self.value,
            'grade_type': self.grade_type,
            'grade_type_ua': grade_types.get(self.grade_type, self.grade_type),
            'weight': self.weight,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'semester': self.semester,
            'comment': self.comment,
            
            # в'язки
            'student_id': self.student_id,
            'student_name': self.student.get_full_name() if self.student else None,
            'student_class': self.student.class_ref.name if self.student and self.student.class_ref else None,
            'uroks_id': self.uroks_id,
            'subject_name': self.subject.name if self.subject else None,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher.get_full_name() if self.teacher else None,
            
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
