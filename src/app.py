"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
import json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario, Personajes, Favoritos, Vehicles, Planetas
#from models import Person
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.

# Renderizar formulario de Inicio de sesión
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    usuario_login = Usuario.query.filter_by(email=email).first()
    if email!= usuario_login.email or password != usuario_login.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

# Renderizar formulario de registro
@app.route("/signup", methods=["POST"])
def signup():
    # name = request.json.get("name", None)
    # password = request.json.get("password", None)
    # usuario_login = Usuario.query.filter_by(name=name).first()
    # if name!= usuario_login.name or password != usuario_login.password:
    #     return jsonify({"msg": "Bad username or password"}), 401

    # access_token = create_access_token(identity=name)
    # return jsonify(access_token=access_token)}
    body = json.loads(request.data)
    
    user = Usuario.query.filter_by(email=body["email"]).first() 
    
    if user is None:
            newUser = Usuario(name=body["name"], email=body["email"], password=body["password"])
            db.session.add(newUser)
            db.session.commit()
            response_body = {
                "msg": "El usuario fue creado con exito"
            }
            return jsonify(response_body), 200

    response_body = {
            "msg": "User exist in the system"
        }
    return jsonify(response_body), 400


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/private", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    usuario_private = Usuario.query.filter_by(name=current_user).first()
    return jsonify(logged_in_as=usuario_private.serialize()), 200

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#a partir de aca empiezan los endpoints

@app.route('/personajes', methods=['GET'])
def handle_personajes():
    allpersonajes = Personajes.query.all()
    results = list(map(lambda item: item.serialize(),allpersonajes))

    return jsonify(results), 200

#obteniendo info de un solo user
@app.route('/personajes/<int:personajes_id>', methods=['GET'])
def get_info_personajes(personajes_id):
    
    personajes = Personajes.query.filter_by(id=personajes_id).first()
    return jsonify(personajes.serialize()), 200

@app.route('/planetas', methods=['GET'])
def handle_planetas():
    allplanetas = Planetas.query.all()
    results = list(map(lambda item: item.serialize(),allplanetas))

    return jsonify(results), 200

#obteniendo info de un solo user
@app.route('/planetas/<int:planetas_id>', methods=['GET'])
def get_info_planetas(planetas_id):
    
    planetas = Planetas.query.filter_by(id=planetas_id).first()
    return jsonify(planetas.serialize()), 200

@app.route('/usuario', methods=['GET'])
def handle_usuario():
    allusuario= Usuario.query.all()
    results = list(map(lambda item: item.serialize(),allusuario))

    return jsonify(results), 200

# obteniendo info de un solo user
@app.route('/usuario/<int:usuario_id>/favoritos/', methods=['GET'])
def get_favoritos_usuario(usuario_id):
    
    usuario_favoritos = Favoritos.query.filter_by(usuario_id=usuario_id).all()
    results = list(map(lambda item: item.serialize(),usuario_favoritos))
    print(results)
    return jsonify(results), 200
    # return jsonify({"msg":"funciona"})
    
# @app.route('/usuario/<int:usuario_id>/favoritos/', methods=['GET'])
# def get_favoritos_usuario(usuario_id):
    
#     usuario_favoritos = Favoritos.query.filter_by(usuario_id=usuario_id).all()
#     results = list(map(lambda item: item.serialize(),usuario_favoritos))
#     print(results)
#     return jsonify(results), 200

# Acá va el POST de USUARIO POR PLANETA FAVORITO
@app.route('/usuario/<int:usuario_id>/favoritos/planetas', methods=['POST'])
def add_new_favourite_planet(usuario_id):
    request_body = request.json
    print(request_body)
    print(usuario_id)
    new_favorito = Favoritos(usuario_id=usuario_id, planetas_id=request_body["planetas_id"])
    db.session.add(new_favorito)
    db.session.commit()
    usuario = Favoritos.query.filter_by(usuario_id=usuario_id).first()
    print(usuario)
    return jsonify(request_body),200

# Acá va el POST de USUARIO POR PERSONAJE FAVORITO
@app.route('/usuario/<int:usuario_id>/favoritos/personajes', methods=['POST'])
def add_new_favourite_personajes(usuario_id):
    request_body = request.json
    print(request_body)
    print(usuario_id)
    new_favorito_to_personajes = Favoritos(usuario_id=usuario_id, personajes_id=request_body["personajes_id"])
    db.session.add(new_favorito_to_personajes)
    db.session.commit()
    usuario_personajes = Favoritos.query.filter_by(usuario_id=usuario_id).first()
    print(usuario_personajes)
    return jsonify(request_body),200

# ACÁ COMIENZAN LOS DELETES DE PERSONAJES
@app.route('/usuario/<int:usuario_id>/favoritos/personajes', methods=['DELETE'])
def eliminar_new_favourite_personajes(usuario_id):
    request_body = request.json
    print(request_body)
    print(usuario_id)
    query_personajes = Favoritos.query.filter_by(usuario_id=usuario_id, personajes_id=request_body["personaje_id"]).first()
    print(query_personajes)
    if query_personajes is None:
        return jsonify({"msg":"No hubo coincidencias, no hay nada para eliminar"}),404
    db.session.delete(query_personajes)
    db.session.commit()
    # print(usuario_personajes_eliminar)
    return jsonify({"msg":"El favorito ha sido eliminado correctamente"}),200

# ACÁ VAN LOS DELETES DE PLANETAS
@app.route('/usuario/<int:usuario_id>/favoritos/planetas', methods=['DELETE'])
def eliminar_new_favourite_planet(usuario_id):
    request_body = request.json
    print(request_body)
    print(usuario_id)
    query= Favoritos.query.filter_by(usuario_id=usuario_id,planetas_id=request_body["planeta_id"]).first()
    print(query)
    if query is None:
        return jsonify({"msg":"No hubo coincidencias, no hay nada para eliminar"}),404
    db.session.delete(query)
    db.session.commit() 
    return jsonify({"msg":"El favorito ha sido eliminado correctamente"}),200



#terminan los endpoints

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
