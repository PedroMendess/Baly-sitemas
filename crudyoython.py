import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='220201',
    database= 'baly sistema',
)
cursor = conexao.cursor()

#Crud
nome_produto = "pedro"
valor = 3
comando = f'INSERT INTO teste (nome_produto, ) VALUES ("{nome_produto}",{valor})'
cursor.execute(comando)





cursor.close()
conexao.close()

#Create
#Nome_produto = "todynho"
#valor = 3
#comando = f'INSERT INTO cliented (Nome_produto, valor) VALUES ("{Nome_produto}",{valor})'
#cursor.execute(comando)

#Read
#comando = f'SELECT*FROM cliented'
#cursor.execute(comando)
#resultado = cursor.fetchall()#Ler o banco de dados
#print(resultado)

#Update
#Nome_produto = "todynho"
#valor = 6
#comando = f'UPDATE cliented SET valor = {valor} WHERE nome_produto = "{Nome_produto}"'
#cursor.execute(comando)
#conexao.commit() 

#Delete