from app.models import *
from app import db

class AddGroup:
	def __init__(self, group_name):
		self.group_name = group_name
	
	def create(self):
		group = Group(name=self.group_name)
		db.session.add(group)
		db.session.commit()

		return group
