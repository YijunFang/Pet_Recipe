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
    #     self.Password = self.psw_to_md5(Password)
    # @classmethod
    # def psw_to_md5(self, str_psw):
    #     import hashlib
    #     if str_psw == None:
    #         return None
    #     else:
    #         m = hashlib.md5(str_psw.encode(encoding='utf-8'))
    #         return m.hexdigest()
     

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
