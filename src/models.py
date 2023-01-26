from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }

class Usuario(db.Model):
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    password= db.Column(db.String(20), nullable=False)
    email= db.Column(db.String(30), nullable=False)
    favoritos_usuario = db.relationship('Favoritos', backref='usuario', lazy=True)
    # favoritos_id = Column(Integer, ForeignKey('favoritos.id'))
    # favoritos = relationship(Favoritos)
    def __repr__(self):
        return '<Usuario %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Personajes(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    apellido = db.Column(db.String(250), nullable=False)
    genero = db.Column(db.String(250), nullable=False)
    color_piel = db.Column(db.String(250), nullable=False)
    color_pelo = db.Column(db.String(250), nullable=False)
    color_ojos = db.Column(db.String(250), nullable=False)
    fecha_nacimiento = db.Column(db.String(250), nullable=False)
    favoritos_personajes = db.relationship('Favoritos', backref='personajes', lazy=True)
    # favoritos = relationship(Favoritos)
    def __repr__(self):
        return '<Usuario %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "genero": self.genero,
            "color_piel": self.color_piel,
            "color_pelo": self.color_pelo,
            "color_ojos": self.color_ojos,
            "fecha_nacimiento": self.fecha_nacimiento
            # do not serialize the password, its a security breach
        }

class Favoritos(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    # agregar = db.Column(db.String(250), nullable=False)
    # eliminar = db.Column(db.String(250), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    personajes_id = db.Column(db.Integer, db.ForeignKey('personajes.id'))
    # usuario = relationship(Usuario)
    planetas_id = db.Column(db.Integer, db.ForeignKey('planetas.id'))
    # planetas = relationship(Usuario)
    vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    # vehicles = relationship(Usuario)
    # personajes = relationship(Usuario)
    def __repr__(self):
        return '<Favoritos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            # "agregar": self.agregar,
            # "eliminar": self.eliminar
            # do not serialize the password, its a security breach
        }

class Planetas(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    poblacion = db.Column(db.String(250))
    terreno = db.Column(db.String(250))
    favoritos_planetas = db.relationship('Favoritos', backref='planetas', lazy=True)
    # favoritos = relationship(Favoritos)
    def __repr__(self):
        return '<Planetas %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "poblacion": self.poblacion,
            "terreno": self.terreno
            # do not serialize the password, its a security breach
        }

class Vehicles(db.Model):
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    modelo = db.Column(db.String(250))
    año_creacion= db.Column(db.String(250))
    capacidad = db.Column(db.String(250), nullable=False)
    favoritos_vehicles= db.relationship('Favoritos', backref='vehicles', lazy=True)
    # favoritos = relationship(Favoritos)
    def __repr__(self):
        return '<Vehicles %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "modelo": self.modelo,
            "año_creacion": self.año_creacion,
            "capacidad": self.capacidad
            # do not serialize the password, its a security breach
        }