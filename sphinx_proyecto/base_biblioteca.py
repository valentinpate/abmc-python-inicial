"""
base_biblioteca.py
------------------

"""

import peewee


mibase = peewee.SqliteDatabase('biblioteca_pw.db')


class BaseModel(peewee.Model):
    """
    Modelo base para definir la base de datos
    """
    class Meta:
        database = mibase


class Biblioteca(BaseModel):

    """
    Clase que crea la tabla Biblioteca, la cual tendra como campos:

    - titulo (CharField): Título del libro (único).

    - autor (CharField): Autor del libro.

    - isbn (IntegerField): ISBN del libro (único).

    - anio (IntegerField): Año de publicación del libro.
    """

    titulo = peewee.CharField(unique=True)
    autor = peewee.CharField()
    isbn = peewee.IntegerField(unique=True)
    anio = peewee.IntegerField()


mibase.connect()
mibase.create_tables([Biblioteca])
