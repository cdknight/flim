import os

class Config:
	
	
	app_name = "File-a-Bug"
	
	app_db_name = "bug_reporter_db"
	app_db_username = "default_u"
	app_db_password = "letmeinmysql"
	app_db_host = "localhost"
	
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'afioj89498ffj98hiahffuihfihwilafhliuifhUIHFIUHFIUHfieuahhu8yh4ih4foh'
	SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}".format(app_db_username, app_db_password, app_db_host, app_db_name)
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	