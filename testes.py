"""
Este arquivo foi criado para realizar teste. Após o eercício ela foi excluída mas optei por não excluir
para realizar exercícios futuramente.
"""

from fieltorcedor import app, database

with app.app_context():
    database.drop_all()
    database.create_all()

#with app.app_context():
#    usuario = Usuario(username='Lolo', email='lolo@gmail.com', senha='123456')
#    usuario2 = Usuario(username='Sil', email= 'sil@gmail.com', senha='123456')
#    database.session.add(usuario)
#    database.session.add(usuario2)
#    database.session.commit()

# Agora vamos ler o banco de dados e verificar qtos usuarios temos
#with app.app_context():
#    meus_usuarios = Usuario.query.all()
#    print(meus_usuarios)

# with app.app_context():
#     meu_post = Post(id_usuario=1, titulo='Vai Corinthians', corpo="O Corinthians é foda!!!")
#     database.session.add(meu_post)
#     database.session.commit()

# with app.app_context():
#     post = Post.query.first()
#     print(post)
#     print(post.titulo)
#     print(post.autor.email)

#with app.app_context():
    #database.drop_all()
    #database.create_all()