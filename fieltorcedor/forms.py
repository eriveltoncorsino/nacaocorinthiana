from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
# A biblioteca a seguir puxam como as informações que devem ser preenchidas (texto, número mostrando o asteriosco e botão, lembrar dados)
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
# Valida os campos preenchidos (campos obrigatórios, tamanho, e-mail, confirmação de senha)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from fieltorcedor.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Repita a Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    # Vamos definir uma função onde informará caso já exista cadastro com o usuario
    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError(f"Usuário {username.data}já existe. Cadastre um usuário válido!")

    # Vamos definir uma função onde informará caso já exista cadastro com o e-mail
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto do Perfil', validators=[FileAllowed(['jpg', 'png'])])
    torcida_gavioes = BooleanField("Gaviões da Fiel")
    torcida_camisa = BooleanField("Camisa 12")
    torcida_pavilhao = BooleanField("Pavilhão 9")
    torcida_estopim = BooleanField("Estopim da Fiel")
    torcida_chopp = BooleanField("Coringão Chopp")
    torcida_macabra = BooleanField("Fiel Macabra")
    torcida_avulsa = BooleanField("Não sou filiado a Organizadas")
    botao_submit_editarperfil = SubmitField("Confirmar")

    # Vamos verificar se o e-mail que o usuário está alterando já existe com outro usuário
    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError(f"E-mail {email.data} já existe. Cadastre um e-mail válido!")


class FormCriarPost(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')