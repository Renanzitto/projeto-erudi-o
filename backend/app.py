import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify, request, session
import bcrypt
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
CORS(app)


def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


@app.route("/api/teste")
def teste():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM TEMA")
        total = cursor.fetchone()[0]
        cursor.close()
        conexao.close()
        return jsonify({"status": "ok", "temas_cadastrados": total})
    except Exception as erro:
        return jsonify({"status": "erro", "mensagem": str(erro)}), 500
@app.route("/api/temas")

def listar_temas():
    busca = request.args.get("busca", "").strip()

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    if busca:
        cursor.execute(
            "SELECT id_tema, titulo, descricao FROM TEMA "
            "WHERE ativo = TRUE AND titulo LIKE %s ORDER BY titulo",
            (f"%{busca}%",),
        )
    else:
        cursor.execute(
            "SELECT id_tema, titulo, descricao FROM TEMA "
            "WHERE ativo = TRUE ORDER BY titulo"
        )

    temas = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(temas)

@app.route("/api/login", methods=["POST"])
def login():
    dados = request.get_json() or {}
    email = dados.get("email", "").strip()
    senha = dados.get("senha", "")

    if not email or not senha:
        return jsonify({"erro": "Informe e-mail e senha."}), 400

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute(
        "SELECT id_usuario, nome, senha_hash, perfil FROM USUARIO "
        "WHERE email = %s AND ativo = TRUE",
        (email,),
    )
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not usuario or not bcrypt.checkpw(
        senha.encode("utf-8"), usuario["senha_hash"].encode("utf-8")
    ):
        return jsonify({"erro": "E-mail ou senha incorretos."}), 401

    session["id_usuario"] = usuario["id_usuario"]
    session["perfil"] = usuario["perfil"]
    return jsonify({"mensagem": "Login realizado.", "nome": usuario["nome"], "perfil": usuario["perfil"]})

if __name__ == "__main__":
    app.run(debug=True)