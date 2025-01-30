from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return f'<User {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    apellido = db.Column(db.String(120), nullable=False)
    email  = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    usuario_favoritos = relationship('Favorito', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "password": self.password,
            "usuario_favoritos": [item.serialize() for item in self.usuario_favoritos]
        }

class Personajes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    mass = db.Column(db.String(120), nullable=False)
    hair_color = db.Column(db.String(120), nullable=False)
    skin_color = db.Column(db.String(120), nullable=False)
    eye_color = db.Column(db.String(120), nullable=False)
    birth_year = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    height = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Personajes {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height
        }

class Planetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    diameter = db.Column(db.String(120), nullable=False)
    rotation_period = db.Column(db.String(120), nullable=False)
    orbital_period = db.Column(db.String(120), nullable=False)
    gravity = db.Column(db.String(120), nullable=False)
    population = db.Column(db.String(120), nullable=False)
    climate = db.Column(db.String(120), nullable=False)
    terrain = db.Column(db.String(120), nullable=False)
    surface_water = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Planetas {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }

class Vehiculos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    model = db.Column(db.String(120), unique=True, nullable=False)
    vehicle_class = db.Column(db.String(120), nullable=False)
    manufacturer = db.Column(db.String(120), nullable=False)
    cost_in_credits = db.Column(db.String(120), nullable=False)
    length = db.Column(db.String(120), nullable=False)
    crew = db.Column(db.String(120), nullable=False)
    passengers = db.Column(db.String(120), nullable=False)
    max_atmosphering_speed = db.Column(db.String(120), nullable=False)
    cargo_capacity = db.Column(db.String(120), nullable=False)
    consumables = db.Column(db.String(120), nullable=False)
    films = db.Column(db.String(120), nullable=False)
    pilots = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Vehiculos {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "films": self.films,
            "pilots": self.pilots
        }

class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    personajes_id = Column(Integer, ForeignKey('personajes.id'))
    personajes = relationship(Personajes)
    vehiculos_id = Column(Integer, ForeignKey('vehiculos.id'))
    vehiculos = relationship(Vehiculos)
    planetas_id = Column(Integer, ForeignKey('planetas.id'))
    planetas = relationship(Planetas)

    def __repr__(self):
        return f'<Favorito {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "personaje": self.personajes.serialize() if self.personajes else None,
            "vehiculo": self.vehiculos.serialize() if self.vehiculos else None,
            "planeta": self.planetas.serialize() if self.planetas else None
        }
