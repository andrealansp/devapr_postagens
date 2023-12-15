from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
db:SQLAlchemy

class Postagem(db.Model):
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)
    id_autor = db.Column(db.Integer,db.ForeignKey('autor.id_autor'))
    
    
class Autor(db.Model):
    __tablename__ = 'autor'
    
    id_autor = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    postagens = db.relationship('Postagem')

def inicializar_banco():
    with app.app_context():
        db.drop_all()
        db.create_all()
        autor = Autor(nome='andre', email="andrealansp@hotmail.com", senha="adm123", admin=True)
        db.session.add(autor)
        db.session.commit()
    

if __name__ == '__main__':
    inicializar_banco()