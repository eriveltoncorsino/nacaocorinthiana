import os
import secrets

from PIL import Image
from flask import render_template, redirect, url_for, flash, request, abort
from fieltorcedor import app, database, bcrypt
from fieltorcedor.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from fieltorcedor.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login realizado com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'E-mail ou senha incorretos. Verifique seus dados!!!', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # Vamos criptografar a senha antes de criá-lo
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        # Vamos adicionar um novo usuário
        database.session.add(usuario)
        # Vamos salvar os dados do novo usuário
        database.session.commit()
        # exibir mensagem de cadastro bem-sucedido
        flash(f'Conta Cadastrada com Sucesso para o E-mail {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Efetuado com Sucesso', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    # adicionar um código aleatótiono nome da imagem
    codigo = secrets.token_hex(4)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # reduzir o tamanho da imagem
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)
    # mudar o campo foto_perfil do usuário para o novo nome da imagem
    return nome_arquivo


def atualizar_torcidas(form):
    lista_torcidas = []
    for campo in form:
        if 'torcida_' in campo.name:
            if campo.data:
                # adicionar o texto do campo.label (Gaviões da Fiel) na lista de torcidas
                lista_torcidas.append(campo.label.text)
    return ';'.join(lista_torcidas)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    # Se o formulário for válido
    if form.validate_on_submit():
        # vamos pegar o e-mail atual e alterar para o preenchido no formulário
        current_user.email = form.email.data
        # vamos pegar o username atual e alterar para o preenchido no formulário
        current_user.username = form.username.data
        if form.foto_perfil.data:
            # Vamos excluir a imagem anterior à alteração
            foto_antiga = current_user.foto_perfil
            if foto_antiga != "default.jpg":
                arquivo = os.path.join(app.root_path, "static/fotos_perfil", foto_antiga)
                if os.path.isfile(arquivo):
                    os.remove(arquivo)
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.torcidas = atualizar_torcidas(form)
        database.session.commit()
        flash("Cadastro atualizado com sucesso!", "alert-success")
        return redirect(url_for("perfil"))
    # Vamos fazer com que os campos sejam preenchidos com as informações automaticamente
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    # Se o autor do post estiver logado
    if current_user == post.autor:
        form = FormCriarPost()
        # Vamos preencher automaticamente, casotenha errado somente uma palavra ou letra não forçará o autor a preencher tudo novamente
        if request.method == "GET":
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash("Post atualizado com sucesso!", "alert-success")
            return redirect(url_for("home"))
    else:
        form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash("Post excluído com sucesso!", "alert-danger")
        return redirect(url_for("home"))
    else:
        abort(403)