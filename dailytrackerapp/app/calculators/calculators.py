from flask import Flask, render_template, request, redirect, url_for, session
from app.calculators import bp

@bp.route("/")
@bp.route("/scholarship")
def scholarship():
    profile_pic_name = 'profile/profile_pics/' + session.get("profile_pic")
    profile_pic = url_for('profile.static', filename=profile_pic_name)
    return render_template('scholarship.html',profile_pic=profile_pic)

@bp.route("/gpa")
def gpa():
    profile_pic_name = 'profile/profile_pics/' + session.get("profile_pic")
    profile_pic = url_for('profile.static', filename=profile_pic_name)
    return render_template('gpa.html',profile_pic=profile_pic)

