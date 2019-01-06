import os

class Config:
	
	#************************ THE FOLLOWING SETTINGS **CANNOT BE** TO BE EDITABLE OUT OF THE CONFIG FILE *********************************************************
	
	
	app_name = "Flim"
	app_allow_anonymous_view_posts = True #TODO actually make this work
	
	app_db_name = os.getenv("FLIM_DB_NAME", default="flim") # no edits outside of config file.
	app_db_username = os.getenv("FLIM_DB_USERNAME", "") # no edits outside of config file.
	app_db_password = os.getenv("FLIM_DB_PASSWORD", "") # no edits outside of config file.
	app_db_host = os.getenv("FLIM_DB_HOST", "") # no edits outside of config file.
	app_db_provider = os.getenv("FLIM_DB_PROVIDER", "") # no edits outside of config file.
	
	app_message_max_length = 9990 # no edits outside of config file.
		
	
	#************************ END SECTION *********************************************************
	
	
	
	#************************ THE FOLLOWING SETTINGS HAVE TO BE EDITABLE OUT OF THE CONFIG FILE *********************************************************
	
	
	
	file_app_post_topics_list = ["Announcement", "Help Needed", "Idea", "Not Urgent", "Urgent", "Windows", "macOS", "Linux", "iOS", "Android", "Windows Phone", 
		"Ubuntu Touch", "KDE Plasma Mobile", "Question", "SIM Card Problem", "Cell Phone", "Desktop", "Laptop", "Broken", "Data Recovery"] # allow edits outside of config file.
	
	file_app_allow_registration_tmp = os.getenv("FLIM_ALLOW_REGISTRATION") # allow edits outside of config file.
	file_app_allow_registration = False
	
	if file_app_allow_registration_tmp == '1':
		file_app_allow_registration = True
	elif file_app_allow_registration_tmp == '0':
		file_app_allow_registration = False
	
	
	file_app_admin_group_id = 1 # allow edits outside of config file.
	
	#************************ END SECTION *********************************************************
	
	#************************ HOST INFORMATION SECTION ********************************************

	app_host = os.getenv("FLIM_HOST", "127.0.0.1")
	app_port = int(os.getenv("FLIM_PORT", "5000"))


	#************************ END SECTION *********************************************************
	
	
	
	#*********************** DEFINE DB-EDITABLE VARS **********************************************
	
	app_allow_registration = file_app_allow_registration
	app_post_topics_list = file_app_post_topics_list
	app_admin_group_id = file_app_admin_group_id
	
	
	#**********************************************************************************************
	
	
	# DO NOT EDIT THE FOLLOWING!!!!!
	
	
	
	
	
	app_version = "TESTING"
	app_static_files_directory = "/static" # do not change, just makes things easier for us
	
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'afioj89498ffj98hiahffuihfihwilafhliuifhUIHFIUHFIUHfieuahhu8yh4ih4foh'
	SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}/{}".format(app_db_provider, app_db_username, app_db_password, app_db_host, app_db_name)
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	
	def get_post_topics_list(self):
		config_topics_list = [(topic, topic) for topic in self.app_post_topics_list]
		return config_topics_list
