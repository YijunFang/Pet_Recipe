from __future__ import print_function
import sys
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
	return render_template("profile_test.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		print('in post')

		username = request.form['username']
		password = request.form['password']
		print('in post after')

		print('Users '+ username)
		print('psd '+ password)

		return render_template('login.html')

		# return Response('login.html')

		# registeredUser = users_repository.get_user(username)
		# print('Users '+ str(users_repository.users))
		# print('Register user %s , password %s' % (registeredUser.username, registeredUser.password))
		# if registeredUser != None and registeredUser.password == password:
		#     print('Logged in..')
		#     login_user(registeredUser)
		#     return redirect(url_for('home'))
		# else:
		#     return abort(401)
	else:
		# print('login get')

		return render_template('login.html')
# class User(UserMixin):
#     pass
#     # user object        
#     @login_manager.user_loader
#     def user_loader(username):
#         if query_user(username):
#             user = User()
#             user.id = username
#             return user
#         return None

#     def query_user(username):
#         user = UserAccounts.query.filter_by(user_name=username).first()
#         if user:
#             return True
#         return False


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
