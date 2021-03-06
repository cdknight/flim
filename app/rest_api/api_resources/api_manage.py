from app import app, api
from flask import request, jsonify
from flask_restful import Resource

from app.rest_api.models import *
from app.models import *

from app.rest_api.api_resources.api_decorators import *
# Authentication for adding an API key is present for security reasons, which are obvious.

@app.route("/api/key/add", methods=["PUT"])
@api_require_auth
@api_require("description", str)
def api_key_add():
    # In order to add an API key, you MUST provide a user by their ID.
    # Request parmeters: username (mandatory): user ID to add API key for
	# Request parameters: password (mandatory): password for user ID
	# Request parmeters: description description for API key added to database
	# Request returns "api_key" : string value of your API key. Keep this value VERY SAFE. Request also returns "status": true. (IF SUCCESSFUL)
	# Request returns "msg" : string, "status" : false. (IF FAILED)

	"""
		This function is designed to generate and return a new API key for a user based on description and user ID provided.
    """

    # A blank report variable is generated.

	report = {}

	# STEP 1: Retrieve values from request and check if they are valid.

	username = request.values.get("username")
	password = request.values.get("password")
	description = request.values.get("description")

	if user_id == None:

		# User ID is not valid! Return failing report.


		report['status'] = False
		report['msg'] = "No user ID was provided"

		return jsonify(report), 403

	if password == None:

		# Passsword is not valid! Return a failing report.

		report['status'] = False
		report['msg'] = "No password was provided"

		return jsonify(report), 403


	# Check user ID and password to be valid

	api_user = Users.query.filter_by(username=username).first()

	if not api_user.check_password(password):

		# The user is unauthorized to create an API key.

		report['status'] = False
		report['msg'] = "You are unauthorized to access this resource"

		return jsonify(report), 403


	# STEP 1b: Make sure the API user is validated with the credentials privided.



	# STEP 2: Generate the API key.

	# STEP 2a: Check if description is valid, we do not want to pass a None value to the database. If it isn't, we will give description a blank value.

	if description == None:
		description = "" 


	# Step 2b: Actually create the API key

	new_api_key = APIKey.create_api_key(api_user, description)

	# Step 3: Generate report and send off.

	report['status'] = True
	report['api_key'] = new_api_key

	return jsonify(report)


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





api.add_resource(APIKeyInfoResource, "/api/key/info")
api.add_resource(APIKeyDeleteResource, "/api/key/delete")

