from flask import Flask, jsonify, request
from database import init_app, db
from models import Uroks, Teacher, Class, Student
from datetime import datetime

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

init_app(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'School Schedule System API',
        'status': 'active',
        'version': '1.0.0',
        'endpoints': {
            # Uroks endpoints
            'GET /api/uroks': 'тримати всі предмети',
            'GET /api/uroks/<id>': 'тримати предмет за ID',
            'POST /api/uroks': 'Створити новий предмет',
            'PUT /api/uroks/<id>': 'новити предмет',
            'DELETE /api/uroks/<id>': 'идалити предмет',
            
            # Teacher endpoints
            'GET /api/teachers': 'тримати всіх вчителів',
            'GET /api/teachers/<id>': 'тримати вчителя за ID',
            'POST /api/teachers': 'Створити нового вчителя',
            'PUT /api/teachers/<id>': 'новити вчителя',
            'DELETE /api/teachers/<id>': 'идалити вчителя',
            'GET /api/uroks/<uroks_id>/teachers': 'тримати вчителів за предметом',
            
            # Class endpoints
            'GET /api/classes': 'тримати всі класи',
            'GET /api/classes/<id>': 'тримати клас за ID',
            'POST /api/classes': 'Створити новий клас',
            'PUT /api/classes/<id>': 'новити клас',
            'DELETE /api/classes/<id>': 'идалити клас',
            'GET /api/teachers/<teacher_id>/classes': 'тримати класи класного керівника',
            
            # Student endpoints
            'GET /api/students': 'тримати всіх учнів',
            'GET /api/students/<id>': 'тримати учня за ID',
            'POST /api/students': 'Створити нового учня',
            'PUT /api/students/<id>': 'новити учня',
            'DELETE /api/students/<id>': 'идалити учня',
            'GET /api/classes/<class_id>/students': 'тримати учнів класу',
            'GET /api/students/active': 'тримати активних учнів',

            # ===== НОВІ ENDPOINTS =====
            # Schedule endpoints
                                        'GET /api/schedules': 'Отримати весь розклад',
            'GET /api/schedules/<id>': 'Отримати запис розкладу за ID',
            'POST /api/schedules': 'Створити новий запис в розкладі',
            'PUT /api/schedules/<id>': 'Оновити запис в розкладі',
            'DELETE /api/schedules/<id>': 'Видалити запис з розкладу',
            'GET /api/classes/<class_id>/schedules': 'Отримати розклад класу',
            'GET /api/teachers/<teacher_id>/schedules': 'Отримати розклад вчителя',

            # Grade endpoints
            'GET /api/grades': 'Отримати всі оцінки',
            'GET /api/grades/<id>': 'Отримати оцінку за ID',
            'POST /api/grades': 'Поставити оцінку',
            'PUT /api/grades/<id>': 'Оновити оцінку',
            'DELETE /api/grades/<id>': 'Видалити оцінку',
            'GET /api/students/<student_id>/grades': 'Отримати оцінки учня',
            'GET /api/classes/<class_id>/subjects/<uroks_id>/grades': 'Отримати оцінки класу з предмету'
        }
    })

# ============ CRUD для Uroks ============
@app.route('/api/uroks', methods=['GET'])
def get_all_uroks():
    try:
        uroks_list = Uroks.query.all()
        return jsonify({
            'status': 'success',
            'data': [uroks.to_dict() for uroks in uroks_list],
            'count': len(uroks_list)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/uroks/<int:id>', methods=['GET'])
def get_uroks(id):
    try:
        uroks = Uroks.query.get_or_404(id)
        return jsonify({
            'status': 'success',
            'data': uroks.to_dict()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'редмет не знайдено'}), 404

@app.route('/api/uroks', methods=['POST'])
def create_uroks():
    try:
        data = request.json
        
        if not data.get('name'):
            return jsonify({'status': 'error', 'message': 'азва предмету обов\'язкова'}), 400
        
        existing = Uroks.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'status': 'error', 'message': 'редмет з такою назвою вже існує'}), 400
        
        new_uroks = Uroks(
            name=data['name'],
            description=data.get('description', ''),
            hours=data.get('hours', 0)
        )
        
        db.session.add(new_uroks)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'редмет успішно створено',
            'data': new_uroks.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/uroks/<int:id>', methods=['PUT'])
