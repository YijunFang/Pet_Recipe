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
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from .forms import LoginForm
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

from sqlalchemy import or_

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.debug = True
app.secret_key = 's3cr3t'

from app.database import db_session,engine
from app.models import *

mail = Mail(app)
s = URLSafeTimedSerializer('Thisisasecret!')



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
                    filter(Recipe.user_id==userid). \
                    filter(Recipe.type==Pet_type.id). \
                    all()
    if request.method == 'POST':
        print ("in post")
        print (request)

        recipe_id = request.form['delete']
        delete_recipe = db_session.query(Recipe).filter_by(id= recipe_id).first()
        db_session.delete(delete_recipe)
        db_session.commit() 
        return redirect('/profile')
    else:
        print(profile)
        return render_template("profile_test.html",profile=profile,recipes=recipes,pets=pets)


@app.route('/update_profile', methods = ['GET', 'POST'])
@login_required
def update_profile_view():
    input_pet_type = Pet_type.query.all()

    # see if confirmation password is correct
    # if not, return to form with error message
    confirm = request.form.get('confirm_password')
    u = db_session.query(User).filter(User.id==current_user.id).first()
    if u is None or u.password != confirm:
        user_pets = db_session.query(Pet,Pet_type). \
                filter(Pet.type==Pet_type.id). \
                filter(Pet.owner==current_user.id).all()
        message="The confirmation password was incorrect, please try again."
        if not confirm:
            message=""
        return render_template("update_profile.html",message=message, \
                                pet_type=input_pet_type,user_pets=user_pets)

    # get all pet_name & pet_types in the form
    for i in range(1,11):
        petname = request.form.get('pet_name_'+str(i))
        pettype = request.form.get('pet_type_'+str(i))
        petid = request.form.get('pet_id_'+str(i))
        petdelete = request.form.get('delete_pet_'+str(i))
        
        # add new pets to db
        if petname is not None and pettype is not None and petid is not None and petdelete is None:
            if petid == "-1":
                print("inserting new pet...")
                rows = db_session.query(Pet).count() + 1
                new_pet = Pet(id=rows,type=pettype,NAME=petname,owner=current_user.id)
                db_session.add(new_pet)
                db_session.commit()
            #update existing pets in db
            else:
                print('updating existing pet...')
                db_session.query(Pet).filter(Pet.id==petid). \
                                      update({Pet.NAME:petname, Pet.type:pettype})
                db_session.commit()
        #delete pets marked for deletion
        if petdelete is not None and petid is not None:
            print('deleting pet...')
            db_session.query(Pet).filter(Pet.id==petid).delete()
            db_session.commit()

    # get new list of pets
    user_pets = db_session.query(Pet,Pet_type). \
                filter(Pet.type==Pet_type.id). \
                filter(Pet.owner==current_user.id).all()

    # handle username update
    new_username = request.form.get('username')
    if new_username:
        db_session.query(User).filter(User.id==current_user.id).update({User.user_name:new_username})
        db_session.commit()

    # handle password update
    new_password = request.form.get('new_password')
    if new_password:
        print("new pass")
        db_session.query(User).filter(User.id==current_user.id).update({User.password:new_password})
        db_session.commit()

    # handle email update
    new_email = request.form.get('email')
    if new_email:
        db_session.query(User).filter(User.id==current_user.id).update({User.email:new_email})
        db_session.commit()     

    # handle profile img update
    img = request.files['post_image']
    if img.filename == '':
        img_path = None
    if img and allowed_file(img.filename):
        filename = secure_filename(img.filename)
        img.save(os.path.join('app/static/images/profile_pic/', filename))
        print ('file upload successfully!')
        img_path = '../static/images/profile_pic/' + filename
        print (img_path)
        user_to_update = db_session.query(User).filter(User.id==current_user.id).update({User.profile_pic:img_path})
        db_session.commit()         

    return render_template("update_profile.html",pet_type=input_pet_type,user_pets=user_pets,message="Profile successfully updated")

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

        elif u.password == password && u.authenticated==1:
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

            # email = request.form['email']
            token = s.dumps(email, salt='email-confirm')
            # fill in your host email
            msg = Message('Confirm Email', sender='youremail', recipients=[email])
            # msg = Message('Confirm Email', sender='yoof.tot@gmail.com', recipients=[email])
            link = url_for('confirm_email', token=token, _external=True)
            msg.body = 'Your link to comfirm account register in Pet Recipe is {}'.format(link)
            mail.send(msg)
            print ('email sent')

            return render_template('wait_for_email.html')
            

    else:
        return render_template('register.html')

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        emaill = s.loads(token, salt='email-confirm', max_age=3600)
        print ('get email')
        admin = User.query.filter_by(email=emaill).first()
        admin.authenticated = 1
        db_session.commit()
        print ('update done')

        u = db_session.query(User).filter_by(email=emaill).first()
        user_id = u.id
        print ('comfirm email')
        login_user(u)

        return render_template('home.html')
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    return '<h1>The token works!</h1>'



@app.route('/fave')
@login_required
def fave():
    #handle event where user adds a new recipe to faves
    recipetofave = request.args.get('recipetofave')  #id of recipe to fave
    if recipetofave is not None:
        print(recipetofave)

    #put list of faves in recipes variable to be rendered by jinja
    recipes = []
    return render_template('home.html',recipes=recipes)

