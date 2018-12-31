from app import app, api
from flask import request
from flask_restful import Resource

from app.rest_api.models import *
from app.models import *


class APIKeyAddResource(Resource):
	
	# In order to add an API key, you MUST provide a user by their ID.
	# Request parmeters: user_id (mandatory): user ID to add API key for
	# Request parmeters: description (optional) description for API key added to database
	# Request returns "api_key" : string value of your API key. Keep this value VERY SAFE. Request also returns "status": true. (IF SUCCESSFUL)
	# Request returns "msg" : string, "status" : false. (IF FAILED)
	
	
	def put(self):
		
		"""
		This function is designed to generate and return a new API key for a user based on description and user ID provided.
		"""
		
		
		# A blank report variable is generated.
		
		report = {} 
		
		# STEP 1: Retrieve values from request and check if they are valid.
		
		user_id = request.values.get("user_id")
		description = request.values.get("description")
		
		if user_id == None:
			
			# User ID is not valid! Return failing report.
			
			
			report['status'] = False
			report['msg'] = "No user ID was provided"
			
			return report
		
		
		# STEP 2: Generate the API key.
		
		# STEP 2a: Check if description is valid, we do not want to pass a None value to the database. If it isn't, we will give description a blank value.
		
		if description == None:
			description = "" 
		
		# Step 2b: Create user object
		
		user = Users.query.filter_by(id=user_id).first()
		
		# Step 2c: Generate API key.
		
		new_api_key = APIKey.create_api_key(user, description)
		
		# Step 3: Generate report and send off.
		
		report['status'] = True
		report['api_key'] = new_api_key
		
		return report
		
class APIKeyInfoResource(Resource):
	
	# This is a simple function. All it requires is api_key in order to view information about the API key.
	
	def get(self):
		
		"""
		This function is designed to generate and return a new API key for a user based on description and user ID provided.
		"""
		
		
		# A blank report variable is generated.
		
		report = {} 
		
		# Step 1: Get request variables
		
		api_key = request.values.get('api_key')
		
		
		# Step 2: Retrieve information about the API key from the APIKey model.
		
		api_key_entry = APIKey.query.filter_by(api_key=api_key).first()
		
		
		# Step 3: Return the dictionary directory from the as_dict function
		
		return api_key_entry.as_dict()

class APIKeyDeleteResource(Resource):
	
	"""
	This is a resource designed for deleting API keys.
	"""		

	# A simple function to delete an API key. It requires api_key in order to delete the API key.
	# This request deletes the API key and returns "status": boolean and "msg": string
	
	def delete(self):
		
		# A report variable is generated in the beginning
		report = {}
		
		# Step 1: Retrieve request variables
		
		api_key_to_delete = request.values.get("api_key")
		
		# Step 2: Get API key object.
		
		api_key_to_delete_entry = APIKey.query.filter_by(api_key=api_key_to_delete).first()
		
		# Step 3: Delete API key.
		
		db.session.delete(api_key_to_delete_entry)
		db.session.commit()
		
		# Step 3: Generate and return report.
		
		report['msg'] = "The API key was deleted succesfully."
		report['status'] = True
		
		return report
		
		
		
	
api.add_resource(APIKeyAddResource, "/api/key/add")
api.add_resource(APIKeyInfoResource, "/api/key/info")
api.add_resource(APIKeyDeleteResource, "/api/key/delete")
