from flask import Flask, jsonify, request
from database import init_app, db
from models import Uroks

app = Flask(__name__)
init_app(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'School Schedule System API',
        'status': 'active',
        'version': '1.0.0',
        'endpoints': {
            'GET /api/uroks': 'тримати всі предмети',
            'GET /api/uroks/<id>': 'тримати предмет за ID',
            'POST /api/uroks': 'Створити новий предмет',
            'PUT /api/uroks/<id>': 'новити предмет',
            'DELETE /api/uroks/<id>': 'идалити предмет'
        }
    })

# ============ CRUD для Uroks ============

# тримати всі предмети
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

# тримати предмет за ID
@app.route('/api/uroks/<int:id>', methods=['GET'])
def get_uroks(id):
    try:
        uroks = Uroks.query.get_or_404(id)
        return jsonify({
            'status': 'success',
            'data': uroks.to_dict()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Uroks not found'}), 404

# Створити новий предмет
@app.route('/api/uroks', methods=['POST'])
def create_uroks():
    try:
        data = request.json
        
        # алідація
        if not data.get('name'):
            return jsonify({'status': 'error', 'message': 'Name is required'}), 400
        
        # еревірка чи існує вже такий предмет
        existing = Uroks.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'status': 'error', 'message': 'Uroks with this name already exists'}), 400
        
        new_uroks = Uroks(
            name=data['name'],
            description=data.get('description', ''),
            hours=data.get('hours', 0)
        )
        
        db.session.add(new_uroks)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Uroks created successfully',
            'data': new_uroks.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# новити предмет
@app.route('/api/uroks/<int:id>', methods=['PUT'])
def update_uroks(id):
    try:
        uroks = Uroks.query.get_or_404(id)
        data = request.json
        
        # новлюємо поля
        if 'name' in data:
            # еревірка чи нове ім'я не зайняте
            existing = Uroks.query.filter(Uroks.name == data['name'], Uroks.id != id).first()
            if existing:
                return jsonify({'status': 'error', 'message': 'Uroks with this name already exists'}), 400
            uroks.name = data['name']
        
        if 'description' in data:
            uroks.description = data['description']
        
        if 'hours' in data:
            uroks.hours = data['hours']
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Uroks updated successfully',
            'data': uroks.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

# идалити предмет
@app.route('/api/uroks/<int:id>', methods=['DELETE'])
def delete_uroks(id):
    try:
        uroks = Uroks.query.get_or_404(id)
        db.session.delete(uroks)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Uroks deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
