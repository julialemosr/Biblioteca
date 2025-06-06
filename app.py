import sqlalchemy
from flask import Flask, jsonify, request
from sqlalchemy import select
from models import Livro, Usuario, Emprestimo, db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

@app.route('/livros', methods=['GET'])
def livros():
    """
        Lista de Livros
           ## Endpoint:
            /livros

           ## Respostas (JSON):
           ```json

        {
            "livros": lista_livros"
        }
        ## Erros possíveis (JSON):
        "A lista está indisponível"
        Bad Request***:
            ```json
    """

    sql_livros = select(Livro)
    resultado_livros = db_session.execute(sql_livros).scalars()
    lista_livros = []
    for n in resultado_livros:
        lista_livros.append(n.serialize_livro())

    print(lista_livros)
    return jsonify({'lista_livros': lista_livros})

@app.route('/usuarios', methods=['GET'])
#proteção
def usuarios():
    """
       Lista de usuários.
       ## Endpoint:
        /usuarios

       ## Respostas (JSON):
       ```json

       {
            "usuarios": lista_usuarios
       }
        ## Erros possíveis (JSON):
        "A lista está indisponível"
        Bad Request***:
            ```json
    """

    sql_usuarios = select(Usuario)
    resultado_usuarios = db_session.execute(sql_usuarios).scalars()
    lista_usuarios = []
    for n in resultado_usuarios:
        lista_usuarios.append(n.serialize_usuario())
    return jsonify({'lista_usuarios': lista_usuarios})

@app.route('/emprestimos', methods=['GET'])
def emprestimos():
    """
       listar emprestimo por usuário.

       ## Endpoint:
        /emprestimos

       ## Respostas (JSON):
       ```json

       {
            "emprestimos": lista_emprestimos
       }

        ## Erros possíveis (JSON):
        "NOs dados desse empréstimo não estão disponíveis ***400
        Bad Request***:
            ```json
    """

    sql_emprestimos = select(Emprestimo)
    resultado_emprestimos = db_session.execute(sql_emprestimos).scalars().all()
    lista_emprestimos = []

    for n in resultado_emprestimos:
        lista_emprestimos.append(n.serialize_emprestimo())
    print(lista_emprestimos)
    return jsonify({'lista_emprestimos': lista_emprestimos}), 200

@app.route('/novo_livro', methods=['POST'])
#proteção
def criar_livros():
    """
       Cadastro de livro.

       ## Endpoint:
        /novo_livro

       ## Respostas (JSON):
       ```json

       {
            "titulo":
            "autor",
            "ISBN":,
            "resumo",
        }

       ## Erros possíveis (JSON):
        "O livro já está cadastrado"
        Bad Request***:
            ```json
       """
    try:
        dados = request.get_json()
        print(dados)
        if not  "titulo" or not "autor" or not "ISBN" in dados:
            return jsonify({'erro': "Campos obrigatórios"})
        if dados["titulo"]== "" or ["autor"]== "" or ["ISBN"]== "" or ["resumo"] == "":
            return jsonify({'erro': "O campo não pode estar vazio"})
        cadastro_livro = Livro(
            titulo=str (dados['titulo']),
            autor=str(dados['autor']),
            ISBN=int(dados['ISBN']),
            resumo=str(dados['resumo'])
        )

        cadastro_livro.save()

        return jsonify({
            'Mensagem': 'Livro adicionado com sucesso',
            'Titulo': cadastro_livro.titulo,
            'Autor': cadastro_livro.autor,
            'ISBN': cadastro_livro.ISBN,
            'Resumo': cadastro_livro.resumo
        }),201

    except ValueError:
        return jsonify({
            'erro':'cadastro de livro inválida!'
        })

@app.route('/novo_usuario', methods=['POST'])
def criar_usuarios():
    """
            Cadastro de usuário

            ## Endpoint:
             /novo_usuario

            ## Respostas (JSON):
            ```json

            {
                 "nome",
                 "cpf":,
                 "endereco",
             }

            ## Erros possíveis (JSON):
             "O usuário já está cadastrado"
             Bad Request***:
                 ```json
            """
    dados = request.get_json()
    print(dados)
    try:
        if not  "nome" or not "CPF" in dados:
            return jsonify({'erro': "Campos obrigatórios"}),400
        if dados["nome"] =="" or ["CPF"] =="" or ["endereco"] == "":
            return jsonify({'erro': "O campo não pode estar vazio"}),400
        cadastro_usuario = Usuario(
            nome=str(dados['nome']),
            CPF=str(dados['CPF']),
            endereco=str(dados['endereco'])
        )

        cadastro_usuario.save()

        return jsonify({
            'Mensagem': 'Usuário criado com sucesso',
            'Nome': cadastro_usuario.nome,
            'CPF': cadastro_usuario.CPF,
            'Endereco': cadastro_usuario.endereco,
        }),201

    except ValueError:
        return jsonify({
            'erro':'cadastro de usuário inválida!'
        }),400

