from app import db

class Accounts(db.Model):
	id = db.Column(db.String, primary_key = True)
	username = db.Column(db.String, unique=True)
	password = db.Column(db.String, nullable = False)

	def __repr__(self):
		return f'<Account {self.username},{self.password},{self.email}>'
	
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
	profile_pic = db.Column(db.String)

	def __repr__(self):
		return f'<Account {self.id},{self.name},{self.email},{self.phone},{self.dob},{self.address},{self.website},{self.github},{self.twitter}, {self.instagram}, {self.facebook},{self.profile_pic} >'
	
