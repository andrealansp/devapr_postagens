from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

lista_cancoes = [
    {"cancao":"Me Refez",
     "estilo":"Gospel"},
    {"cancao":"Pra Onde Iremos? (Ao Vivo)",
     "estilo":"Gospel"},
    {"cancao":"comigo",
     "estilo":"Gospel"},
    {"cancao":"O Jogo Virou",
     "estilo":"Gospel"},
    {"cancao":"Daqui Pra Frente",
     "estilo":"Sertanejo Universitário"},
    {"cancao":"Solteiro Forçado",
     "estilo":"Sertanejo Universitário"},
    {"cancao":"Canudinho",
     "estilo":"Sertanejo Universatário"},
    {"cancao":"Nosso Quadro",
     "estilo":"Sertanejo Universatário"}
]
# GET http://localhost:5000/cancoes
@app.route('/cancoes')
def get_all_nusics():
    return jsonify(lista_cancoes)

# http://localhost:5000/cancoes/1
@app.route('/cancoes/<int:indice>', methods=["GET"])
def get_music_by_id(indice):
    return jsonify(lista_cancoes[indice])

# http://localhost:5000/cancoes
@app.route('/cancoes',methods=["POST"])
def add_music_to_list():
    cancao_adicionada = request.get_json()
    lista_cancoes.append(cancao_adicionada)    
    return jsonify(cancao_adicionada, 200)

# http://localhost:5000/cancoes/1
@app.route('/cancoes/<int:indice>',methods=["PUT"])
def update_music(indice):
    try:
        cancao_atualizada = request.get_json()
        lista_cancoes[indice].update(cancao_atualizada)    
        return jsonify(cancao_atualizada, 200)
    except:
        return (f'Não foi possível encontrar o indice {indice} na lista de músicas', 404)
    
# http://localhost:5000/cancoes/1
@app.route('/cancoes/<int:indice>', methods=["DELETE"])
def delete_music(indice):
    try:
        if lista_cancoes[indice] is not None:
            del lista_cancoes[indice]
            return jsonify(f'Foi excluida com sucesso ! \n {lista_cancoes[indice]}')
    except:
        return jsonify(f'Não foi possível encontrar o indice {indice} na lista de músicas', 404)



app.run(port=5000,host="localhost", debug=True)