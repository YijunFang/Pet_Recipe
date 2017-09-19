from flask import Flask, render_template, request
# from Pet_Recipe.LoginForm import LoginForm
# from main import app
from .forms import LoginForm

app = Flask(__name__)
app.debug = True
app.secret_key = 's3cr3t'

from app.database import db_session,engine
from app.models import User,Recipe

@app.route('/')
def index():
	"""
		example code for selecting (call query in sqlalchemy)
		
	for item in db_session.query(Recipe.id, Recipe.ingredient,Recipe.instruction):
		print (item)
	"""
	recipes = db_session.query(Recipe).all()
	print(recipes)

	return render_template("home.html",recipes=recipes)  

@app.route('/search',methods=['POST'])
def search_view():
	search_term = request.form['search_term']   
	return render_template("search_test.html",search_term=search_term) 

@app.route('/profile')
def profile_view():    
	return render_template("profile_test.html")  

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
        title = 'Sign In',
        form = form)

if __name__ == '__main__':
	#print "lol"
	app.run(debug=True, host='127.0.0.1')

