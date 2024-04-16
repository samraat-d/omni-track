from flask import Flask, render_template, request, redirect, url_for, session
from app.todo import bp
from app.models import Todo
from app import db
import random

@bp.route('/')
def todo():
    accid = session.get('id')
    profile_pic_name = 'profile/profile_pics/' + session.get("profile_pic")
    profile_pic = url_for('profile.static', filename=profile_pic_name)
    todo_list = Todo.query.filter(Todo.account_id == accid).all()
    return render_template("todo.html", todo_list=todo_list, profile_pic=profile_pic)

@bp.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    accid = session.get('id')
    id = random.randrange(100, 999)
    id_check = Todo.query.filter_by(id=id).first()
    while(id_check == id):
        id = random.randrange(100, 999)
    new_todo = Todo(id=id,account_id=accid, title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todo.todo"))

@bp.route("/update/<int:todo_id>")
def update(todo_id):
    accid = session.get('id')
    todo = Todo.query.filter((Todo.id==todo_id) & (Todo.account_id == accid)).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo.todo"))

@bp.route("/delete/<int:todo_id>")
def delete(todo_id):
    accid = session.get('id')
    todo = Todo.query.filter((Todo.id==todo_id) & (Todo.account_id == accid)).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo.todo"))
