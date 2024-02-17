# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import re
from flask_socketio import SocketIO
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy import text
from sqlalchemy.sql import func


app = Flask(__name__)
app.secret_key = "sam24"
socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///omnitrack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Accounts(db.Model):
	id = db.Column(db.String, primary_key = True)
	username = db.Column(db.String, unique=True)
	password = db.Column(db.String, nullable = False)
	email = db.Column(db.String)

	def __repr__(self):
		return f'<Account {self.username},{self.password},{self.email}>'
	
def object_as_dict(obj):
	return {c.key: getattr(obj, c.key)
		for c in inspect(obj).mapper.column_attrs}

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg_username = ''
	msg_password = ''
	msg = ''

	if request.method == 'POST':
		username1 = request.form['username']
		password1 = request.form['password']
		account = Accounts.query.filter_by(username=username1, password=password1).first()
		#query = Accounts.query.all()
		#for user in query:
			#print(object_as_dict(user))
		if account:
			session['loggedin'] = True
			session['id'] = account.id
			session['username'] = account.username
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		elif len(username1)==0 or not re.match(r'[^@]+@[^@]+\.[^@]+', username1):
			print("username wrong")
			msg_username = 'Enter username'
			msg = 'Incorrect username / password !'
		elif len(password1) == 0:
			msg_password = 'Enter password'
			msg = 'Incorrect username / password !'
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg_username = msg_username, msg_password = msg_password, msg=msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username1 = request.form['username']
		password1 = request.form['password']
		email1 = request.form['email']
		account = Accounts.query.filter_by(username=username1).first()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email1):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username1):
			msg = 'Username must contain only characters and numbers !'
		elif not username1 or not password1 or not email1:
			msg = 'Please fill out the form !'
		else:
			new_account = Accounts(username = username1, password = password1, email = email1)
			db.session.add(new_account)
			msg = 'You have successfully registered !'
			db.session.commit()
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(
    app,
    allow_unsafe_werkzeug=True,
    host='localhost',
    port=int(3030)
    )