# from flask.wtf import Form
# from flask_wtf import Form
from flask_wtf import Form
# from wtforms.fields import TextField, BooleanField
# from wtforms.validators import Required
# from wtforms import TextField, BooleanField

from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)