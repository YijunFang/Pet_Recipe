from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import MetaData
from flask_login import AnonymousUserMixin

class User(Base):
	# this line ccreates class variables
	# automatically from .db file
    __table__ = Base.metadata.tables['user']

    """
    id = __table__.c.id
    password = __table__.c.password
    authenticated = __table__.c.authenticated
    """

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return bool(self.authenticated)

class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Guest'
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return False

class Comment(Base):
	__table__ = Base.metadata.tables['comment']

class Favourite(Base):
	__table__ = Base.metadata.tables['favourite']

class Follow(Base):
    __table__ = Base.metadata.tables['follow']

class Pet(Base):
	__table__ = Base.metadata.tables['pet']

class Pet_type(Base):
	__table__ = Base.metadata.tables['pet_type']

class Recipe(Base):
	__table__ = Base.metadata.tables['recipe']
	def __init__(self, *args, **kwargs):
		super(Recipe, self).__init__(**kwargs)
