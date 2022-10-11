from asyncio.windows_events import NULL
from tkinter import E
from flask import Flask, request
from flask_cors import CORS
from src.entidadesRelacionais import usuario
from src.entidadesRelacionais.usuario_funcionario import Usuario_Funcionario
from src.entidadesRelacionais.usuario import Usuario
from cerberus import Validator
from src.database.database import Database
from datetime import datetime
from typing import Union
from sqlalchemy import select

app = Flask(__name__)

app.config['database'] = Database(create_all=True)
CORS(app)

@app.route("/cadastro", methods = ['POST','GET'])
def cadastrar ():
    if request.method== 'POST':
        json = request.get_json()
        
        # Validador de json cerberus 
        schema = {
            'email': {'type': 'string', 'required': True},
            'telefone': {'type': 'string', 'required': True},
            'cpf': {'type': 'string', 'required': True},
            'nome': {'type': 'string', 'required': True},
            'sobrenome': {'type': 'string', 'required': True},
            'password': {'type': 'string', 'required': True},
            'dt_nasc': {'type': 'string', 'required': True},
            'user_type': {'type': 'string', 'required': True} 
        }
        validate = Validator(schema)
        
        # caso não tenha campo retorna error
        if( validate.validate(json) is not True):
            return validate.errors, 400
        
        # json usuario que irá ser passado para o banco
        usuario = Usuario(
            email = json.get('email'),
            telefone = json.get('telefone'),
            cpf = json.get('cpf'),
            nome = json.get('nome'),
            sobrenome = json.get('sobrenome'),
            password = json.get('password'),
            dt_nasc = json.get('dt_nasc'), #datetime.strptime(json.get('dt_nasc'),'%d%m%y')
            user_type = json.get('user_type')
        )
        cadastrarBanco(usuario)

        return 'usuario criado com sucesso.'

@app.route("/cadastroFuncionario", methods = ['POST'])
def cadastrar_Funcionario ():
    json = request.get_json()

    # Validador de json cerberus 
    schema = {
        'email': {'type': 'string', 'required': True},
        'nome': {'type': 'string', 'required': True},
        'password': {'type': 'string', 'required': True},
        'especialidade': {'type': 'string', 'required': True},
        'user_type': {'type': 'string', 'required': True}
    }
    validate = Validator(schema)
    
    # caso não tenha campo retorna error
    if( validate.validate(json) is not True):
        return validate.errors, 400
    
    # json funcionario que irá ser passado para o banco
    usuario_funcionario = Usuario_Funcionario(
        email = json.get('email'),
        nome = json.get('nome'),
        password = json.get('password'),
        especialidade = json.get('especialidade'),
        user_type = json.get('user_type')
    )
    cadastrarBanco(usuario_funcionario)

    return 'Funcionário criado com sucesso.'


def cadastrarBanco(usuario: Union[Usuario,Usuario_Funcionario]):
    # acrescentar o banco
    db: Database = app.config['database']
    dbSession = db.session_scoped()
    dbSession.add(usuario)
    dbSession.commit()
    db.session_scoped.remove()
        
@app.route("/login_Funcionario", methods = ['POST'])
def Login_Funcionario ():
        json = request.get_json()
        user_email = json.get('email')
        user_password = json.get('password')

        db: Database = app.config['database']
        dbSession = db.session_scoped()
       

        usuario_maluco = dbSession.query(dbSession.user_type).filter_by((dbSession.email == user_email) & (dbSession.password == user_password)).all()
        if usuario_maluco != NULL:
            return usuario_maluco
        else:
            return NULL    

        

app.run(debug=True)