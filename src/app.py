
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Personajes, Planetas, Favorito, Vehiculos, Usuario
import json
# from models import Person

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

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# Endpoints INICIO


"""-----------------------------------------------_<People>_-------------------------------------"""

@app.route('/people', methods=['GET'])
def handle_people():
    all_people = Personajes.query.all()
    people_list = [p.serialize() for p in all_people]

    if not people_list:
        return jsonify({'msj': 'no hay personajes'}), 404

    return jsonify(people_list), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def handle_people_id(people_id):
    one_person = Personajes.query.filter_by(id=people_id).first()

    if not one_person:
        return jsonify({'msj': 'El personaje no existe'}), 404

    return jsonify(one_person.serialize()), 200


@app.route('/people', methods=['POST'])
def create_people():
    try:
        request_body = request.get_json()
        if not request_body:
            return jsonify({"message": "Solicitud JSON inválida"}), 400

        required_fields = ['name', 'mass', 'hair_color', 'skin_color',
                           'eye_color', 'birth_year', 'gender', 'height']
        missing_fields = [field for field in required_fields if field not in request_body]
        if missing_fields:
            return jsonify({"message": f"Faltan los campos: {', '.join(missing_fields)}"}), 400

        existing_person = Personajes.query.filter_by(name=request_body["name"]).first()

        if existing_person:
            return jsonify({"message": "El personaje ya existe"}), 409  

        new_person = Personajes(
            name=request_body['name'],
            mass=request_body['mass'],
            hair_color=request_body['hair_color'],
            skin_color=request_body['skin_color'],
            eye_color=request_body['eye_color'],
            birth_year=request_body['birth_year'],
            gender=request_body['gender'],
            height=request_body['height']
        )
        db.session.add(new_person)
        db.session.commit()
        return jsonify(new_person.serialize()), 201  

    except KeyError as ke:
        return jsonify({"message": f"Falta el campo: {str(ke)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500


@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    try:
        existing_person = Personajes.query.filter_by(id=people_id).first()

        if existing_person:
            db.session.delete(existing_person)
            db.session.commit()
            return jsonify({"message": "El personaje ha sido eliminado"}), 200

        return jsonify({"message": "El personaje que intenta eliminar no existe"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500


@app.route('/users/favorites/people/<int:people_id>', methods=['POST'])
def create_fav_people(people_id):
    try:
        
        usuario_id = 1

        if not Usuario.query.filter_by(id=usuario_id).first():
            return jsonify({"message": "El usuario al que le quiere añadir un favorito no existe"}), 404

        if not Personajes.query.filter_by(id=people_id).first():
            return jsonify({"message": "El personaje que quiere añadir a favoritos no existe"}), 404

        existing_favorito = Favorito.query.filter_by(personajes_id=people_id, usuario_id=usuario_id).first()

        if existing_favorito:
            return jsonify({"message": "El personaje ya está en favoritos"}), 409  # Changed to 409 Conflict

        new_favorito = Favorito(
            usuario_id=usuario_id,
            personajes_id=people_id,
            vehiculos_id=None,
            planetas_id=None
        )
        db.session.add(new_favorito)
        db.session.commit()

        print(new_favorito.serialize())
        return jsonify(new_favorito.serialize()), 201 

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500


@app.route('/users/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people(people_id):
    try:
        
        usuario_id = 1

        existing_favorito = Favorito.query.filter_by(personajes_id=people_id, usuario_id=usuario_id).first()

        if existing_favorito:
            db.session.delete(existing_favorito)
            db.session.commit()
            return jsonify({"message": "El personaje ha sido eliminado de favoritos"}), 200

        if not Usuario.query.filter_by(id=usuario_id).first():
            return jsonify({"message": "El usuario no existe"}), 404

        if not Personajes.query.filter_by(id=people_id).first():
            return jsonify({"message": "El personaje que quiere eliminar de favoritos no existe"}), 404

        return jsonify({"message": "El personaje no está en favoritos"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500


"""-----------------------------------------------_<People>_-------------------------------------"""

"""-----------------------------------------------_<Planets>_-------------------------------------"""


@app.route('/planets', methods=['GET'])
def handle_planets():
    all_planets = Planetas.query.all()
    planets_list = [p.serialize() for p in all_planets]

    if not planets_list:
        return jsonify({'msj': 'no hay planetas'}), 404

    return jsonify(planets_list), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_planet_id(planet_id):
    one_planet = Planetas.query.filter_by(id=planet_id).first()

    if not one_planet:
        return jsonify({'msj': 'El planeta no existe'}), 404

    return jsonify(one_planet.serialize()), 200


@app.route('/planets', methods=['POST'])
def create_planet():
    try:
        request_body = request.get_json()
        if not request_body:
            return jsonify({"message": "Solicitud JSON inválida"}), 400

        required_fields = ['name', 'diameter', 'rotation_period',
                           'orbital_period', 'gravity', 'population',
                           'climate', 'terrain', 'surface_water']
        missing_fields = [field for field in required_fields if field not in request_body]
        if missing_fields:
            return jsonify({"message": f"Faltan los campos: {', '.join(missing_fields)}"}), 400

        existing_planet = Planetas.query.filter_by(name=request_body["name"]).first()

        if existing_planet:
            return jsonify({"message": "El planeta ya existe"}), 409  

        new_planet = Planetas(
            name=request_body['name'],
            diameter=request_body['diameter'],
            rotation_period=request_body['rotation_period'],
            orbital_period=request_body['orbital_period'],
            gravity=request_body['gravity'],
            population=request_body['population'],
            climate=request_body['climate'],
            terrain=request_body['terrain'],
            surface_water=request_body['surface_water']
        )
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(new_planet.serialize()), 201  

    except KeyError as ke:
        return jsonify({"message": f"Falta el campo: {str(ke)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500


@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    try:
        existing_planet = Planetas.query.filter_by(id=planet_id).first()

        if existing_planet:
            db.session.delete(existing_planet)
            db.session.commit()
            return jsonify({"message": "El planeta ha sido eliminado"}), 200

        return jsonify({"message": "El planeta que intenta eliminar no existe"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500


@app.route('/users/favorites/planet/<int:planet_id>', methods=['POST'])
def create_fav_planet(planet_id):
    try:
        
        usuario_id = 1

        if not Usuario.query.filter_by(id=usuario_id).first():
            return jsonify({"message": "El usuario al que le quiere añadir un favorito no existe"}), 404

        if not Planetas.query.filter_by(id=planet_id).first():
            return jsonify({"message": "El planeta que quiere añadir a favoritos no existe"}), 404

        existing_favorito = Favorito.query.filter_by(planetas_id=planet_id, usuario_id=usuario_id).first()

        if existing_favorito:
            return jsonify({"message": "El planeta ya está en favoritos"}), 409  

        new_favorito = Favorito(
            usuario_id=usuario_id,
            personajes_id=None,
            vehiculos_id=None,
            planetas_id=planet_id
        )
        db.session.add(new_favorito)
        db.session.commit()

        print(new_favorito.serialize())
        return jsonify(new_favorito.serialize()), 201  

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500


@app.route('/users/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    try:
        
        usuario_id = 1

        existing_favorito = Favorito.query.filter_by(planetas_id=planet_id, usuario_id=usuario_id).first()

        if existing_favorito:
            db.session.delete(existing_favorito)
            db.session.commit()
            return jsonify({"message": "El planeta ha sido eliminado de favoritos"}), 200

        if not Usuario.query.filter_by(id=usuario_id).first():
            return jsonify({"message": "El usuario no existe"}), 404

        if not Planetas.query.filter_by(id=planet_id).first():
            return jsonify({"message": "El planeta que quiere eliminar de favoritos no existe"}), 404

        return jsonify({"message": "El planeta no está en favoritos"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500


"""-----------------------------------------------_<Planets>_-------------------------------------"""

"""-----------------------------------------------_<Vehicles>_-------------------------------------"""


@app.route('/vehicles', methods=['GET'])
def handle_vehicles():
    all_vehicles = Vehiculos.query.all()
    vehicles_list = [v.serialize() for v in all_vehicles]

    if not vehicles_list:
        return jsonify({'msj': 'no hay vehiculos'}), 404

    return jsonify(vehicles_list), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def handle_vehicle_id(vehicle_id):
    one_vehicle = Vehiculos.query.filter_by(id=vehicle_id).first()

    if not one_vehicle:
        return jsonify({'msj': 'El vehiculo no existe'}), 404

    return jsonify(one_vehicle.serialize()), 200


@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    try:
        request_body = request.get_json()
        if not request_body:
            return jsonify({"message": "Solicitud JSON inválida"}), 400

        required_fields = [
            'name', 'model', 'vehicle_class', 'manufacturer',
            'cost_in_credits', 'length', 'crew', 'passengers',
            'max_atmosphering_speed', 'cargo_capacity',
            'consumables', 'films', 'pilots'
        ]
        missing_fields = [field for field in required_fields if field not in request_body]
        if missing_fields:
            return jsonify({"message": f"Faltan los campos: {', '.join(missing_fields)}"}), 400

        existing_vehicle = Vehiculos.query.filter_by(name=request_body["name"]).first()

        if existing_vehicle:
            return jsonify({"message": "El vehiculo ya existe"}), 409  

        new_vehicle = Vehiculos(
            name=request_body['name'],
            model=request_body['model'],
            vehicle_class=request_body['vehicle_class'],
            manufacturer=request_body['manufacturer'],
            cost_in_credits=request_body['cost_in_credits'],
            length=request_body['length'],
            crew=request_body['crew'],
            passengers=request_body['passengers'],
            max_atmosphering_speed=request_body['max_atmosphering_speed'],
            cargo_capacity=request_body['cargo_capacity'],
            consumables=request_body['consumables'],
            films=json.dumps(request_body['films']),    
            pilots=json.dumps(request_body['pilots'])   
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify(new_vehicle.serialize()), 201  

    except KeyError as ke:
        return jsonify({"message": f"Falta el campo: {str(ke)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500


@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    try:
        existing_vehicle = Vehiculos.query.filter_by(id=vehicle_id).first()

        if existing_vehicle:
            db.session.delete(existing_vehicle)
            db.session.commit()
            return jsonify({"message": "El vehiculo ha sido eliminado"}), 200

        return jsonify({"message": "El vehiculo que intenta eliminar no existe"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500


@app.route('/users/favorites/vehicle/<int:vehicle_id>', methods=['POST'])
def create_fav_vehicle(vehicle_id):
    try:
       
        usuario_id = 1

        if not Usuario.query.filter_by(id=usuario_id).first():
            return jsonify({"message": "El usuario al que le quiere añadir un favorito no existe"}), 404

        if not Vehiculos.query.filter_by(id=vehicle_id).first():
            return jsonify({"message": "El vehiculo que quiere añadir a favoritos no existe"}), 404

        existing_favorito = Favorito.query.filter_by(vehiculos_id=vehicle_id, usuario_id=usuario_id).first()

        if existing_favorito:
            return jsonify({"message": "El vehiculo ya está en favoritos"}), 409  

        new_favorito = Favorito(
            usuario_id=usuario_id,
            personajes_id=None,
            vehiculos_id=vehicle_id,
            planetas_id=None
        )
        db.session.add(new_favorito)
        db.session.commit()

        print(new_favorito.serialize())
        return jsonify(new_favorito.serialize()), 201  

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500


@app.route('/users/favorites/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_fav_vehicle(vehicle_id):
    try:
        
        usuario_id = 1

        existing_favorito = Favorito.query.filter_by(vehiculos_id=vehicle_id, usuario_id=usuario_id).first()

        if existing_favorito:
            db.session.delete(existing_favorito)
            db.session.commit()
            return jsonify({"message": "El vehiculo ha sido eliminado de favoritos"}), 200

        if not Usuario.query.filter_by(id=usuario_id).first():
            return jsonify({"message": "El usuario no existe"}), 404

        if not Vehiculos.query.filter_by(id=vehicle_id).first():
            return jsonify({"message": "El vehiculo que quiere eliminar de favoritos no existe"}), 404

        return jsonify({"message": "El vehiculo no está en favoritos"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error interno del servidor: {str(e)}"}), 500


"""-----------------------------------------------_<Vehicles>_-------------------------------------"""

"""-----------------------------------------------_<Users>_-------------------------------------"""

@app.route('/users', methods=['GET'])
def handle_users():
    all_users = Usuario.query.all()
    users_list = [u.serialize() for u in all_users]

    if not users_list:
        return jsonify({'msj': 'no hay usuarios'}), 404

    return jsonify(users_list), 200


@app.route('/users/favorites', methods=['GET'])
def handle_user_favorites():
    
    usuario_id = 1

    all_favorites = Favorito.query.filter_by(usuario_id=usuario_id).all()
    favorites_list = [f.serialize() for f in all_favorites]
    print(favorites_list)

    if not favorites_list:
        return jsonify({'msj': 'no hay favoritos'}), 404

    return jsonify({'results': favorites_list}), 200


@app.route('/favorites', methods=['GET'])
def handle_favorites():
    all_favorites = Favorito.query.all()
    favorites_list = [f.serialize() for f in all_favorites]

    if not favorites_list:
        return jsonify({'msj': 'no hay favoritos'}), 404

    return jsonify(favorites_list), 200

"""-----------------------------------------------_<Users>_-------------------------------------"""


    # Endpoints FINAL

@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response"
    }

    return jsonify(response_body), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
