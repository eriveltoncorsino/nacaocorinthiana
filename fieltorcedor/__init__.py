from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) # app é uma instância da classe flask

app.config['SECRET_KEY'] = '29cecf8afd6176f06bb3f55472d490d1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///torcedores.db'

database = SQLAlchemy(app)
# Com o código bcrypt, somente o nosso site será permitido criptografar e descriptograr as senhas.
bcrypt = Bcrypt(app)
# Criar a variável Login para o nosso site
login_manager = LoginManager(app)
# Vamos direcionar a pessoa que quiser consultar alguma página e não estiver logado para a página de login
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

# A importação deve ser colocada no final pois precisamos executar o app pois precisamos
# que o app esteja rodando.
from fieltorcedor import routes
