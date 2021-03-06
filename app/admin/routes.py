from app import db
from app import app
from app.models import *
from app.admin.forms import *

from app.create.user import Register
from app.update.user_profile import UpdateUserProfile

from app.forms import RegistrationForm, UpdateProfileForm

from app import config_helper

from flask import render_template, abort, request, redirect, flash, abort
from flask_login import current_user, login_manager

from app.admin.instance_stats import InstanceStats

import sys
import json


# ADMIN ROUTES

# All admin route functions are prepended by 'admin_' 


@app.before_request
def restrict_admin_access():
	
	request_paths = request.path.split('/')
	admin_group = Group.admin_group()
	
	if request_paths[1] == "admin":
		if not admin_group in current_user.groups: # not an admin
			abort(404)
			
			
	
	


@app.route('/admin/version')
def admin_test():
	return render_template("admin/version.html", sys=sys, title="Version")
	
#********************************************** ADMIN HOME **********************************************




#********************************************** END ADMIN HOME **********************************************
	
	
#********************************************** INSTANCE STATS ROUTES **********************************************

istats = InstanceStats()

@app.route('/admin/')
@app.route('/admin/stats')
def admin_stats():
	return render_template('admin/stats.html', istats=istats, title="Stats")
	
@app.route('/admin/stats/cpuload_percent')
def cpuload_percent():
	return json.dumps(istats.cpu_load_percent())
	
@app.route('/admin/stats/cpuload_freq')
def cpuload_freq():
	return json.dumps(istats.cpu_current_frequencies())
	
@app.route('/admin/stats/avail_mem')
def avail_mem():
	print(round(istats.available_mem(), 2))
	return str(round(istats.available_mem(), 2))
	
@app.route('/admin/stats/avail_swap_mem')
def avail_swap_mem():
	print(round(istats.available_swap_mem(), 2))
	return str(round(istats.available_swap_mem(), 2))
	
	
	
	

	
	
#********************************************** END INSTANCE STATS **********************************************


#********************************************** /admin/forum/* ROUTES *************************************************

@app.route('/admin/forum/topics')
def admin_topics_prefs():
	topics = Topic.query.all()
	
	#print(f"DEBUG: topics is {topics}")
	
	return render_template("admin/topics.html", title="Manage Topics", topics=topics)
	
	

@app.route('/admin/forum/topics/new_topic', methods=["GET", "POST"])
def admin_new_topic():
	form = NewTopicForm()
	
	if form.validate_on_submit():
		new_topic = Topic(name=form.topic_name.data)
		db.session.add(new_topic)
		db.session.commit()
		
		flash("Topic added succesfully.")
		
		return redirect(url_for("admin_topics_prefs"))
	
	return render_template("admin/new_topic.html", title="New Topic", form=form)
	
@app.route('/admin/forum/topics/delete_topic/<topic_id>', methods=["GET", "POST"])
def admin_delete_topic(topic_id):
	topic = Topic.query.filter_by(id=topic_id).first()
	
	if topic != None:
		db.session.delete(topic)
		db.session.commit()
		
		flash("Topic removed succesfully.")
		
		return redirect(url_for("admin_topics_prefs"))
		
	flash("Topic removed unsuccesfully.")	
	return redirect(url_for("admin_topics_prefs"))
	
	
@app.route('/admin/forum/topics/edit_topic/<topic_id>', methods=["GET", "POST"])
def admin_edit_topic(topic_id):
	topic = Topic.query.filter_by(id=topic_id).first()
	form = EditTopicForm()
	
	if form.validate_on_submit():
		topic.name = form.new_topic_name.data
		db.session.commit()
		
		flash("Topic updated succesfully.")
		
		return redirect(url_for("admin_topics_prefs"))
	
	form.new_topic_name.default = topic.name
	form.process()
	
	return render_template("admin/edit_topic.html", form=form, title="Edit Topic")


#********************************************** END /admin/forum/* ROUTES *********************************************


#********************************************** /admin/user/* ROUTES********************************************

