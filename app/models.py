from app import db
from app import login
from flask import url_for
from flask_login import UserMixin
from datetime import datetime
from app.config import Config
from app.rest_api.models import *

import hashlib
import json

current_config = Config()

# Handy little function to get an list of IDs from a list of models.
def get_id_list(models):
	model_id_list = []

	# We can add an ID here because no matter what model it is, it has an ID.

	for model in models:
		model_id_list.append(model.id)

	return model_id_list


subresponses = db.Table('subresponses',
	db.Column('response_id', db.Integer, db.ForeignKey('responses.id')),
	db.Column('subresponse_id', db.Integer, db.ForeignKey('responses.id'))
)

group_associations = db.Table('group_associations',
	db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)

class Topic(db.Model):
	__tablename__ = 'topics'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(512), index=True)

	def as_json(self):
		ndict = {}
		ndict['id'] = self.id
		ndict['name'] = self.name
		posts_relating = []
		posts_list = Post.query.all()
		for post in posts_list:
			topics_list = post.get_topics_list()
			if self.name in topics_list:
				posts_relating.append(post.id)
		ndict['posts'] = posts_relating
		return ndict


	def __repr__(self):
		return f"<Topic {self.name}>"

class Users(UserMixin, db.Model):
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	first_name = db.Column(db.String(128), index=True)
	last_name = db.Column(db.String(128), index=True)
	email = db.Column(db.String(128), index=True)
	about = db.Column(db.Text(9990))
	password_hashed = db.Column(db.String(255))
	username = db.Column(db.String(32), index=True, unique=True)

	post = db.relationship('Post', backref='creator')
	response = db.relationship('Response', backref='creator')

	groups = db.relationship(
        'Group', secondary=group_associations)

    # The users have a relationship to the APIKey class.

	api_keys = db.relationship("APIKey")

	def as_dict(self):
		ndict = {}
		ndict['id'] = self.id

		group_ids_list = []
		for group in self.groups:
			group_ids_list.append(group.id)

		ndict['groups'] = group_ids_list

		ndict['admin'] = self.is_admin()
		ndict['first_name'] = self.first_name
		ndict['last_name'] = self.last_name
		ndict['email'] = self.email
		ndict['about'] = self.about
		ndict['password_hashed'] = self.password_hashed
		ndict['username'] = self.username

		return ndict

	def add_to_group(self, group):
		if not self.in_group(group):
			self.groups.append(group)
			db.session.commit()

	def remove_from_group(self, group):
		if self.in_group(group):
			self.groups.remove(group)
			db.session.commit()

	def in_group(self, group):
		#retur n self.groups.filter(group_associations.c.group_id == group.id).count() > 0
		return group in self.groups
		# I really don't see why we can't just do return group in self.groups

	def is_admin(self):
		return Group.admin_group() in self.groups

	def set_password(self, password):
		self.password_hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()

	def check_password(self, check_password):
		return self.password_hashed ==  hashlib.sha256(check_password.encode('utf-8')).hexdigest()

	@login.user_loader
	def load_user(id):
		return Users.query.get(int(id))

	@staticmethod
	def get_user_from_api_key(api_key):
		api_key_inst = APIKey.query.filter_by(api_key=api_key).first()
		user = Users.query.filter_by(id=api_key_inst.user_id).first()
		return user
		
	
	
	def __repr__(self): 
		return "<object User {}>".format(self.username)

class Post(db.Model):
	__tablename__ = "post"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	
	title = db.Column(db.String(128), index=True) 
	content = db.Column(db.Text(current_config.app_message_max_length))
	
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) 
	
	topics = db.Column(db.Text(current_config.app_message_max_length), default="")	
	
	response = db.relationship("Response", backref="parent_post", lazy="dynamic")
	
	def as_dict(self):
		ndict = {}
		ndict["id"] = self.id
		ndict["title"] = self.title
		ndict["content"] = self.content
		ndict["timestamp"] = str(self.timestamp)
		
		ndict["creator_id"] = Users.query.filter_by(id=self.user_id).first().id
				
				
		responses = Response.query.filter_by(parent_post=self).all()
		
		responses_list = []
		
		for response in responses:
			responses_list.append(response.id)
			
		ndict['response_ids'] = responses_list
		
		ndict['topic_list'] = self.get_topics_list()
		
		
		return ndict
	 
	@staticmethod 
	def get_all_posts_list():
		"""Returns all post ids in a list"""
		all_posts = Post.query.all()
		all_post_id_list = []
		for post in all_posts:
			 all_post_id_list.append(post.id)
			 
		return {"all_posts": all_post_id_list}
	
	def get_topics_list(self):
		return json.loads(self.topics)
	
	

	def __repr__(self):
		return "<object Post {} {}>".format(self.id, self.title)
		
		
		
		
class Response(db.Model):
	__tablename__ = "responses"
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
				
	
	response_subresponses = db.relationship(
        'Response', secondary=subresponses,
        primaryjoin=(subresponses.c.response_id == id),
        secondaryjoin=(subresponses.c.subresponse_id == id),
        backref=db.backref('subresponses', lazy='dynamic'), lazy='dynamic')
	
	post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	
	content = db.Column(db.Text(current_config.app_message_max_length))
	
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	
	
	def as_dict(self):
		ndict = {}
		ndict['post_id'] = self.post_id
		ndict['user_id'] = self.user_id
		ndict['content'] = self.content
		ndict['timestamp'] = str(self.timestamp)
		
		return ndict
		
	
	
	def add_subresponse(self, subresponse):
		if not self.is_subresponse(subresponse):
			self.response_subresponses.append(subresponse)
		
	def remove_subresponse(self, subresponse):
		if self.is_subresponse(subresponse):
			self.response_subrepsonses.remove(subresponse)
	
	def is_subresponse(self, subresponse): #we'll not be removing the subresponse param because the program is more flexible then
		return self.subresponses.filter(
			subresponses.c.subresponse_id == subresponse.id).count() > 0
	
	
	def __repr__(self):
		return "<object Response id:{}>".format(self.id)

class Group(db.Model):
	__tablename__ = 'groups'
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(256), index=True)
	
	def formatted_name(self):
		return self.name.replace(" ", "_").lower()
	
	def as_dict(self):
		ndict = {}
		ndict["id"] = self.id
		ndict["name"] = self.name
		
		return ndict
	
	@staticmethod
	def create_group(group_name):
		new_group = Group(name=group_name)
		db.session.add(new_group)
		db.session.commit()
	
	
	@staticmethod	
	def admin_group():
		return Group.query.filter_by(id=current_config.app_admin_group_id).first() # TODO Force group admin to be created with GID 1
		
	def __repr__(self):
		return "<Group id: {} name: {}".format(self.id, self.name)
		
		
class DBConfig(db.Model):
	__tablename__ = 'config'
	
	config_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	
	key = db.Column(db.String(128), index=True)
	value = db.Column(db.Text(9999))	
	@staticmethod
	def get_value(key):
		return DBConfig.query.filter_by(key=key).first()
		


	
		

		
		
	
		


