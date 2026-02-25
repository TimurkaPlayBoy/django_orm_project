from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'School Schedule System API',
        'status': 'active',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    app.run(debug=True)
