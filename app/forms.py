from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectMultipleField, widgets
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo
from app.config import Config
from app import config_helper

current_config = Config()



class RegistrationForm(FlaskForm):
	first_name = StringField('First Name', validators=[DataRequired()])
	last_name = StringField('Last Name', validators=[DataRequired()]) 
	username = StringField('Username', validators=[DataRequired()])
	email = EmailField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_validate', message='The passwords must match')])
	password_validate = PasswordField('Password (type again to validate)', validators=[DataRequired()])
	submit = SubmitField('Register')

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	remember_me = BooleanField("Remember")
	submit = SubmitField("Log In")


class PostForm(FlaskForm):
	edit_post = False
	title = StringField("Title", validators=[DataRequired()])
	content = TextAreaField("Content", validators=[DataRequired()])
	topics = SelectMultipleField("Topics", choices=config_helper.get_full_post_topics_list())
	submit = SubmitField("Post")

def validate_newpost_form(form):
	if form.edit_post:
		return bool(form.content.data)
	
	return form.title.data and form.content.data

class UpdateProfileForm(FlaskForm):
	first_name = StringField('First Name')
	last_name = StringField('Last Name')

	email = EmailField('Email')

	password = PasswordField('Password', validators=[EqualTo('password_validate', message='The passwords must match')])
	password_validate = PasswordField('Password (type again to validate)')

	about_me = TextAreaField("About Me")

	submit = SubmitField("Update Information")

class EditPostForm(FlaskForm):
	content = TextAreaField("New Content")
	topics = SelectMultipleField("Update Topics/Tags", choices=config_helper.get_full_post_topics_list(), option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
	submit = SubmitField("Update Post")

class NewResponseForm(FlaskForm):
	content = TextAreaField("Response")
	submit = SubmitField("Submit Response")

class EditResponseForm(FlaskForm):
	content = TextAreaField("Edit Response")
	submit = SubmitField("Update Response")






