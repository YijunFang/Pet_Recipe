# Pet_Recipe

Installing flask:

http://flask.pocoo.org/docs/0.12/installation/#installation

Running flask app (for windows):
```
virtualenv venv             
```
to setup virtual env for the first time
```
pip install Flask          
```
if flask is not installed in the virtual env yet
```
venv\Scripts\activate      
```
to start virtual env
```
set FLASK_APP=run.py 
```
to choose web app. Use export command on unix
```
flask run                   
```
to run web app
```
venv\Scripts\deactivate 
```
to exit virtual environment

virtual env is needed to run on windows, may not be necessary on other OS
