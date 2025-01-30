import os
from flask_admin import Admin
from models import db, Planetas, Vehiculos, Favorito, Personajes, Usuario
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Agrega tus modelos aquí. Este es un ejemplo de cómo agregar el modelo Usuario al admin
    admin.add_view(ModelView(Planetas, db.session))
    admin.add_view(ModelView(Vehiculos, db.session))
    admin.add_view(ModelView(Favorito, db.session))
    admin.add_view(ModelView(Personajes, db.session))
    admin.add_view(ModelView(Usuario, db.session))

    # Puedes duplicar esa línea para agregar nuevos modelos
    # admin.add_view(ModelView(TuNuevoModelo, db.session))
