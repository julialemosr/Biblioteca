import sqlalchemy
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
    return jsonify({'lista_emprestimos' : lista_emprestimos})

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

@app.route('/realizar_emprestimo', methods=['POST'])
def realizar_emprestimo():
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

@app.route('/livros_disponiveis_emprestados', methods=['GET'])
def consultas():
    sql_consultas = select(Livro)
    resultado_consultas = db_session.execute(sql_consultas).scalars()
    lista_consultas = []
    for n in resultado_consultas:
        lista_consultas.append(n.serialize_livro())
    return jsonify({'lista_livros_disponiveis_emprestados': lista_consultas})

@app.route('/consulta_historico_emprestimo', methods=['GET'])
def historico_emprestimo():
    sql_historico_emprestimo = select(Emprestimo)
    resultado_historico_emprestimo = db_session.execute(sql_historico_emprestimo).scalars()
    lista_historico_emprestimo = []
    for n in resultado_historico_emprestimo:
        lista_historico_emprestimo.append(n.serialize_emprestimo())
    return jsonify({'lista_consulta_historico_emprestimo': lista_historico_emprestimo})


@app.route('/atualizar_usuario/<id>', methods=['PUT'])
def atualizar_usuario(id):
    try:
        usuario_editado = db_session.execute(select(Usuario).where(Usuario.id_usuario == id)).scalar()

        if not usuario_editado:
            return jsonify({
                "erro": "Não foi possível encontrar o usuário!"
            })

        if request.method == 'PUT':
            if (not request.form['form_nome'] and not request.form['form_CPF']
                    and not request.form['form_endereco']):
                return jsonify({
                    "erro": "Os campos não devem ficar em branco!"
                })

            else:
                CPF = request.form['form_CPF'].strip()
                if usuario_editado.CPF != CPF:
                    CPF_existe = db_session.execute(select(Usuario).where(Usuario.CPF == CPF)).scalar()

                    if CPF_existe:
                        return jsonify({
                            "erro": "Este CPF já existe!"
                        })

                usuario_editado.nome = request.form['form_nome']
                usuario_editado.CPF = request.form['form_CPF'].strip()
                usuario_editado.endereco = request.form['form_endereco']

                usuario_editado.save()

                return jsonify({
                    "nome": usuario_editado.nome,
                    "CPF": usuario_editado.CPF,
                    "endereco": usuario_editado.endereco,
                })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "Esse CPF já foi cadastrado!"
        })

@app.route('/atualizar_livro/<id>', methods=['PUT'])
def atualizar_livro(id):
    try:
        livro_editado = db_session.execute(select(Livro).where(Livro.id_livro == id)).scalar()

        if not livro_editado:
            return jsonify({
                "erro": "O livro não foi encontrado!"
            })

        if request.method == 'PUT':
            if (not request.form['form_titulo'] and not request.form['form_autor']
                    and not request.form['form_ISBN'] and not request.form['form_resumo']):
                return jsonify({
                    "erro": "Os campos não devem ficar em branco!"
                })

            else:
                livro_editado.titulo = request.form['form_titulo']
                livro_editado.autor = request.form['form_autor']
                livro_editado.ISBN = request.form['form_ISBN']
                livro_editado.resumo = request.form['form_resumo']

                livro_editado.save()

                return jsonify({
                    "titulo": livro_editado.titulo,
                    "autor": livro_editado.autor,
                    "ISBN": livro_editado.ISBN,
                    "resumo": livro_editado.resumo
                })

    except sqlalchemy.exc.IntegrityError:
        return jsonify({
            "erro": "O titulo já foi cadastrado!"
        })


if __name__ == '__main__':
    app.run(debug=True)