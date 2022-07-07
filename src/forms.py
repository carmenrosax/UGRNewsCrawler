from wtforms import Form
from wtforms import StringField, PasswordField, IntegerField

class LoginForm(Form):
    username= StringField('Username:')
    pwd= PasswordField('Contraseña:')

class getNewsByContent(Form):
    search= StringField('')







