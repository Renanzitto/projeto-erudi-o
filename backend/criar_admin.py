import getpass
import bcrypt
from app import conectar

nome = input("Nome do administrador: ")
email = input("E-mail do administrador: ")
senha = getpass.getpass("Senha (não aparece enquanto você digita): ")

senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

conexao = conectar()
cursor = conexao.cursor()
cursor.execute(
    "INSERT INTO USUARIO (nome, email, senha_hash, perfil) VALUES (%s, %s, %s, 'administrador')",
    (nome, email, senha_hash),
)
conexao.commit()
cursor.close()
conexao.close()

print("Administrador criado com sucesso!")