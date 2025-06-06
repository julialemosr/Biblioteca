from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, declarative_base
# engine = create_engine('sqlite:///base_biblioteca.sqlite3')

from dotenv import load_dotenv
import os  # criar variavel de ambiente '.env'
import configparser  # criar arquivo de configuração 'config.ini'

# configurar banco vercel
# ler variavel de ambiente
load_dotenv()
# Carregue as configurações do banco de dados
url_ = os.environ.get("DATABASE_URL")
print(f"modo1:{url_}")

# Carregue o arquivo de configuração
config = configparser.ConfigParser()
config.read('config.ini')
# Obtenha as configurações do banco de dados
database_url = config['database']['url']
print(f"mode2:{database_url}")

#Configuração da base de dados SQLite Online e local
#engine = create_engine(database_url) # conectar Vercel
engine = create_engine('sqlite:///base_biblioteca.sqlite3') # conectar local alterado/substituído

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
# Base.query = db_session.query_property()

class Livro(Base):
    __tablename__ = 'LIVROS'
    id_livro = Column(Integer, primary_key=True)
    titulo = Column(String(40), nullable=False, index=True, unique=True)
    autor = Column(String(30), nullable=False, index=True)
    ISBN = Column(Integer, nullable=False, index=True)
    resumo = Column(String(200), nullable=False, index=True)

    def __repr__(self):
        return '<Livro: {} {} {} {} {}'.format(self.id_livro, self.titulo, self.autor, self.ISBN, self.resumo)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_livro(self):
        dados_livro = {
            "id_livro": self.id_livro,
            "Titulo": self.titulo,
            "Autor": self.autor,
            "ISBN": self.ISBN,
            "Resumo": self.resumo
        }
        return dados_livro



class Usuario(Base):
    __tablename__ = 'USUARIOS'
    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String(40), nullable=False, index=True)
    CPF = Column(String(11), nullable=False, index=True, unique=True)
    endereco = Column(String(50), nullable=False, index=True)

    def __repr__(self):
        return '<Produto: {} {} {} {}'.format(self.id_usuario, self.nome, self.CPF, self.endereco)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_usuario(self):
        dados_usuario = {
            "id_usuario": self.id_usuario,
            "Nome": self.nome,
            "CPF": self.CPF,
            "Endereco": self.endereco
        }
        return dados_usuario


class Emprestimo(Base):
    __tablename__ = 'EMPRESTIMOS'
    id_emprestimo = Column(Integer, primary_key=True)
    data_emprestimo = Column(String(8), nullable=False, index=True)
    data_devolucao = Column(String(8), nullable=False, index=True)

    id_usuario = Column(Integer, ForeignKey('USUARIOS.id_usuario'))
    usuario = relationship('Usuario')
    id_livro = Column(Integer, ForeignKey('LIVROS.id_livro'))
    livro = relationship('Livro')


    def __repr__(self):
        return '<Venda: {} {} {} {} '.format(self.id_livro, self.id_emprestimo, self.data_emprestimo, self.data_devolucao)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_emprestimo(self):
        dados_emprestimo = {
            "id_emprestimo": self.id_emprestimo,
            "Data_emprestimo": self.data_emprestimo,
            "Data_devolucao": self.data_devolucao,
            "id_usuario": self.id_usuario,
            "id_livro": self.id_livro,
        }
        return dados_emprestimo

def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()