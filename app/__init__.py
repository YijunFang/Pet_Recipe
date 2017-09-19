from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import views

# start up the database using object models
# from models.py. import other classes as needed
from app.database import db_session,init_db,engine
init_db()
from sqlalchemy.orm import scoped_session, sessionmaker, Query
db_session = scoped_session(sessionmaker(bind=engine))

# auto disconnects the database when app exits
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()