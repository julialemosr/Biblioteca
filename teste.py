
import sqlalchemy
from sqlalchemy import *
from flask import Flask, jsonify, request
from flask_pydantic_spec import FlaskPydanticSpec
from models import *
app = Flask(__name__)

@app.route('/status_livro', methods=['GET'])
def status_livro():
    try:
        livro_emprestado = db_session.execute(
            select(Livro).where(Livro.id_livro == Emprestimo.id_emprestimo).distinct(Livro.ISBN)).scalars()
        id_livro_emprestado = db_session.execute(
            select(Livro.id_livro).where(Livro.id_livro == Emprestimo.id_emprestimo).distinct(Livro.ISBN)).scalars()
        print("livro Emprestado",livro_emprestado)
        livrostatus = db_session.execute(select(Livro)).scalars()

        print("Livros todos", livrostatus)

        lista_emprestados = []
        lista_disponiveis = []
        for livro in livro_emprestado:
            lista_emprestados.append(livro.serialize_user())

        for book in livrostatus:
            if book.id not in id_livro_emprestado:
                lista_disponiveis.append(book.serialize_user())

        print("resultados lista", lista_emprestados)
        print("resultados disponibiliza", lista_disponiveis)


        return jsonify({
            "livros emprestados": lista_emprestados,
            "livros disponiveis": lista_disponiveis

        })

    except ValueError:
        return jsonify({
            "error": "dados de status indisponíveis"
        })


if __name__ == '__main__':
    app.run(debug=True)