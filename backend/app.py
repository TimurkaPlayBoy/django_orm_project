from flask import Flask, jsonify, request
from database import init_app, db
from models import Uroks, Teacher
import json

app = Flask(__name__)

# алаштовуємо JSON кодування для підтримки української мови
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
            'GET /api/uroks/<uroks_id>/teachers': 'тримати вчителів за предметом'
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

if __name__ == '__main__':
    app.run(debug=True)
