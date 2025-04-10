from flask import Flask, jsonify, request, redirect, url_for, flash
from sqlalchemy import select
from models import Livro, Usuario, Emprestimo, db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

@app.route('/livros', methods=['GET'])
def livros():
    sql_livros = select(Livro)
    resultado_livros = db_session.execute(sql_livros).scalars()
    lista_livros = []
    for n in resultado_livros:
        lista_livros.append(n.serialize_livro())
    return jsonify({'lista_livros': lista_livros})

@app.route('/usuarios', methods=['GET'])
def usuarios():
    sql_usuarios = select(Usuario)
    resultado_usuarios = db_session.execute(sql_usuarios).scalars()
    lista_usuarios = []
    for n in resultado_usuarios:
        lista_usuarios.append(n.serialize_usuario())
    return jsonify({'lista_usuarios': lista_usuarios})

@app.route('/emprestimos', methods=['GET'])
def emprestimos():
    sql_emprestimos = select(Emprestimo)
    resultado_emprestimos = db_session.execute(sql_emprestimos).scalars()
    lista_emprestimos = []
    for n in resultado_emprestimos:
        lista_emprestimos.append(n.serialize_emprestimo())
    return jsonify({'lista_emprestimos'
                    '': lista_emprestimos})

@app.route('/novo_livro', methods=['POST'])
def criar_livros():
    try:
        form_cadastro_livro = Livro(
            titulo=str (request.form['form-titulo']),
            autor=str(request.form['form-autor']),
            ISBN=int(request.form['form-ISBN']),
            resumo=str(request.form['form-resumo'])
        )

        form_cadastro_livro.save()

        return jsonify({
            'Mensagem': 'Livro adicionado com sucesso',
            'Titulo': form_cadastro_livro.titulo,
            'Autor': form_cadastro_livro.autor,
            'ISBN': form_cadastro_livro.ISBN,
            'Resumo': form_cadastro_livro.resumo
        })

    except ValueError:
        return jsonify({
            'erro':'cadastro de livro inválida!'
        })

@app.route('/novo_usuario', methods=['POST'])
def criar_usuarios():
    try:
        form_cadastro_usuario = Usuario(
            nome=str(request.form['form-nome']),
            CPF=str(request.form['form-CPF']),
            endereco=str(request.form['form-endereco'])
        )

        form_cadastro_usuario.save()

        return jsonify({
            'Mensagem': 'Usuário criado com sucesso',
            'Nome': form_cadastro_usuario.nome,
            'CPF': form_cadastro_usuario.CPF,
            'Endereco': form_cadastro_usuario.endereco,
        })

    except ValueError:
        return jsonify({
            'erro':'cadastro de usuário inválida!'
        })

@app.route('/realizacao_emprestimo', methods=['POST'])
def realizacao_emprestimo():
    try:
        form_cadastro_emprestimo = Emprestimo(
            id_usuario = int(request.form['id_usuario']),
            id_livro = int(request.form['id_livro']),
            data_emprestimo = request.form['data_emprestimo'],
            data_devolucao = request.form['data_devolucao']
        )
        return jsonify({
            'Mensagem': 'Empréstimo realizado com sucesso',
            'id_usuario': form_cadastro_emprestimo.id_usuario,
            'id_livro': form_cadastro_emprestimo.id_livro,
            'data_emprestimo': form_cadastro_emprestimo.data_emprestimo,
            'data_devolucao': form_cadastro_emprestimo.data_devolucao,
        })

    except ValueError:
        return jsonify({
            'erro':'cadastro de usuário inválida!'
        })

@app.route('/consulta_livros', methods=['GET'])
def consulta_livros():
    try:


        return jsonify({

        })

    except ValueError:
        return jsonify({
            'erro':'cadastro de usuário inválida!'
        })


if __name__ == '__main__':
    app.run(debug=True)