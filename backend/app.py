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

@app.route("/api/cadastro", methods=["POST"])
def cadastro():
    dados = request.get_json() or {}
    nome = dados.get("nome", "").strip()
    email = dados.get("email", "").strip().lower()
    senha = dados.get("senha", "")

    if not nome or not email or not senha:
        return jsonify({"erro": "Informe nome, e-mail e senha."}), 400

    if len(senha) < 8:
        return jsonify({"erro": "A senha precisa ter pelo menos 8 caracteres."}), 400

    senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO USUARIO (nome, email, senha_hash, perfil) "
            "VALUES (%s, %s, %s, 'colaborador')",
            (nome, email, senha_hash),
        )
        conexao.commit()
    except mysql.connector.IntegrityError:
        return jsonify({"erro": "Este e-mail já está cadastrado."}), 409
    finally:
        cursor.close()
        conexao.close()

    return jsonify({"mensagem": "Cadastro realizado com sucesso."}), 201

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensagem": "Logout realizado."})


@app.route("/api/eu")
def quem_sou_eu():
    if "id_usuario" not in session:
        return jsonify({"logado": False})

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute(
        "SELECT id_usuario, nome, perfil FROM USUARIO "
        "WHERE id_usuario = %s AND ativo = TRUE",
        (session["id_usuario"],),
    )
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not usuario:
        session.clear()
        return jsonify({"logado": False})

    return jsonify({"logado": True, "nome": usuario["nome"], "perfil": usuario["perfil"]})

def exige_login():
    if "id_usuario" not in session:
        return jsonify({"erro": "Faça login para continuar."}), 401
    return None


def exige_admin():
    if "id_usuario" not in session:
        return jsonify({"erro": "Faça login para continuar."}), 401
    if session.get("perfil") != "administrador":
        return jsonify({"erro": "Acesso restrito a administradores."}), 403
    return None


@app.route("/api/contribuicoes", methods=["POST"])
def enviar_contribuicao():
    erro = exige_login()
    if erro:
        return erro

    dados = request.get_json() or {}
    id_tema = dados.get("id_tema")
    titulo = dados.get("titulo", "").strip()
    descricao = dados.get("descricao", "").strip()
    como_usar = dados.get("como_usar", "").strip() or None
    fonte = dados.get("fonte", "").strip() or None

    if not id_tema or not titulo or not descricao:
        return jsonify({"erro": "Informe tema, título e descrição."}), 400

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_tema FROM TEMA WHERE id_tema = %s AND ativo = TRUE", (id_tema,))
    if not cursor.fetchone():
        cursor.close()
        conexao.close()
        return jsonify({"erro": "Tema não encontrado."}), 404

    cursor.execute(
        "INSERT INTO CONTRIBUICAO (id_tema, id_usuario, titulo, descricao, como_usar, fonte) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (id_tema, session["id_usuario"], titulo, descricao, como_usar, fonte),
    )
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({"mensagem": "Contribuição enviada para aprovação."}), 201


@app.route("/api/contribuicoes/pendentes")
def listar_pendentes():
    erro = exige_admin()
    if erro:
        return erro

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute(
        "SELECT c.id_contribuicao, c.titulo, c.descricao, c.como_usar, c.fonte, "
        "c.criado_em, t.titulo AS tema, u.nome AS colaborador "
        "FROM CONTRIBUICAO c "
        "JOIN TEMA t ON t.id_tema = c.id_tema "
        "JOIN USUARIO u ON u.id_usuario = c.id_usuario "
        "WHERE c.status = 'pendente' ORDER BY c.criado_em"
    )
    pendentes = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(pendentes)


@app.route("/api/contribuicoes/<int:id_contribuicao>/aprovar", methods=["POST"])
def aprovar_contribuicao(id_contribuicao):
    erro = exige_admin()
    if erro:
        return erro

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM CONTRIBUICAO WHERE id_contribuicao = %s AND status = 'pendente'",
        (id_contribuicao,),
    )
    c = cursor.fetchone()
    if not c:
        cursor.close()
        conexao.close()
        return jsonify({"erro": "Contribuição pendente não encontrada."}), 404

    cursor.execute(
        "INSERT INTO REPERTORIO (titulo, descricao, como_usar, fonte, id_usuario_criador) "
        "VALUES (%s, %s, %s, %s, %s)",
        (c["titulo"], c["descricao"], c["como_usar"], c["fonte"], c["id_usuario"]),
    )
    id_repertorio = cursor.lastrowid
    cursor.execute(
        "INSERT INTO TEMA_REPERTORIO (id_tema, id_repertorio) VALUES (%s, %s)",
        (c["id_tema"], id_repertorio),
    )
    cursor.execute(
        "UPDATE CONTRIBUICAO SET status = 'aprovada', id_admin_avaliador = %s, "
        "avaliado_em = NOW(), id_repertorio = %s WHERE id_contribuicao = %s",
        (session["id_usuario"], id_repertorio, id_contribuicao),
    )
    conexao.commit()
    cursor.close()
    conexao.close()
    return jsonify({"mensagem": "Contribuição aprovada e publicada."})


@app.route("/api/contribuicoes/<int:id_contribuicao>/rejeitar", methods=["POST"])
def rejeitar_contribuicao(id_contribuicao):
    erro = exige_admin()
    if erro:
        return erro

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE CONTRIBUICAO SET status = 'rejeitada', id_admin_avaliador = %s, "
        "avaliado_em = NOW() WHERE id_contribuicao = %s AND status = 'pendente'",
        (session["id_usuario"], id_contribuicao),
    )
    conexao.commit()
    alteradas = cursor.rowcount
    cursor.close()
    conexao.close()
    if alteradas == 0:
        return jsonify({"erro": "Contribuição pendente não encontrada."}), 404
    return jsonify({"mensagem": "Contribuição rejeitada."})

@app.route("/api/temas/<int:id_tema>")
def detalhe_tema(id_tema):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT id_tema, titulo, descricao FROM TEMA WHERE id_tema = %s AND ativo = TRUE",
        (id_tema,),
    )
    tema = cursor.fetchone()
    if not tema:
        cursor.close()
        conexao.close()
        return jsonify({"erro": "Tema não encontrado."}), 404

    cursor.execute(
        "SELECT r.id_repertorio, r.titulo, r.descricao, r.como_usar, r.fonte "
        "FROM REPERTORIO r "
        "JOIN TEMA_REPERTORIO tr ON tr.id_repertorio = r.id_repertorio "
        "WHERE tr.id_tema = %s AND r.ativo = TRUE ORDER BY r.titulo",
        (id_tema,),
    )
    tema["repertorios"] = cursor.fetchall()

    cursor.execute(
        "SELECT m.id_material, m.titulo, m.descricao, m.tipo, m.fonte, m.url "
        "FROM MATERIAL_COMPLEMENTAR m "
        "JOIN TEMA_MATERIAL tm ON tm.id_material = m.id_material "
        "WHERE tm.id_tema = %s AND m.ativo = TRUE ORDER BY m.titulo",
        (id_tema,),
    )
    tema["materiais"] = cursor.fetchall()

    cursor.close()
    conexao.close()
    return jsonify(tema)

if __name__ == "__main__":
    app.run(debug=True)