@app.route('/realizar_emprestimo', methods=['POST'])
def realizar_emprestimo():
    """
              Realiza emprestimo.

              ## Endpoint:
               /realizar_emprestimo

              ## Respostas (JSON):
              ```json

              {
                   "id_usuario":,
                   "id_livro",
                   "data_emprestimo",
                   "data_emprestimo",
               }

              ## Erros possíveis (JSON):
               "O empréstimo já foi cadastrado"
               Bad Request***:
                   ```json
              """

    try:
        dados = request.get_json()
        print(dados)
        # if not  "data_emprestimo" or not "data_devolucao" in dados:
        #     return jsonify({'erro': "Campos obrigatórios"})
        # if dados["data_emprestimo"] =="" or ["data_devolucao"] == "":
        #     return jsonify({'erro': "O campo não pode estar vazio"})

        cadastro_emprestimo = Emprestimo(
            id_usuario = int(dados['id_usuario']),
            id_livro = int(dados['id_livro']),
            data_emprestimo = dados['data_emprestimo'],
            data_devolucao = dados['data_devolucao'],
        )
        cadastro_emprestimo.save()
        print('foi cadastrado com sucesso')
        return jsonify({
            'Mensagem': 'Empréstimo realizado com sucesso',
            "id_usuario": cadastro_emprestimo.id_usuario,
            "id_livro": cadastro_emprestimo.id_livro,
            "data_emprestimo": cadastro_emprestimo.data_emprestimo,
            "data_devolucao": cadastro_emprestimo.data_devolucao,
        }),201

    except ValueError:
        return jsonify({
            'erro':'cadastro de usuário inválida!'})

@app.route('/consulta_historico_emprestimo', methods=['GET'])
#protecao
def historico_emprestimo():
    """
       Consulta historico de emprestimo

       ## Endpoint:
        /consulta_historico_emprestimo

       ## Respostas (JSON):
       ```json

       {
            "historico": historico_de_emprestimo
       }

        ## Erros possíveis (JSON):
        "O histórico não está disponível
        Bad Request***:
            ```json
    """
    sql_historico_emprestimo = select(Emprestimo)
    resultado_historico_emprestimo = db_session.execute(sql_historico_emprestimo).scalars()
    lista_historico_emprestimo = []
    for n in resultado_historico_emprestimo:
        lista_historico_emprestimo.append(n.serialize_emprestimo())
    return jsonify({'historico_de_emprestimo': lista_historico_emprestimo})


@app.route('/atualizar_usuario/<id>', methods=['PUT'])
#proteção
def atualizar_usuario(id):
    """
              API para atualizar dados do usuario.

              ## Endpoint:
               /atualizar_usuario/<int:id>

               ##Parâmetros:
               "id" **Id do usuario**

              ## Respostas (JSON):
              ```json

              {
                   "nome":
                   "cpf",
                   "endereco":,
               }

              ## Erros possíveis (JSON):
               "O CPF deste usuário já está cadastrado"
               Bad Request***:
                   ```json
              """
    dados = request.get_json()
    print(dados)
    try:
        if not  "nome" or not "CPF" in dados:
            return jsonify({'erro': "Campos obrigatórios"})
        if dados["nome"] == "" or ["CPF"] == "" or ["endereco"] == "":
            return jsonify({'erro': "O campo não pode estar vazio"})

        usuario_editado = db_session.execute(select(Usuario).where(Usuario.id_usuario == id)).scalar()

        if not usuario_editado:
            return jsonify({
                "erro": "Não foi possível encontrar o usuário!"
            })

        # if request.method == 'PUT':
        if (not dados ['nome'] and not dados ['CPF']
                and not dados ['endereco']):
            return jsonify({
                "erro": "Os campos não devem ficar em branco!"
            })

        else:
            CPF = dados ['CPF'].strip()
            if usuario_editado.CPF != CPF:
                CPF_existe = db_session.execute(select(Usuario).where(Usuario.CPF == CPF)).scalar()

                if CPF_existe:
                    return jsonify({
                        "erro": "Este CPF já existe!"
                    })

            usuario_editado.nome = dados ['nome']
            usuario_editado.CPF = dados ['CPF'].strip()
            usuario_editado.endereco = dados ['endereco']

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
#proteção
def atualizar_livro(id):
    """
               Atualizar livro.
               ## Endpoint:
                /atualizar_livro/<int:id>

                ## Parâmetro:
                "id" **Id do livro**

               ## Respostas (JSON):
               ```json

               {
                    "titulo":
                    "autor",
                    "ISBN":,
                    "resumo",
                }

               ## Erros possíveis (JSON):
                "O titulo do livro já está cadastrado"
                Bad Request***:
                    ```json
               """
    dados = request.get_json()
    print(dados)
    try:
        if not  "titulo" or not "autor" or not "ISBN" in dados:
            return jsonify({'erro': "Campos obrigatórios"})
        if dados["titulo"] == "" or ["autor"] == "" or ["ISBN"] == "" or ["resumo"] == "":
            return jsonify({'erro': "O campo não pode estar vazio"})
        livro_editado = db_session.execute(select(Livro).where(Livro.id_livro == id)).scalar()

        if not livro_editado:
            return jsonify({
                "erro": "O livro não foi encontrado!"
            })

        if request.method == 'PUT':
            if (not dados ['titulo'] and not dados['autor']
                    and not dados ['ISBN'] and not dados ['resumo']):
                return jsonify({
                    "erro": "Os campos não devem ficar em branco!"
                })

            else:
                livro_editado.titulo = dados ['titulo']
                livro_editado.autor = dados ['autor']
                livro_editado.ISBN = dados ['ISBN']
                livro_editado.resumo = dados ['resumo']

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