@app.route('/admin/users/signup_settings', methods=["GET", "POST"])
def admin_signup_settings():
	perms_form = SignUpPermissionsForm()
	
	print(f'After commiting to database, the app_allow_registration value is {int(config_helper.get_config_value("app_allow_registration"))}')
	
	if config_helper.get_config_value('app_allow_registration') == '1':
		perms_form.allow_registration.default = True
	else:
		perms_form.allow_registration.default = False
	
	
	if perms_form.validate_on_submit():
		print(f"allow_registration is {perms_form.allow_registration.data}")
		
		flash("Settings changed succesfully!")
		config_helper.add_config_keypair("app_allow_registration", perms_form.allow_registration.data)
		
		print(f'[dbg] After commiting to database, the app_allow_registration value is {config_helper.get_config_value("app_allow_registration")}')
		
		return redirect(url_for("admin_signup_settings"))
	
	perms_form.process()
	return render_template("admin/signup_settings.html", title="Sign-up Settings", perms_form=perms_form)


@app.route("/admin/users/create_user", methods=["GET", "POST"])
def admin_create_user():
	form = RegistrationForm()

	if form.validate_on_submit():
		
		re = Register(form.first_name.data, form.last_name.data, form.email.data, form.password.data, form.username.data)
		re.register()
		
		flash(f"User created succesfully.")
		
		return redirect(url_for("admin_manage_users"))
		
	
	return render_template("admin/create_user.html", title="Create User", form=form)
	
	
@app.route('/admin/users/manage_users')
def admin_manage_users():
	all_users = Users.query.all()
	
	return render_template("admin/manage_users.html", users=all_users)
	
@app.route('/admin/users/manage_user/<user_id>', methods=["GET", "POST"])
def admin_manage_user(user_id):
	user_to_manage = Users.query.filter_by(id=user_id).first()
	
	form = UpdateProfileForm()
	
	
	if form.validate_on_submit():
		if form.password.data == form.password_validate.data:
			update_user_profile = UpdateUserProfile(form.first_name.data, form.last_name.data, form.email.data, form.password.data, 
														form.password_validate.data, form.about_me.data, user_to_manage)
														
			update_user_profile.update()
			
			flash("User updated succesfully!")
			return redirect(url_for("admin_manage_users"))
			
		else:
			flash("Error: The passwords do not match.")	
		
		
	
	# Set form default values from the user's current information
	
	form.first_name.default = user_to_manage.first_name
	form.last_name.default = user_to_manage.last_name
	form.email.default = user_to_manage.email 
	form.about_me.default = user_to_manage.about
	
	# Set form default values form the user's current information
	
	
	form.about_me.label = "About" # Set this label to something more appropriate for admins
	
	form.process()
	
	
	
	return render_template("admin/manage_user.html", user=user_to_manage, form=form)

#********************************************** /admin/user/* ROUTES********************************************

#********************************************** /admin/group/* ROUTES********************************************

@app.route("/admin/group/create_group", methods=["GET", "POST"])
def admin_create_group():
	form = CreateGroupForm()
	
	if form.validate_on_submit():	
		Group.create_group(form.group_name.data)
		flash("Group created succesfully!")
		
		return redirect(url_for("admin_manage_groups"))
		
	
	return render_template("admin/new_group.html", title="Create Group", form=form)
	
	
@app.route('/admin/group/manage_groups')
def admin_manage_groups():
	all_groups = Group.query.all()
	
	return render_template("admin/manage_groups.html", title="Manage Groups", all_groups=all_groups)
	
	
@app.route('/admin/group/delete_group/<group_id>')
def admin_delete_group(group_id):
	group_to_delete = Group.query.filter_by(id=group_id).first()
	
	db.session.delete(group_to_delete)
	db.session.commit()
	
	flash("Group deleted succesfully!")
	
	return redirect(url_for("admin_manage_groups"))
	
	
	
@app.route('/admin/group/edit_group/<group_id>', methods=["GET", "POST"])
def admin_edit_group(group_id):
	group_to_edit = Group.query.filter_by(id=group_id).first()
	
	form = EditGroupForm()
	
	
	if form.validate_on_submit():
		group_to_edit.name = form.group_name.data
		db.session.commit()
		
		flash("Group modified succesfully!")
		
		return redirect(url_for("admin_manage_groups"))
	
	
	form.group_name.default = group_to_edit.name
	form.process()
	
	return render_template('admin/edit_group.html', form=form, title="Edit Group")
#********************************************** /admin/group/* ROUTES********************************************
















