from sqlite3.dbapi2 import connect
from flask import Flask, render_template, request, url_for, flash, redirect
import os, datetime #manipulação de datas
import sqlite3
from flask_sqlalchemy import SQLAlchemy #serve para fazer o mapeamento dos objetos para o modelo relacional
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_insumo(insumo_id): 
    #dado o ID do insumo, ele fará uma pesquisa no BD
    conn = get_db_connection()
    insumo = conn.execute('SELECT * FROM insumos WHERE id = ?', (insumo_id,)).fetchone()
    conn.close()
    if insumo is None:
        abort(404)
    return insumo #se não for insumo aqui, no insumos.html não vai retornar o individual


project_dir = os.path.dirname(os.path.abspath(__file__)) #abre o database.db
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

@app.route('/') # TELA PRINCIPAL
# A função index vai ser chamada quando o servidor receber uma requisição na raiz
# ao colocar o endereço da aplicação sem nenhum caminho após /, vai entrar nessa função.
def index():
    conn = get_db_connection() #conecta com o BD
    insumos = conn.execute('SELECT * FROM insumos').fetchall()
    conn.close()
    return render_template('index.html', insumos=insumos)


@app.route('/addinsumo', methods=('GET', 'POST'))
def addinsumo():

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Por favor, insira o nome do insumo que deseja cadastrar!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO insumos (nome_insumo, beneficios) VALUES (?, ?)',
                    (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('addinsumo.html')
  
      
@app.route('/<int:insumo_id>') #id do insumo é rota para consulta individual
def post(insumo_id):
    post = get_insumo(insumo_id)
    return render_template('insumos.html', post=post)


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    insumo = get_insumo(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Por favor, insira o nome do insumo que deseja cadastrar!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE insumos SET nome_insumo = ?, beneficios = ?'
            'WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', insumo=insumo)


#@app.route('/<int:id>/delete', methods=('POST',))
#def deleteInsumo(id):
#    insumo = get_insumo(id)
#    conn = get_db_connection()
#    conn.execute('DELETE FROM insumos WHERE id = ?', (id,))
#    conn.commit()
#    conn.close()
#    flash('"{}" foi deletado com sucesso!'.format(insumo['nome_insumo']))
#    return redirect(url_for('index'))


