#!flask/bin/python
from app import app
from app.views import *
app.run(debug=True)
