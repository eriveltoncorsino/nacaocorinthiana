from fieltorcedor import database, login_manager
from datetime import datetime
from flask_login import UserMixin

# Vamos criar uma função para encontrar o suário
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

# Após criar a função, temos que informar qual tabela que tem a estrutura de usuário que ela precisa
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    torcidas = database.Column(database.String, nullable=False, default='Não Informado')

    # Vamos criar um método para contar os posts do usuário
    def contar_posts(self):
        return len(self.posts)
    # Agora já podemos contar quantos posts cada usuário tem pelo perfil.html


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)