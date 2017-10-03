from app.database import Base

class User(Base):
	# this line ccreates class variables
	# automatically from .db file
    __table__ = Base.metadata.tables['user']
    def __init__(self
                 , UserName
                 , Password
                 ):
        self.UserName = UserName
        self.Password = Password

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