@app.route('/atualizar_emprestimo/<int:id>', methods=['POST'])
def atualizar_emprestimo(id):
    """
               Atualizar emprestimo.
               ## Endpoint:
                /atualizar_livro/<int:id>

                ## Parâmetro:
                "id" **Id do emprestimo**

               ## Respostas (JSON):
               ```json

               {
                    "id_livro":
                    "id_usuario",
                    "data_devolucao",:,
                    "data_emprestimo":,
                }

               ## Erros possíveis (JSON):
                "O titulo do livro já está cadastrado"
                Bad Request***:
                    ```json
               """
    dados_atualizar_emprestimo = request.get_json()
    try:
        emprestimo_atualizado = db_session.execute(select(Emprestimo).where(Emprestimo.id_emprestimo == id)).scalar()

        if not emprestimo_atualizado:
            return jsonify({
                "erro": "O emprestimo não foi encontrado!"
            })

        if (not "id_livro" in dados_atualizar_emprestimo or not "id_usuario" in dados_atualizar_emprestimo
                or not "data_devolucao" in dados_atualizar_emprestimo or not "data_emprestimo" in dados_atualizar_emprestimo):
            return jsonify({
                "erro": "É obrigatório ter os campos: Nome, CPF e Endereço"
            }), 400

        if (dados_atualizar_emprestimo["id_livro"] == "" or dados_atualizar_emprestimo["id_usuario"] == ""
                or dados_atualizar_emprestimo["data_devolucao"] == "" or dados_atualizar_emprestimo["data_emprestimo"] == ""):
            return jsonify({
                "erro": "Preencha os campos em branco!!"
            }), 400


        emprestimo_atualizado.livro_id = dados_atualizar_emprestimo["id_livro"]
        emprestimo_atualizado.usuario_id = dados_atualizar_emprestimo["id_usuario"].strip()
        emprestimo_atualizado.data_devolucao =dados_atualizar_emprestimo["data_devolucao"]
        emprestimo_atualizado.data_emprestimo = dados_atualizar_emprestimo["data_emprestimo"]

        emprestimo_atualizado.save()
        # db_session.commit()

        return jsonify({
            "id_livro": emprestimo_atualizado.livro_id,
            "id_usuario": emprestimo_atualizado.usuario_id,
            "data_devolucao": emprestimo_atualizado.data_devolucao,
            "data_emprestimo": emprestimo_atualizado.data_emprestimo,
        }), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        db_session.close()

@app.route('/livro_status', methods=['GET'])
def livro_status():
    """
              status de livro.

               ## Endpoint:
                /livro_status
               ## Respostas (JSON):
               ```json
               {
                    "livros emprestados":
                    "livros disponiveis",
                }

                ## Erros possíveis (JSON):
                "Os dados do status está indisponível"
                Bad Request***:
                    ```json
                """
    try:
        livro_emprestado = db_session.execute(
            select(Livro).where(Livro.id_livro == Emprestimo.id_livro).distinct(Livro.ISBN)
        ).scalars()

        id_livro_emprestado = db_session.execute(
            select(Emprestimo.id_livro).distinct(Emprestimo.id_livro)
        ).scalars().all()

        print("livro Emprestados",livro_emprestado)
        print("ids_livro_emprestado",id_livro_emprestado)
        livrostatus = db_session.execute(select(Livro)).scalars()

        print("Todos os livros", livrostatus)

        lista_emprestados = []
        lista_disponiveis = []
        for livro in livro_emprestado:
            lista_emprestados.append(livro.serialize_livro())

        print("Resultados da lista:", lista_emprestados)

        for livro in livrostatus:
            if livro.id_livro not in id_livro_emprestado:
                lista_disponiveis.append(livro.serialize_livro())

        print("Resultados disponiveis", lista_disponiveis)


        return jsonify({
            "Livros emprestados": lista_emprestados,
            "Livros disponiveis": lista_disponiveis

        })

    except ValueError:
        return jsonify({
            "error": "Dados indisponíveis"
        })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

