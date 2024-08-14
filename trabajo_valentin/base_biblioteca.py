from peewee import *


mibase = SqliteDatabase('biblioteca_pw.db')


class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mibase


class Biblioteca(BaseModel):
    titulo = CharField(unique=True)
    autor = CharField()
    isbn= IntegerField(unique=True)
    anio= IntegerField()


mibase.connect()
mibase.create_tables([Biblioteca])
