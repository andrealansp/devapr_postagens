from collections.abc import Mapping
import jwt
from flask import Flask, jsonify, make_response, request
from estrutura_banco_de_dados import Autor, Postagem, app, db
from functools import wraps
from datetime import datetime, timedelta
import config

def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'manesagem': 'Token não foi incluído!'}, 401)
        try:
            resultado = jwt.decode(token,app.config['SECRET_KEY'])
            autor = Autor.query.filter_by(id_autor=resultado['id_autor']).first()
        except:
            return jsonify({'mensagem': 'Token é inválido!'}, 401)
        return f(autor, *args, **kwargs)
    return decorated


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login Inválido', 401,{'WWW-Authenticate':'Basic realm="Login Obrigatório"'})
    usuario = Autor.query.filter_by(nome=auth.username).first()
    if not usuario:
        return make_response('Login Inválido', 401,{'WWW-Authenticate':'Basic realm="Login Obrigatório"'})
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor':usuario.id_autor, 'exp': datetime.utcnow()+timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token':token.decode('UTF-8')})
    return make_response('Login Inválido', 401,{'WWW-Authenticate':'Basic realm="Login Obrigatório"'})
        

@app.route('/postagens', methods=['GET'])
@token_obrigatorio
def obter_todas_postagens(autor):
    postagens = Postagem.query.all()

    list_postagens = []
    for postagem in postagens:
        postagem_atual = {}
        postagem_atual['titulo'] = postagem.titulo
        postagem_atual['id_autor'] = postagem.id_autor
        list_postagens.append(postagem_atual)
    return jsonify({'postagens': list_postagens})


@app.route('/postagens/<int:postagem_id>', methods=['GET'])
@token_obrigatorio
def obter_postagem_por_id(autor,postagem_id):
    postagem = Postagem.query.filter_by(id_postagem=postagem_id).first()
    postagem_atual = {}
    try:
        postagem_atual['titulo'] = postagem.titulo
    except:
        pass
    postagem_atual['id_autor'] = postagem.id_autor

    return jsonify({'postagens': postagem_atual})


@app.route('/postagens', methods=['POST'])
@token_obrigatorio
def nova_postagem(autor):
    nova_postagem = request.get_json()
    postagem = Postagem(
        titulo=nova_postagem['titulo'], id_autor=nova_postagem['id_autor'])

    db.session.add(postagem)
    db.session.commit()

    return jsonify({'mensagem': 'Postagem criada com sucesso'})


@app.route('/postagens/<int:postagem_id>', methods=['PUT'])
@token_obrigatorio
def atualizar_postagem(autor,postagem_id):
    postagem_alterada = request.get_json()
    postagem = Postagem.query.filter_by(id_postagem=postagem_id).first()
    try:
        postagem.titulo = postagem_alterada['titulo']
    except:
       pass
    try:
       postagem.id_autor = postagem_alterada['id_autor']
    except:
        pass

    db.session.commit()
    return jsonify({'mensagem': 'Postagem alterada com sucessso'})


@app.route('/postagens/<int:postagem_id>', methods=['DELETE'])
@token_obrigatorio
def excluir_postagem(autor,postagem_id):
    postagem_a_ser_excluida = Postagem.query.filter_by(
        id_postagem=postagem_id).first()
    if not postagem_a_ser_excluida:
        return jsonify({'mensagem': 'Não foi encontrado uma postagem com este id'})
    db.session.delete(postagem_a_ser_excluida)
    db.session.commit()

    return jsonify({'mensagem': 'Postagem excluída com sucesso!'})

@app.route('/autores')
@token_obrigatorio
def obter_autores(autor):
    autores = Autor.query.all()
    lista_de_autores = []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor
        autor_atual['email'] = autor.email
        autor_atual['nome'] = autor.nome
        lista_de_autores.append(autor_atual)
        
    return jsonify({'autores':lista_de_autores})

@app.route('/autores/<int:id_autor>', methods=['GET'])
@token_obrigatorio
def obter_autor_por_id(autor,id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify("Autor não encontrado!")
    autor_atual = {}
    autor_atual['id_autor'] = autor.id_autor
    autor_atual['email'] = autor.email
    autor_atual['nome'] = autor.nome
    
    return jsonify({"autor":autor_atual})

@app.route('/autores', methods=['POST'])
@token_obrigatorio
def novo_autor(autor):
    novo_autor = request.get_json()
    autor = Autor(nome=novo_autor['nome'], senha=novo_autor['senha'], email=novo_autor['email'])
    db.session.add(autor)
    db.session.commit()
    return jsonify('Usuário criado com sucesso',200)

@app.route('/autors/<int:id_autor>', methods=['PUT'])
@token_obrigatorio
def alterar_autor(autor,id_autor):
    usuario_a_alterar = request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify({"Mensagem": "Este usuário não foi encontrado"})
    try:
        if usuario_a_alterar['nome']:
            autor.nome = usuario_a_alterar['nome']
    except:
        pass
    try:
        if usuario_a_alterar['email']:
            autor.email = usuario_a_alterar['email']
    except:
        pass
    try:
        if usuario_a_alterar['senha']:
            autor.senha = usuario_a_alterar['senha']
    except:
        pass
    db.session.commit()
    return jsonify({"mensagem":"Usuário alterado com sucesso!"})
    

@app.route('/autores/<int:id_autor>', methods=['DELETE'])
@token_obrigatorio
def excluir_autor(autor,id_autor):
    autor_existente = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor_existente:
        return jsonify({'mensagem':'Este autor não foi encontrado!'})
    db.session.delete(autor_existente)
    db.session.commit()
    
    return jsonify({'mensagem': 'Autor excluído com sucesso !'})

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
