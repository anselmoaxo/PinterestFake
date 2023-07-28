from fakepinterest import db, login_manager
from datetime import datetime
from flask_login import UserMixin

# Esta função é usada pelo Flask-Login para carregar um usuário com base em seu ID.
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

# Classe para representar a tabela de usuários no banco de dados.
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)  # Nome do usuário
    email = db.Column(db.String, unique=True, nullable=False)  # Email do usuário (deve ser único)
    senha = db.Column(db.String, nullable=False)  # Senha do usuário
    fotos = db.relationship("Foto", backref='usuario')  # Relação com a tabela de fotos (uma lista de fotos pertence a este usuário)

# Classe para representar a tabela de fotos no banco de dados.
class Foto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String, default='default.png')  # Caminho para a imagem da foto (default.png é um valor padrão)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Data de criação da foto
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Chave estrangeira para o ID do usuário que possui esta foto
