from flask import Flask, render_template

app = Flask(__name__)

@app.route('/',methods=["GET"])
def index():
	#we must use render_template in order to make dynamic pages with jinja in the html file itself
	#all html files need to be in templates folder
    return render_template("home_test.html") 

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')