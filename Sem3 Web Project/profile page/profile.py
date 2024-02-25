# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import re
import random
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

class Account_Details(db.Model):
	id = db.Column(db.String, primary_key = True)
	name = db.Column(db.String)
	email = db.Column(db.String)
	phone = db.Column(db.BigInteger, unique=True)
	dob = db.Column(db.String)
	address = db.Column(db.Text)
	website = db.Column(db.String)
	github = db.Column(db.String)
	twitter = db.Column(db.String)
	instagram = db.Column(db.String)
	facebook = db.Column(db.String)
	profile_pic = db.Column(db.String, default='/static/pics/default-pfp.jpg')

	def __repr__(self):
		return f'<Account {self.id},{self.name},{self.email},{self.phone},{self.dob},{self.address},{self.website},{self.github},{self.twitter}, {self.instagram}, {self.facebook},{self.profile_pic} >'
	
def object_as_dict(obj):
	return {c.key: getattr(obj, c.key)
		for c in inspect(obj).mapper.column_attrs}

@app.route('/')
@app.route('/profile')
def login():
	account = Account_Details.query.filter_by(username=id, password=password1).first()
	return render_template('profile.html', )

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
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
			return render_template('login.html', msg_register = msg)
	return render_template('register.html', msg = msg, msg_password = msg_password, msg_username = msg_username, msg_password_class = msg_password_class, msg_username_class = msg_username_class, msg_confirmpass = msg_confirmpass, msg_confirmpass_class = msg_confirmpass_class)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(
    app,
    allow_unsafe_werkzeug=True,
    host='localhost',
    port=int(3030)
    )