# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from app.login import login
from app.models import Accounts
from app import db
import re
import random
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy import text
from sqlalchemy.sql import func
	
def object_as_dict(obj):
	return {c.key: getattr(obj, c.key)
		for c in inspect(obj).mapper.column_attrs}

@login.route('/')
@login.route('/login', methods =['GET', 'POST'])
def login_func():
	msg_username = ''
	msg_password = ''
	msg = ''
	msg_register = ''

	if request.method == 'POST':
		username1 = request.form['username']
		password1 = request.form['password']
		account = Accounts.query.filter_by(username=username1, password=password1).first()
		print(username1, password1)
		#query = Accounts.query.all()
		#for user in query:
			#print(object_as_dict(user))
		if account:
			session['loggedin'] = True
			session['id'] = account.id
			session['username'] = account.username
			msg = 'Logged in successfully !'
			return render_template('login/index.html', msg = msg)
		if len(username1)==0:
			msg_username = 'alert-validate'
			msg = 'Incorrect username or password !'
		if len(password1)==0:
			msg_password = 'alert-validate'
			msg = 'Incorrect username or password !'
		

	return render_template('login/login.html', msg_username = msg_username, msg_password = msg_password, msg=msg, msg_register = msg_register)

@login.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return render_template('login/login.html')

@login.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	msg_username = ''
	msg_username_class = ''
	msg_password = ''
	msg_password_class = ''
	msg_confirmpass = ''
	msg_confirmpass_class = ''
	flag = 0
	if request.method == 'POST':
		username1 = request.form['username']
		password1 = request.form['password']
		confirmpass1 = request.form['confirmpass']
		account = Accounts.query.filter_by(username=username1).first()
		if not re.match(r'[A-Za-z0-9]+', username1):
			msg_username = 'Create unique username'
			msg_username_class = 'alert-validate'
			flag = 1
		if account:
			msg_username = 'Account already exists'
			msg_username_class = 'alert-validate'
			flag = 1
		if not password1:
			msg_password = 'Enter passoword'
			msg_password_class = 'alert-validate'
			flag = 1
		if not confirmpass1:
			msg_confirmpass = 'Enter passoword'
			msg_confirmpass_class = 'alert-validate'
			flag = 1
		if confirmpass1 != password1:
			msg_confirmpass = 'Password not matching'
			msg_confirmpass_class = 'alert-validate'
			flag = 1
			
		if flag ==1:
			msg="Incorrect details entered"
		else:
			id = random.randrange(100, 999)
			id_check = Accounts.query.filter_by(id=id).first()
			while(id_check == id):
				id = random.randrange(100, 999)
			new_account = Accounts(id=id, username = username1, password = password1, email = None)
			db.session.add(new_account)
			msg = 'You have successfully registered!'
			db.session.commit()
			return render_template('login/login.html', msg_register = msg)
	return render_template('login/register.html', msg = msg, msg_password = msg_password, msg_username = msg_username, msg_password_class = msg_password_class, msg_username_class = msg_username_class, msg_confirmpass = msg_confirmpass, msg_confirmpass_class = msg_confirmpass_class)


