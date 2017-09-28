from flask import Flask, render_template, request
# from Pet_Recipe.LoginForm import LoginForm
# from main import app
from .forms import LoginForm
from sqlalchemy import or_
app = Flask(__name__)
app.debug = True
app.secret_key = 's3cr3t'

from app.database import db_session,engine
from app.models import *

@app.route('/')
def index():
	recipes = db_session.query(Recipe,Pet_type,User).filter(Recipe.type==Pet_type.id). \
							 filter(Recipe.user_id==User.id).all()

	#return render_template("home_alt.html",recipes=recipes) # uncomment for old version
	                                                         # we may reuse this for logged
	                                                         # in users' feed
	return render_template("home_alt.html",recipes=recipes)  

def search_view():
	search_term = request.form['search_term']
	search_filter = request.form['search_filter']
	pet_type = Pet_type.query.all()

	user = []
	recipes = []

	#search users
	if search_filter=='Users' or search_filter=='Everything':
		user = db_session.query(User).filter(User.user_name.contains(search_term)).all()
	#search for search_term in recipe title,instruction & ingredients
	if search_filter=='Recipes' or search_filter=='Everything':
		recipes = db_session.query(Recipe,Pet_type,User).\
							 filter(Recipe.type==Pet_type.id). \
							 filter(Recipe.user_id==User.id). \
							 filter(or_(Recipe.title.contains(search_term), \
							 	        Recipe.ingredient.contains(search_term), \
							 	        Recipe.instruction.contains(search_term))).all()
	#search based on pet filter
	# reference for querying db based on list of checkbox values
	# https://stackoverflow.com/questions/41741224/multiple-checkbox-sqlalchemy-delete
	selected_pets = request.form.getlist('pet_filter')
	print(selected_pets)	

	return render_template("result_page.html",search_term=search_term, search_filter=search_filter, \
		                    pet_type=pet_type, recipes=recipes, user = user, ) 

@app.route('/profile')
def profile_view():    
	return render_template("profile_test.html")  

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
        title = 'Sign In',
        form = form)

@app.route('/recipe')
def recipe_view():  
	recipeid = request.args.get('recipeid')
	title = request.args.get('title')
	ingredient = request.args.get('ingredient')
	instruction = request.args.get('instruction')
	pettype= request.args.get('pettype')
	user= request.args.get('user')
	img= request.args.get('img')

	return render_template("recipe.html",
		recipeid=recipeid,
		title=title,
		ingredient=ingredient,
		instruction=instruction,
		pettype=pettype,
		user=user,
		img=img)

if __name__ == '__main__':
	#print "lol"
	app.run(debug=True, host='127.0.0.1')

