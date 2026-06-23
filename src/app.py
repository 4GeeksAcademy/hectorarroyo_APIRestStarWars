"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planeta, Personaje, Favorito
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

CURRENT_USER_ID = 1


# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoints


@app.route('/users', methods=['GET'])
def get_usuarios():
    try:
        query_results = User.query.all()

        if not query_results:
            return jsonify({"msg": "usuarios no encontrados"}), 400

        results = list(map(lambda item: item.serialize(), query_results))

        response_body = {
            "msg": "lista de usuarios encontrada",
            "results": results
        }

        return jsonify(response_body), 200

    except Exception as error:
        print(f"Error al obtener los usuarios: {error}")
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500


@app.route('/users/favorites', methods=['GET'])
def get_favoritos_usuario():
    try:
        query_results = Favorito.query.filter_by(user_id=CURRENT_USER_ID).all()

        if not query_results:
            return jsonify({"msg": "favoritos no encontrados"}), 400

        results = list(map(lambda item: item.serialize(), query_results))

        response_body = {
            "msg": "lista de favoritos encontrada",
            "results": results
        }

        return jsonify(response_body), 200

    except Exception as error:
        print(f"Error al obtener los favoritos: {error}")
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500


# Personajes
@app.route('/people', methods=['GET'])
def get_people():
    try:
        query_results = Personaje.query.all()

        if not query_results:
            return jsonify({"msg": "personajes no encontrados"}), 400

        results = list(map(lambda item: item.serialize(), query_results))

        response_body = {
            "msg": "lista de personajes encontrada",
            "results": results
        }

        return jsonify(response_body), 200

    except Exception as error:
        print(f"Error al obtener los personajes: {error}")
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500


@app.route('/people/<int:people_id>', methods=['GET'])
def get_personaje(people_id):
    try:
        query_result = Personaje.query.get(people_id)

        if not query_result:
            return jsonify({"msg": "personaje no encontrado"}), 400

        response_body = {
            "msg": "personaje encontrado",
            "result": query_result.serialize()
        }

        return jsonify(response_body), 200

    except Exception as error:
        print(f"Error al obtener el personaje: {error}")
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500


# Planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    try:
        query_results = Planeta.query.all()

        if not query_results:
            return jsonify({"msg": "planetas no encontrados"}), 400

        results = list(map(lambda item: item.serialize(), query_results))

        response_body = {
            "msg": "lista de planetas encontrada",
            "results": results
        }

        return jsonify(response_body), 200

    except Exception as error:
        print(f"Error al obtener los planetas: {error}")
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planeta(planet_id):
    try:
        query_result = Planeta.query.get(planet_id)

        if not query_result:
            return jsonify({"msg": "planeta no encontrado"}), 400

        response_body = {
            "msg": "planeta encontrado",
            "result": query_result.serialize()
        }

        return jsonify(response_body), 200

    except Exception as error:
        print(f"Error al obtener el planeta: {error}")
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500

# Favoritos


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorito_planeta(planet_id):
    try:
        planeta = Planeta.query.get(planet_id)

        if not planeta:
            return jsonify({"msg": "planeta no encontrado"}), 400

        ya_existe = Favorito.query.filter_by(
            user_id=CURRENT_USER_ID,
            planeta_id=planet_id
        ).first()

        if ya_existe:
            return jsonify({"msg": "este planeta ya está en favoritos"}), 400

        nuevo_favorito = Favorito(
            user_id=CURRENT_USER_ID,
            planeta_id=planet_id,
            personaje_id=None
        )

        db.session.add(nuevo_favorito)
        db.session.commit()

        response_body = {
            "msg": "planeta añadido a favoritos",
            "result": nuevo_favorito.serialize()
        }

        return jsonify(response_body), 201

    except Exception as error:
        db.session.rollback()
        print(f"Error al añadir planeta a favoritos: {error}")
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorito_personaje(people_id):
    try:
        personaje = Personaje.query.get(people_id)

        if not personaje:
            return jsonify({"msg": "personaje no encontrado"}), 400

        ya_existe = Favorito.query.filter_by(
            user_id=CURRENT_USER_ID,
            personaje_id=people_id
        ).first()

        if ya_existe:
            return jsonify({"msg": "este personaje ya está en favoritos"}), 400

        nuevo_favorito = Favorito(
            user_id=CURRENT_USER_ID,
            planeta_id=None,
            personaje_id=people_id
        )

        db.session.add(nuevo_favorito)
        db.session.commit()

        response_body = {
            "msg": "personaje añadido a favoritos",
            "result": nuevo_favorito.serialize()
        }

        return jsonify(response_body), 201

    except Exception as error:
        db.session.rollback()
        print(f"Error al añadir personaje a favoritos: {error}")
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorito_planeta(planet_id):
    try:
        favorito = Favorito.query.filter_by(
            user_id=CURRENT_USER_ID,
            planeta_id=planet_id
        ).first()

        if not favorito:
            return jsonify({"msg": "favorito no encontrado"}), 400

        db.session.delete(favorito)
        db.session.commit()

        response_body = {
            "msg": "planeta eliminado de favoritos"
        }

        return jsonify(response_body), 200

    except Exception as error:
        db.session.rollback()
        print(f"Error al eliminar planeta de favoritos: {error}")
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorito_personaje(people_id):
    try:
        favorito = Favorito.query.filter_by(
            user_id=CURRENT_USER_ID,
            personaje_id=people_id
        ).first()

        if not favorito:
            return jsonify({"msg": "favorito no encontrado"}), 400

        db.session.delete(favorito)
        db.session.commit()

        response_body = {
            "msg": "personaje eliminado de favoritos"
        }

        return jsonify(response_body), 200

    except Exception as error:
        db.session.rollback()
        print(f"Error al eliminar personaje de favoritos: {error}")
        return jsonify({"msg": "Internal Server Error", "error": str(error)}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
