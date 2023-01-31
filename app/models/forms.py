from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

class CreateUser(FlaskForm):
    email = StringField("username", validators=[DataRequired()])
    phone = StringField("phone", validators=[DataRequired()] )
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    name = StringField("username", validators=[DataRequired()])
    repetepassword = PasswordField("password", validators=[DataRequired()])
    cargo = StringField("phone", validators=[DataRequired()] )

class CreateTeam(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description", validators=[DataRequired()])


class Candidato(FlaskForm):
    status = StringField("status", validators=[DataRequired()])


class recuperar(FlaskForm):
    email = StringField("username", validators=[DataRequired()])
    phone = StringField("phone", validators=[DataRequired()] ) 

class CreateHero(FlaskForm):
    equipe = StringField("equipe", validators=[DataRequired()])

class Search(FlaskForm):
    username = StringField("username", validators=[DataRequired()])