def update_uroks(id):
    try:
        uroks = Uroks.query.get_or_404(id)
        data = request.json
        
        if 'name' in data:
            existing = Uroks.query.filter(Uroks.name == data['name'], Uroks.id != id).first()
            if existing:
                return jsonify({'status': 'error', 'message': 'редмет з такою назвою вже існує'}), 400
            uroks.name = data['name']
        
        if 'description' in data:
            uroks.description = data['description']
        
        if 'hours' in data:
            uroks.hours = data['hours']
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'редмет успішно оновлено',
            'data': uroks.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/uroks/<int:id>', methods=['DELETE'])
def delete_uroks(id):
    try:
        uroks = Uroks.query.get_or_404(id)
        db.session.delete(uroks)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'редмет успішно видалено'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============ CRUD для Teacher ============
@app.route('/api/teachers', methods=['GET'])
def get_all_teachers():
    try:
        teachers = Teacher.query.all()
        return jsonify({
            'status': 'success',
            'data': [teacher.to_dict() for teacher in teachers],
            'count': len(teachers)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/teachers/<int:id>', methods=['GET'])
def get_teacher(id):
    try:
        teacher = Teacher.query.get_or_404(id)
        return jsonify({
            'status': 'success',
            'data': teacher.to_dict()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'чителя не знайдено'}), 404

@app.route('/api/teachers', methods=['POST'])
def create_teacher():
    try:
        data = request.json
        
        required_fields = ['first_name', 'last_name', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'status': 'error', 'message': f'{field} є обов\'язковим полем'}), 400
        
        existing = Teacher.query.filter_by(email=data['email']).first()
        if existing:
            return jsonify({'status': 'error', 'message': 'читель з таким email вже існує'}), 400
        
        if data.get('uroks_id'):
            uroks = Uroks.query.get(data['uroks_id'])
            if not uroks:
                return jsonify({'status': 'error', 'message': 'редмет не знайдено'}), 404
        
        new_teacher = Teacher(
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data.get('middle_name'),
            email=data['email'],
            phone=data.get('phone'),
            address=data.get('address'),
            qualification=data.get('qualification'),
            experience_years=data.get('experience_years', 0),
            uroks_id=data.get('uroks_id')
        )
        
        db.session.add(new_teacher)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'чителя успішно створено',
            'data': new_teacher.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/teachers/<int:id>', methods=['PUT'])
def update_teacher(id):
    try:
        teacher = Teacher.query.get_or_404(id)
        data = request.json
        
        if 'first_name' in data:
            teacher.first_name = data['first_name']
        if 'last_name' in data:
            teacher.last_name = data['last_name']
        if 'middle_name' in data:
            teacher.middle_name = data['middle_name']
        if 'email' in data:
            existing = Teacher.query.filter(Teacher.email == data['email'], Teacher.id != id).first()
            if existing:
                return jsonify({'status': 'error', 'message': 'Email вже використовується'}), 400
            teacher.email = data['email']
        if 'phone' in data:
            teacher.phone = data['phone']
        if 'address' in data:
            teacher.address = data['address']
        if 'qualification' in data:
            teacher.qualification = data['qualification']
        if 'experience_years' in data:
            teacher.experience_years = data['experience_years']
        if 'uroks_id' in data:
            if data['uroks_id']:
                uroks = Uroks.query.get(data['uroks_id'])
                if not uroks:
                    return jsonify({'status': 'error', 'message': 'редмет не знайдено'}), 404
            teacher.uroks_id = data['uroks_id']
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'чителя успішно оновлено',
            'data': teacher.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/teachers/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    try:
        teacher = Teacher.query.get_or_404(id)
        db.session.delete(teacher)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'чителя успішно видалено'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/uroks/<int:uroks_id>/teachers', methods=['GET'])
def get_teachers_by_subject(uroks_id):
    try:
        uroks = Uroks.query.get_or_404(uroks_id)
        teachers = Teacher.query.filter_by(uroks_id=uroks_id).all()
        
        return jsonify({
            'status': 'success',
            'subject': uroks.name,
            'data': [teacher.to_dict() for teacher in teachers],
            'count': len(teachers)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============ CRUD для Class ============
@app.route('/api/classes', methods=['GET'])
def get_all_classes():
    try:
        classes = Class.query.all()
        return jsonify({
            'status': 'success',
            'data': [cls.to_dict() for cls in classes],
            'count': len(classes)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/classes/<int:id>', methods=['GET'])
def get_class(id):
    try:
        cls = Class.query.get_or_404(id)
        return jsonify({
            'status': 'success',
            'data': cls.to_dict()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'лас не знайдено'}), 404

@app.route('/api/classes', methods=['POST'])
def create_class():
    try:
        data = request.json
        
        required_fields = ['grade_level', 'letter', 'academic_year']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'status': 'error', 'message': f'{field} є обов\'язковим полем'}), 400
        
        grade_level = data['grade_level']
        letter = data['letter'].upper()
        class_name = f"{grade_level}-{letter}"
        
        existing = Class.query.filter_by(name=class_name).first()
        if existing:
            return jsonify({'status': 'error', 'message': f'лас {class_name} вже існує'}), 400
        
        if data.get('class_teacher_id'):
            teacher = Teacher.query.get(data['class_teacher_id'])
            if not teacher:
                return jsonify({'status': 'error', 'message': 'чителя не знайдено'}), 404
        
        new_class = Class(
            name=class_name,
            grade_level=grade_level,
            letter=letter,
            academic_year=data['academic_year'],
            room_number=data.get('room_number'),
            class_teacher_id=data.get('class_teacher_id'),
            capacity=data.get('capacity', 30)
        )
        
        db.session.add(new_class)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'лас {class_name} успішно створено',
            'data': new_class.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/classes/<int:id>', methods=['PUT'])
def update_class(id):
    try:
        cls = Class.query.get_or_404(id)
        data = request.json
        
        if 'grade_level' in data or 'letter' in data:
            grade_level = data.get('grade_level', cls.grade_level)
            letter = data.get('letter', cls.letter).upper()
            new_name = f"{grade_level}-{letter}"
            
            existing = Class.query.filter(Class.name == new_name, Class.id != id).first()
            if existing:
                return jsonify({'status': 'error', 'message': f'лас {new_name} вже існує'}), 400
            
            cls.name = new_name
            cls.grade_level = grade_level
            cls.letter = letter
        
        if 'academic_year' in data:
            cls.academic_year = data['academic_year']
        if 'room_number' in data:
            cls.room_number = data['room_number']
        if 'class_teacher_id' in data:
            if data['class_teacher_id']:
                teacher = Teacher.query.get(data['class_teacher_id'])
                if not teacher:
                    return jsonify({'status': 'error', 'message': 'чителя не знайдено'}), 404
            cls.class_teacher_id = data['class_teacher_id']
        if 'capacity' in data:
            if data['capacity'] < len(cls.students):
                return jsonify({'status': 'error', 'message': 'істкість не може бути меншою за кількість учнів'}), 400
            cls.capacity = data['capacity']
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'лас успішно оновлено',
            'data': cls.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/classes/<int:id>', methods=['DELETE'])
def delete_class(id):
    try:
        cls = Class.query.get_or_404(id)
        
        if len(cls.students) > 0:
            return jsonify({
                'status': 'error', 
                'message': f'еможливо видалити клас, в якому є {len(cls.students)} учнів'
            }), 400
        
        db.session.delete(cls)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'лас успішно видалено'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/teachers/<int:teacher_id>/classes', methods=['GET'])
def get_classes_by_teacher(teacher_id):
    try:
        teacher = Teacher.query.get_or_404(teacher_id)
        classes = Class.query.filter_by(class_teacher_id=teacher_id).all()
        
        return jsonify({
            'status': 'success',
            'teacher': teacher.get_full_name(),
            'data': [cls.to_dict() for cls in classes],
            'count': len(classes)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============ CRUD для Student ============

# тримати всіх учнів
@app.route('/api/students', methods=['GET'])
def get_all_students():
    try:
        students = Student.query.all()
        return jsonify({
            'status': 'success',
            'data': [student.to_dict() for student in students],
            'count': len(students)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# тримати учня за ID
@app.route('/api/students/<int:id>', methods=['GET'])
def get_student(id):
    try:
        student = Student.query.get_or_404(id)
        return jsonify({
            'status': 'success',
            'data': student.to_dict()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'чня не знайдено'}), 404

# тримати активних учнів
@app.route('/api/students/active', methods=['GET'])
def get_active_students():
    try:
        students = Student.query.filter_by(is_active=True).all()
        return jsonify({
            'status': 'success',
            'data': [student.to_dict() for student in students],
            'count': len(students)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Створити нового учня
@app.route('/api/students', methods=['POST'])
def create_student():
    try:
        data = request.json
        
        # алідація обов'язкових полів
        required_fields = ['first_name', 'last_name', 'date_of_birth', 'class_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'status': 'error', 'message': f'{field} є обов\'язковим полем'}), 400
        
        # еревірка існування класу
        class_obj = Class.query.get(data['class_id'])
        if not class_obj:
            return jsonify({'status': 'error', 'message': 'лас не знайдено'}), 404
        
        # еревірка місткості класу
        if len(class_obj.students) >= class_obj.capacity:
            return jsonify({
                'status': 'error', 
                'message': f'лас {class_obj.name} досяг максимальної місткості ({class_obj.capacity} учнів)'
            }), 400
        
        # онвертація дати
        try:
            date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        except:
            return jsonify({'status': 'error', 'message': 'еправильний формат дати. икористовуйте YYYY-MM-DD'}), 400
        
        # еревірка email (якщо вказано)
        if data.get('email'):
            existing = Student.query.filter_by(email=data['email']).first()
            if existing:
                return jsonify({'status': 'error', 'message': 'чень з таким email вже існує'}), 400
        
        new_student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data.get('middle_name'),
            date_of_birth=date_of_birth,
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            class_id=data['class_id'],
            enrollment_date=datetime.now().date(),
            is_active=data.get('is_active', True),
            parent_name=data.get('parent_name'),
            parent_phone=data.get('parent_phone'),
            medical_notes=data.get('medical_notes')
        )
        
        db.session.add(new_student)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'чня успішно створено',
            'data': new_student.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# новити учня
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    try:
        student = Student.query.get_or_404(id)
        data = request.json
        
        # новлюємо поля
        if 'first_name' in data:
            student.first_name = data['first_name']
        if 'last_name' in data:
            student.last_name = data['last_name']
        if 'middle_name' in data:
            student.middle_name = data['middle_name']
        if 'date_of_birth' in data:
            try:
                student.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            except:
                return jsonify({'status': 'error', 'message': 'еправильний формат дати'}), 400
        if 'email' in data:
            if data['email']:
                existing = Student.query.filter(Student.email == data['email'], Student.id != id).first()
                if existing:
                    return jsonify({'status': 'error', 'message': 'Email вже використовується'}), 400
            student.email = data['email']
        if 'phone' in data:
            student.phone = data['phone']
        if 'address' in data:
            student.address = data['address']
        if 'class_id' in data:
            class_obj = Class.query.get(data['class_id'])
            if not class_obj:
                return jsonify({'status': 'error', 'message': 'лас не знайдено'}), 404
            student.class_id = data['class_id']
        if 'is_active' in data:
            student.is_active = data['is_active']
        if 'parent_name' in data:
            student.parent_name = data['parent_name']
        if 'parent_phone' in data:
            student.parent_phone = data['parent_phone']
        if 'medical_notes' in data:
            student.medical_notes = data['medical_notes']
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'чня успішно оновлено',
            'data': student.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# идалити учня
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        student = Student.query.get_or_404(id)
        db.session.delete(student)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'чня успішно видалено'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# тримати учнів класу
@app.route('/api/classes/<int:class_id>/students', methods=['GET'])
def get_students_by_class(class_id):
    try:
        class_obj = Class.query.get_or_404(class_id)
        students = Student.query.filter_by(class_id=class_id).all()
        
        return jsonify({
            'status': 'success',
            'class': class_obj.name,
            'data': [student.to_dict() for student in students],
            'count': len(students),
            'capacity': class_obj.capacity,
            'available': class_obj.capacity - len(students)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
