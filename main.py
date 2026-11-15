import os
from flask import Flask, jsonify, request, send_from_directory, abort
from medicao import dados_Pessoa, novo_cenario, ajustar_passo, gerar_relatorio, serializar

app = Flask(__name__)
PASTA = os.path.dirname(os.path.abspath(__file__))
usuarios = []  # fica na memória: ao fechar o programa, os cadastros são perdidos


def buscar(uid):
    if 0 <= uid < len(usuarios):
        return usuarios[uid]
    abort(404)


@app.errorhandler(404)
def nao_encontrado(e):
    return jsonify(erro="Usuário não encontrado. Se o servidor foi reiniciado, recarregue a página e cadastre de novo."), 404


@app.route("/")
def index():
    return send_from_directory(PASTA, "index.html")


@app.route("/api/usuarios", methods=["GET"])
def listar():
    return jsonify([{"id": u["id"], "nome": u["nome"]} for u in usuarios])


@app.route("/api/usuarios", methods=["POST"])
def cadastrar():
    try:
        usuario = dados_Pessoa(**(request.get_json() or {}))
    except TypeError:
        return jsonify(erro="Dados incompletos. Preencha todos os campos."), 400
    except ValueError as erro:
        return jsonify(erro=str(erro)), 400
    usuario["id"] = len(usuarios)
    usuarios.append(usuario)
    return jsonify(serializar(usuario)), 201


@app.route("/api/usuarios/<int:uid>", methods=["GET"])
def detalhar(uid):
    return jsonify(serializar(buscar(uid)))


@app.route("/api/usuarios/<int:uid>/cenario", methods=["POST"])
def cenario(uid):
    usuario = buscar(uid)
    novo_cenario(usuario)
    return jsonify(serializar(usuario))


@app.route("/api/usuarios/<int:uid>/passo", methods=["POST"])
def passo(uid):
    usuario = buscar(uid)
    ajustar_passo(usuario)
    return jsonify(serializar(usuario))


@app.route("/api/usuarios/<int:uid>/relatorio", methods=["GET"])
def relatorio(uid):
    return jsonify(gerar_relatorio(buscar(uid)))


if __name__ == "__main__":
    print("Abra no navegador: http://localhost:5000")
    app.run(debug=True, port=5000)
