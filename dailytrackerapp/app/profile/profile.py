# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from app.profile import bp
from app.models import Account_Details
from app import db
import random
from flask_socketio import SocketIO
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy import text
from sqlalchemy.sql import func

def object_as_dict(obj):
	return {c.key: getattr(obj, c.key)
		for c in inspect(obj).mapper.column_attrs}

@bp.route('/profile')
def profile():
	logcheck = session.get('loggedin')
	if logcheck == True:
		id = session.get('id')
		account = Account_Details.query.filter_by(id=id).first()
		if account:
			full_name = account.name
			if full_name == None:
				full_name = ''
			email = account.email
			if email == None:
				email = ''
			phone = account.phone
			if phone == None:
				phone = ''
			dob = account.dob
			if dob == None:
				dob = ''
			address = account.address
			if address == None:
				address = ''
			website = account.website
			if website == None:
				website = ''
			github = account.github
			if github == None:
				github = ''
			twitter = account.twitter
			if twitter == None:
				twitter = ''
			instagram = account.instagram
			if instagram == None:
				instagram = ''
			facebook = account.facebook
			if facebook == None:
				facebook = ''
			profile_pic_name = 'profile/profile_pics/' + account.profile_pic
			profile_pic = url_for('profile.static', filename=profile_pic_name)
			return render_template('profile/profile.html', full_name=full_name, email=email, phone=phone, dob=dob, address=address, website=website, github=github, twitter=twitter, instagram=instagram, facebook=facebook, profile_pic=profile_pic)
	else:
		return render_template('login/login.html')
	return render_template('profile/profile.html')

@bp.route('/profile_edit', methods =['GET', 'POST'])
def profile_edit():
	logcheck = session.get('loggedin')
	profile_pic_name = 'profile/profile_pics/' + session.get("profile_pic")
	profile_pic = url_for('profile.static', filename=profile_pic_name)
	if logcheck == True:
		id = session.get('id')
		account = Account_Details.query.filter_by(id=id).first()
		if account:
			if request.method == 'POST':
				full_name = request.form['fullname']
				email = request.form['email']
				phone = request.form['phone']
				dob = request.form['dob']
				address = request.form['address']
				website = request.form['website']
				github = request.form['github']
				twitter = request.form['twitter']
				instagram = request.form['instagram']
				facebook = request.form['facebook']
				if request.files.get('profile_pic_file') is not None and request.files['profile_pic_file'].filename:
					profile_pic = request.files['profile_pic_file']
					filepath = os.path.join('C:\\Users\\Shilpa\\Desktop\\Coding Files\\daily-tracker\\dailytrackerapp\\app\\profile\\static\\profile\\profile_pics', profile_pic.filename)
					account.profile_pic = profile_pic.filename
					profile_pic.save(filepath)
					session['profile_pic'] = profile_pic.filename
				profile_pic_name = 'profile/profile_pics/' + session.get("profile_pic")
				profile_pic = url_for('profile.static', filename=profile_pic_name)
				if full_name:
					account.name = full_name
				if email:
					account.email = email
				if phone:
					account.phone = phone
				if dob:
					account.dob = dob
				if address:
					account.address = address
				if website:
					account.website = website
				if twitter:
					account.twitter = twitter
				if github:
					account.github = github
				if instagram:
					account.instagram = instagram
				if facebook:
					account.facebook = facebook
				db.session.commit()
				return render_template('profile/profile.html', full_name=account.name, email=account.email, phone=account.phone, dob=account.dob, address=account.address, website=account.website, github=account.github, twitter=account.twitter, instagram=account.instagram, facebook=account.facebook, profile_pic=profile_pic)
	else:
		return render_template('login/login.html')
	return render_template('profile/profile-edit.html', profile_pic = profile_pic)

