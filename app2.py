from flask import Flask, request
from flask_cors import CORS
from src.entidadesRelacionais.usuario_funcionario import Usuario_Funcionario
from cerberus import Validator
from src.database.database import Database
from datetime import datetime

app = Flask(__name__)

app.config['database'] = Database(create_all=True)
CORS(app)

@app.route("/cadastroFuncionario", methods = ['POST'])
def cadastrar ():
    json = request.get_json()

    # Validador de json cerberus 
    schema = {
        'email': {'type': 'string', 'required': True},
        'cpf': {'type': 'string', 'required': True},
        'nome': {'type': 'string', 'required': True},
        'sobrenome': {'type': 'string', 'required': True},
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
        cpf = json.get('cpf'),
        nome = json.get('nome'),
        sobrenome = json.get('sobrenome'),
        password = json.get('password'),
        especialidade = json.get('especialidade'),
        user_type = json.get('user_type')
    )
    cadastrarBanco(usuario_funcionario)

    return 'Funcionário criado com sucesso.'


def cadastrarBanco(usuario_funcionario: Usuario_Funcionario):
    # acrescentar o banco
    db: Database = app.config['database']
    dbSession = db.session_scoped()
    dbSession.add(usuario_funcionario)
    dbSession.commit()
    db.session_scoped.remove()
        

app.run(debug=True)