@app.route('/recipe', methods = ['POST','GET']) 
def recipe_view():
    """
    can't rely on every link going to /recipe to contain all the info set as 
    parameters from the previous page, so use db lookup with recipe id

    """
    sys.stderr.write('###recipe view entered###\n')
    #case 1: handle links in form of {{ url_for('recipe_view',rid= r.Recipe.id }}
    recipeid = request.args.get('recipeid')
    if recipeid is not None:
        recipe = db_session.query(Recipe,Pet_type,User).\
                                 filter(Recipe.type==Pet_type.id). \
                                 filter(Recipe.user_id==User.id). \
                                 filter(Recipe.id==recipeid).first()
        comments = db_session.query(Comment,User).filter(Comment.recipe_id==recipeid). \
                            filter(Comment.user_id==User.id).all()

        commentid = request.args.get('commentid')

        if commentid is not None:
    
            sys.stderr.write('###delete comment entered###\n')

    #       meta = MetaData(engine,reflect=True)
    #       table = meta.tables['comment']
    #       rem = table.delete(id==commentid) 
    #       conn = engine.connect()
    #       conn.execute(rem)
    #       conn.close()
            db_session.query(Comment).filter(Comment.id == commentid).delete()
            db_session.commit()
            comments = db_session.query(Comment,User).filter(Comment.recipe_id==recipeid). \
                                filter(Comment.user_id==User.id).all()
        
    
        
            return render_template("recipe.html",
            recipeid=recipe.Recipe.id,
            title=recipe.Recipe.title,
            ingredient=recipe.Recipe.ingredient,
            instruction=recipe.Recipe.instruction,
            pettype=recipe.Pet_type.type,
            user=recipe.User.user_name,
            img=recipe.Recipe.imagepath,
            userid=recipe.User.id,
            comments=comments)
        else:

            if request.method=='POST':
                #see how upload recipe uploads to database
            
                sys.stderr.write('###post method entered###\n')
                comment = request.form['comment']
                user_id=current_user.id
                dbs = db_session.query(User).filter_by(id= user_id).first()
                
                if(dbs is not None):
                    meta = MetaData(engine,reflect=True)
                    table = meta.tables['comment']
                    ins = table.insert().values(user_id=user_id, recipe_id=recipeid, message=comment) 
                    conn = engine.connect()
                    conn.execute(ins)
                    conn.close()
                    comments = db_session.query(Comment,User).filter(Comment.recipe_id==recipeid). \
                                filter(Comment.user_id==User.id).all()
        
                    return render_template("recipe.html",
                    recipeid=recipe.Recipe.id,
                    title=recipe.Recipe.title,
                    ingredient=recipe.Recipe.ingredient,
                    instruction=recipe.Recipe.instruction,
                    pettype=recipe.Pet_type.type,
                    user=recipe.User.user_name,
                    img=recipe.Recipe.imagepath,
                    userid=recipe.User.id,
                    comments=comments)
    
        #   else:

            else:   
                return render_template("recipe.html",
                    recipeid=recipe.Recipe.id,
                    title=recipe.Recipe.title,
                    ingredient=recipe.Recipe.ingredient,
                    instruction=recipe.Recipe.instruction,
                    pettype=recipe.Pet_type.type,
                    user=recipe.User.user_name,
                    img=recipe.Recipe.imagepath,
                    userid=recipe.User.id,
                    comments=comments)

    else:
        sys.stderr.write('###redirect to home entered###\n')
        return redirect('/')
















def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_post', methods = ['GET', 'POST'])
@login_required
def upload_post():
    UPLOAD_FOLDER = 'app/static/images/recipe_image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    input_pet_type = Pet_type.query.all()
    if request.method == 'POST':
        print ('in post')
        print (request.form)
        title = request.form['title']
        pet_type = request.form['pet_type']
        user_id=current_user.id
        u = db_session.query(User).filter_by(id= user_id).first()

        ing_counter = 1
        ins_counter = 1
        ingredient = ""
        instruction = ""
        # Get the instruction and indigation
        for r in sorted(request.form.iterkeys()):
            ingredient_target = 'ingredientInput_' + str(ing_counter)
            instruction_target = 'instructionInput_' + str(ins_counter)
            print (ingredient_target)
            if r == ingredient_target :
                print (r)
                r_content = request.form[ingredient_target]
                #instruction = str(indigredient) + str(counter) + ". " + str(r_content) + '\n'
                ingredient = str(ingredient)+ str(r_content) + '\n'
                print (ingredient)
                ing_counter+=1
            elif r == instruction_target:
                print (r)
                r_content = request.form[instruction_target]
                instruction = str(instruction) + str(ins_counter) + ". " + str(r_content) + '\n'
                print (instruction)
                ins_counter+=1

        #instruction = request.form['instruction']


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

            return redirect('/profile')
        else:
            return render_template('upload_post.html', pet_type = input_pet_type)

    else:
        return render_template('upload_post.html', pet_type = input_pet_type)

if __name__ == '__main__':
    #print "lol"
    app.run(debug=True, host='127.0.0.1')
