from flask import Flask, request
from flask_cors import CORS
from src.entidadesRelacionais.usuario import Usuario
from cerberus import Validator
from src.database.database import Database
from datetime import datetime

app = Flask(__name__)

app.config['database'] = Database(create_all=True)
CORS(app)

@app.route("/cadastro", methods = ['POST'])
def cadastrar ():
    json = request.get_json()

    # Validador de json cerberus 
    schema = {
        'email': {'type': 'string', 'required': True},
        'telefone': {'type': 'string', 'required': True},
        'cpf': {'type': 'string', 'required': True},
        'nome': {'type': 'string', 'required': True},
        'sobrenome': {'type': 'string', 'required': True},
        'password': {'type': 'string', 'required': True},
        'dt_nasc': {'type': 'string', 'required': True}
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
        dt_nasc = json.get('dt_nasc') #datetime.strptime(json.get('dt_nasc'),'%d%m%y')
    )
    cadastrarBanco(usuario)

    return 'usuario criado com sucesso.'


def cadastrarBanco(usuario: Usuario):
    # acrescentar o banco
    db: Database = app.config['database']
    dbSession = db.session_scoped()
    dbSession.add(usuario)
    dbSession.commit()
    db.session_scoped.remove()
        

app.run(debug=True)