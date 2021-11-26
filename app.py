from sqlite3.dbapi2 import ProgrammingError, connect
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


def get_receita(receita_nome): 
    #dado o ID da receita, ele fará uma pesquisa no BD
    conn = get_db_connection()
    receita = conn.execute('SELECT * FROM receitas WHERE nome_receita = ?', (receita_nome,)).fetchone()
    conn.close()
    if receita is None:
        abort(404)
    return receita 


project_dir = os.path.dirname(os.path.abspath(__file__)) #abre o database.db
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))
# esse comando diz que queremos realmente trabalhar com sqlite

app = Flask('__name__')

app.config['SECRET_KEY'] = 'your secret key'
# professor vai explicar mais pra frente sobre isso

app.config["SQLALCHEMY_DATABSE_URI"] = database_file # definir o arquivo SQL
db = SQLAlchemy(app)
db.init_app(app) # objeto do tipo SQL Alchemy, utilizado para seguir com as consultas

# criação da classe com os 4 atributos definidos na tabela "insumos"
class Insumos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    nome_insumo = db.Column(db.String(80), nullable=False)
    beneficios = db.Column(db.String(500), nullable=False)


# criação da classe com os 4 atributos definidos na tabela "insumos"
class Receitas(db.Model):
    # id2 = db.Column(db.Integer, primary_key=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    nome_receita = db.Column(db.String(80), nullable=False, primary_key=True)
    ingredientes = db.Column(db.String(500), nullable=False)
    passos = db.Column(db.String(500), nullable=False)


@app.route('/') # TELA PRINCIPAL
# A função index vai ser chamada quando o servidor receber uma requisição na raiz
# ao colocar o endereço da aplicação sem nenhum caminho após /, vai entrar nessa função.
def index():
    return render_template('homepage.html')


@app.route('/cadastrados')
def cadastrados():
    conn = get_db_connection() #conecta com o BD
    insumos = conn.execute('SELECT * FROM insumos').fetchall()
    conn.close()
    return render_template('index.html', insumos=insumos)


@app.route('/receitas')
def receitas():
    conn = get_db_connection() #conecta com o BD
    receitas = conn.execute('SELECT * FROM receitas').fetchall()
    conn.close()
    return render_template('index_receitas.html', receitas=receitas)



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
            return redirect(url_for('cadastrados'))

    return render_template('addinsumo.html')


@app.route('/addreceita', methods=('GET', 'POST'))
def addreceita():

    if request.method == 'POST':
        title = request.form['title']
        content1 = request.form['content1']
        content2 = request.form['content2']

        if not title:
            flash('Por favor, insira o nome da receita que deseja cadastrar!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO receitas (nome_receita, ingredientes, passos) VALUES (?, ?, ?)',
                    (title, content1, content2))
            conn.commit()
            conn.close()
            return redirect(url_for('receitas'))

    return render_template('addreceita.html')
 
      
@app.route('/<int:insumo_id>') #id do insumo é rota para consulta individual
def post(insumo_id):
    post = get_insumo(insumo_id)
    return render_template('insumos.html', post=post)


@app.route('/<string:receita_nome>') #id do insumo é rota para consulta individual
def post2(receita_nome):
    post2 = get_receita(receita_nome)
    return render_template('receitas.html', post2=post2)


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_insumo(id)

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
            return redirect(url_for('cadastrados'))

    return render_template('edit.html', post=post)


@app.route('/<string:receita_nome>/editreceita', methods=('GET', 'POST'))
def editreceita(receita_nome):
    post2 = get_receita(receita_nome)

    if request.method == 'POST':
        title = request.form['title']
        content1 = request.form['content1']
        content2 = request.form['content2']

        if not title:
            flash('Por favor, insira o nome da receita que deseja cadastrar!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE receitas SET ingredientes = ?, passos = ?'
            'WHERE nome_receita = ?', (content1, content2, title))
            conn.commit()
            conn.close()
            return redirect(url_for('receitas'))

    return render_template('edit_receita.html', post2=post2)

#@app.route('/<int:id>/delete', methods=('POST',))
#def deleteInsumo(id):
#    insumo = get_insumo(id)
#    conn = get_db_connection()
#    conn.execute('DELETE FROM insumos WHERE id = ?', (id,))
#    conn.commit()
#    conn.close()
#    flash('"{}" foi deletado com sucesso!'.format(insumo['nome_insumo']))
#    return redirect(url_for('index'))


