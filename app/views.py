# for debug
from __future__ import print_function
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

from flask import Flask, render_template, request, Response
# from Pet_Recipe.LoginForm import LoginForm
# from main import app
from .forms import LoginForm
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 

from app.database import db_session,engine
from app.models import *



app = Flask(__name__)
app.debug = True
app.secret_key = 's3cr3t'

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/')
def index():
	"""
		example code for selecting (call query in sqlalchemy)
		
	for item in db_session.query(Recipe.id, Recipe.ingredient,Recipe.instruction):
		print (item)
	"""
	recipes = db_session.query(Recipe,Pet_type,User).filter(Recipe.type==Pet_type.id). \
							 filter(Recipe.user_id==User.id).all()
	
	# for a in recipes:
	# 	print(str(a.User))
	print('hello ')

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

if __name__ == '__main__':
	#print "lol"
	app.run(debug=True, host='127.0.0.1')

