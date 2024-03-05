# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import re
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
		account = Account_Details.query.filter_by(id=id)
		if account:
			full_name = account.name
			email = account.email
			phone = account.phone
			dob = account.dob
			address = account.address
			website = account.website
			github = account.github
			twitter = account.twitter
			instagram = account.instagram
			facebook = account.facebook
			profile_pic = account.profile_pic
			return render_template('profile/profile.html', full_name=full_name, email=email, phone=phone, dob=dob, address=address, website=website, github=github, twitter=twitter, instagram=instagram, facebook=facebook, profile_pic=profile_pic)
	else:
		return render_template('login/login.html')
	return render_template('profile/profile.html')

@bp.route('/profile_edit')
def profile_edit():
	return render_template('profile/profile-edit.html')

