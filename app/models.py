from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import MetaData

class User(Base):
	# this line ccreates class variables
	# automatically from .db file
    __table__ = Base.metadata.tables['user']
    


class Comment(Base):
	__table__ = Base.metadata.tables['comment']

class Favourite(Base):
	__table__ = Base.metadata.tables['favourite']

class Pet(Base):
	__table__ = Base.metadata.tables['pet']

class Pet_type(Base):
	__table__ = Base.metadata.tables['pet_type']

class Recipe(Base):
	__table__ = Base.metadata.tables['recipe']
