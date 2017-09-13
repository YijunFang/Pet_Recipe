from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
	#we must use render_template in order to make dynamic pages with jinja in the html file itself
	#all html files need to be in templates folder
	return render_template("home_test.html")  

@app.route('/search',methods=['POST'])
def search_view():
	search_term = request.form['search_term']   
	return render_template("search_test.html",search_term=search_term) 

@app.route('/profile')
def profile_view():    
	return render_template("profile_test.html")  #html file can be replaced without affecting app route


if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1')