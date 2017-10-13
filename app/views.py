from __future__ import print_function
import sys
import re
import logging
import os
logging.basicConfig(level=logging.DEBUG)


from flask import Flask, render_template, request,redirect,url_for
from werkzeug.utils import secure_filename
# from Pet_Recipe.LoginForm import LoginForm
# from main import app
from .forms import LoginForm
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

from sqlalchemy import or_

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

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


@app.route('/')
def index():
	#show logged in version of homepage with favorites
	if current_user.is_authenticated:
		recipes = db_session.query(Recipe,Pet_type,User).filter(Recipe.type==Pet_type.id). \
								 filter(Recipe.user_id==User.id).all()
		return redirect('/fave')

	#show guest version of homepage
	else:
		recipes = db_session.query(Recipe,Pet_type,User).filter(Recipe.type==Pet_type.id). \
								 filter(Recipe.user_id==User.id).all()
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

@app.route('/profile', methods = ['GET', 'POST'])
def profile_view():
	userid = request.args.get('userid')		
	if userid is None:
		if current_user.is_authenticated:
			userid = current_user.id
		else:
			return redirect('/')
	if User.query.get(userid) is None:
		userid = current_user.id	
	print(userid)
	print("In profile")
	#print(current_user.id)
	#print(userid)
	
	profile = db_session.query(User).filter(User.id==userid).all()

	pets = db_session.query(Pet,Pet_type). \
					filter(Pet.type==Pet_type.id). \
			  		filter(Pet.owner==userid).all()

	recipes = []
	recipes = db_session.query(Recipe,Pet_type). \
					filter(Recipe.user_id==userid).	\
					filter(Recipe.type==Pet_type.id). \
					all()
	if request.method == 'POST':
		print ("in post")

		recipe_id = request.form['delete']
		delete_recipe = db_session.query(Recipe).filter_by(id= recipe_id).first()
		db_session.delete(delete_recipe)
		db_session.commit()	
		return render_template("home.html")
	else:
		print(profile)
		return render_template("profile_test.html",profile=profile,recipes=recipes,pets=pets)


@app.route('/update_profile', methods = ['GET', 'POST'])
@login_required
def update_profile_view():
	input_pet_type = Pet_type.query.all()
	user_pets = db_session.query(Pet,Pet_type). \
					filter(Pet.type==Pet_type.id). \
			  		filter(Pet.owner==current_user.id).all()

	return render_template("update_profile.html",pet_type=input_pet_type,user_pets=user_pets)

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
			print (current_user.get_id)
			return redirect('/')
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
			conn.close()
			
			u = db_session.query(User).filter_by(user_name= username).first()
			user_id = u.id
			print ('success')
			return render_template('home.html')

	else:
		return render_template('register.html')


@app.route('/fave')
@login_required
def fave():
	#handle event where user adds a new recipe to faves
	recipetofave = request.args.get('recipetofave')	 #id of recipe to fave
	if recipetofave is not None:
		print(recipetofave)

	#put list of faves in recipes variable to be rendered by jinja
	recipes = []
	return render_template('home.html',recipes=recipes)

@app.route('/recipe')
def recipe_view():
	"""
	can't rely on every link going to /recipe to contain all the info set as 
	parameters from the previous page, so use db lookup with recipe id

	"""

	#case 1: handle links in form of {{ url_for('recipe_view',rid= r.Recipe.id }}
	recipeid = request.args.get('recipeid')
	if recipeid is not None:
		recipe = db_session.query(Recipe,Pet_type,User).\
								 filter(Recipe.type==Pet_type.id). \
								 filter(Recipe.user_id==User.id). \
								 filter(Recipe.id==recipeid).first()
		return render_template("recipe.html",
			recipeid=recipe.Recipe.id,
			title=recipe.Recipe.title,
			ingredient=recipe.Recipe.ingredient,
			instruction=recipe.Recipe.instruction,
			pettype=recipe.Pet_type.type,
			user=recipe.User.user_name,
			img=recipe.Recipe.imagepath,
			userid=recipe.User.id)

	else:
		return redirect('/')

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_post', methods = ['GET', 'POST'])
def upload_post():
	UPLOAD_FOLDER = 'app/static/images/recipe_image'
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	input_pet_type = Pet_type.query.all()
	if request.method == 'POST':
		print ('in post')
		title = request.form['title']
		ingredient = request.form['ingredient']
		instruction = request.form['instruction']
		pet_type = request.form['pet_type']
		user_id=current_user.id
		u = db_session.query(User).filter_by(id= user_id).first()

		img = request.files['post_image']
		if img.filename == '':
			img_path = None
		if img and allowed_file(img.filename):
			filename = secure_filename(img.filename)
			img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print ('file upload successfully!')
			img_path = '../static/images/recipe_image/' + filename
			print (img_path)

		if( u is not None):
			meta = MetaData(engine,reflect=True)
			table = meta.tables['recipe']
			if img_path is not None:
				ins = table.insert().values(user_id=user_id, ingredient=ingredient, instruction=instruction, type=pet_type, title=title, imagepath=img_path) 
			else:
				ins = table.insert().values(user_id=user_id, ingredient=ingredient, instruction=instruction, type=pet_type, title=title) 
			conn = engine.connect()
			conn.execute(ins)
			conn.close()

			return render_template('home.html', pet_type = input_pet_type)
		else:
			return render_template('upload_post.html', pet_type = input_pet_type)

	else:
		return render_template('upload_post.html', pet_type = input_pet_type)

if __name__ == '__main__':
	#print "lol"
	app.run(debug=True, host='127.0.0.1')