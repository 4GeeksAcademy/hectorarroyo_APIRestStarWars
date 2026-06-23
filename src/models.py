from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date


db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    apellido: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    fecha_suscripcion: Mapped[date] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    # relaciones
    favoritos = relationship("Favorito", backref="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "fecha_suscripcion": self.fecha_suscripcion,
            # do not serialize the password, its a security breach
        }


class Planeta(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    clima: Mapped[str] = mapped_column(String(120), nullable=False)
    diametro: Mapped[float] = mapped_column(nullable=False)

    favoritos = relationship("Favorito", backref="planeta")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "diametro": self.diametro,
        }


class Personaje(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    birth_year: Mapped[date] = mapped_column(nullable=False)
    genero: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    favoritos = relationship("Favorito", backref="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "birth_year": self.birth_year,
            "genero": self.genero,
        }


class Favorito(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)

    planeta_id: Mapped[int] = mapped_column(
        ForeignKey("planeta.id"), nullable=True)

    personaje_id: Mapped[int] = mapped_column(
        ForeignKey("personaje.id"), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planeta_id": self.planeta_id,
            "personaje_id": self.personaje_id,
        }
