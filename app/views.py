from __future__ import print_function
import sys
import re
import logging
logging.basicConfig(level=logging.DEBUG)


from flask import Flask, render_template, request,redirect
# from Pet_Recipe.LoginForm import LoginForm
# from main import app
from .forms import LoginForm
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 

from sqlalchemy import or_
app = Flask(__name__)
app.debug = True
app.secret_key = 's3cr3t'

from app.database import db_session,engine
from app.models import *


# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.anonymous_user = Anonymous

user_id = None
current_user = Anonymous

@app.route('/')
def index():

	recipes = db_session.query(Recipe,Pet_type,User).filter(Recipe.type==Pet_type.id). \
							 filter(Recipe.user_id==User.id).all()

	#return render_template("home_alt.html",recipes=recipes) # uncomment for old version
															 # we may reuse this for logged
															 # in users' feed
	return render_template("home_alt.html",recipes=recipes)

@app.route('/search',methods=['PUT','GET'])
def search_view_put():
	print("search_view")
	return redirect('/')

@app.route('/search',methods=['POST'])
def search_view():
	# print("search_view")
	search_term = request.form['search_term']
	if len(search_term) == 0 or search_term == "":
		return index()

	search_filter = request.form['search_filter']
	pet_type = Pet_type.query.all()

	user = []
	recipes = []

	#search based on pet filter
	selected_pets = request.form.getlist('pet_filter')
	if selected_pets != "" and len(selected_pets) != 0:
		query_pet_type = db_session.query(Pet_type).\
							filter(Pet_type.type.in_(selected_pets)).all()
		print("query_pet_type: "),
		for pet_t in query_pet_type:
			print(str(pet_t.id)+" "),
			pet_t = str(pet_t)
		print

		recipes = db_session.query(Recipe,Pet_type,User).\
								 filter(Recipe.type==Pet_type.id). \
								 filter(Recipe.user_id==User.id). \
								 filter(Pet_type.type.in_(selected_pets)).\
								 filter(or_(Recipe.title.contains(search_term), \
											Recipe.ingredient.contains(search_term), \
											Recipe.instruction.contains(search_term))).all()

	else:
		# #search users
		if search_filter=='Users' or search_filter=='Everything':
			user = db_session.query(User).filter(User.user_name.contains(search_term)).all()
		#search for search_term in recipe title,instruction & ingredients
		if search_filter=='Recipes' or search_filter=='Everything':
			recipes = db_session.query(Recipe,Pet_type,User).\
								 filter(Recipe.type==Pet_type.id). \
								 filter(Recipe.user_id==User.id). \
								 filter(or_(Pet_type.type.contains(search_term),\
											Recipe.title.contains(search_term), \
											Recipe.ingredient.contains(search_term), \
											Recipe.instruction.contains(search_term))).all()

	print("search_filter: "+search_filter)
	print("selected_pets: "),
	print(selected_pets)
	print("pet_type: "),
	for i in pet_type:
		print(i.type+" "),
	print
	print("recipes: "),
	for i in recipes:
		print(i[0].type),
	print
	print("user:"),
	print(user)
	print("============")
	return render_template("result_page.html",search_term=search_term, search_filter=search_filter, \
							pet_type=pet_type, recipes=recipes, user = user, )

@app.route('/profile')
def profile_view():
	print("In profile")
	print(current_user)
	return render_template("profile_test.html")

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		print('in post')

		username = request.form['username']
		password = request.form['password']

		u = db_session.query(User).filter_by(user_name= username).first()
		if (u is None) :
			# signup page
			return render_template('login_err.html')

		elif u.password == password:
			print("login success")
			user_id = u.id
			login_user(u)
			current_user = u
			return render_template('home.html')
		else:
			# print('u obj '+ str(u.user_name))
			return render_template('login_err.html')

	else:
		return render_template('login.html')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    """Logout the current user."""
    # removed these lines because it causes server to fail on mulitple users
    #user = current_user
    #user.authenticated = False
    logout_user()
    return render_template("logout.html")

@app.route('/register', methods = ['GET', 'POST'])
def register():
	if request.method == 'POST':
		print('in post')

		password = request.form['password']
		c_password = request.form['c_password']
		c_password = request.form['c_password']
		email = request.form['email']
		username = request.form['username']
		u = db_session.query(User).filter_by(user_name= username).first()
		if not password or not username or not email or not password == c_password or not bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email)) :
			return render_template('register_err.html')
		elif (u is not None) :
			return render_template('register_err_u.html')
		else: 
			# engine.execute('INSERT INTO "user" ''(user_name,password,email) ''VALUES ("s1","raw1","a@gmail.com")') 
			meta = MetaData(engine,reflect=True)
			table = meta.tables['user']

			ins = table.insert().values(user_name=username, password = password, email= email, authenticated=0 ) 
			conn = engine.connect() 
			conn.execute(ins)
			
			u = db_session.query(User).filter_by(user_name= username).first()
			user_id = u.id
			print ('success')
			return render_template('home.html')

	else:
		return render_template('register.html')

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