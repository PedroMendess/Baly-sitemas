from dataclasses import dataclass
@dataclass
class Usuario_Funcionario:
    email : str
    cpf  : int
    nome : str
    sobrenome : str
    password : str
    especialidade : str
    user_type: str