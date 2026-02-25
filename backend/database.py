from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = SQLAlchemy()

def init_app(app):
    # алаштування бази даних
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # ніціалізація 
    db.init_app(app)
    
    # Створення таблиць
    with app.app_context():
        db.create_all()
        print('✅ Database created successfully!')
