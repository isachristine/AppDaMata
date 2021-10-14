from flask import Flask, render_template
import os, datetime #manipulação de datas
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import defaultload #mapeamento dos objetos para modelo relacional

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))
# esse comando diz que queremos realmente trabalhar com sqlite

app = Flask('__name__')

app.config['SECRET_KEY'] = 'your secret key'
# professor vai explicar mais pra frente sobre isso

app.config["SQLALCHEMY_DATABSE_URI"] = database_file # definir o arquivo SQL
db = SQLAlchemy(app) # objeto do tipo SQL Alchemy, utilizado para seguir com as consultas


# criação da classe com os 4 atributos definidos na tabela "insumos"
class Insumos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    nome_insumo = db.Column(db.String(80), nullable=False)
    beneficios = db.Column(db.String(500), nullable=False)

@app.route('/')
# A função index vai ser chamada quando o servidor receber uma requisição
def index():
    conn = get_db_connection()
    Insumos = conn.execute('SELECT * FROM insumos').fetchall()
    conn.close()
#    insumos = Insumos.query.all()
    return render_template('index.html', insumos=Insumos)
