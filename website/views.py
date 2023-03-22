
# Standard routes for the app , where users can actually go to

# url deifned here , seperate app from blueprint
import datetime
from flask import Blueprint, render_template , flash , request , jsonify ,  redirect, url_for
from flask_login import  login_required, current_user
from .models import Note , Todo
from . import db
import json



# Makes things more organised 
views = Blueprint('views', __name__) 

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Please enter a note!', category='error')
            
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Your note has been saved!', category='success')
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods = ['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Your note has been deleted!', category='success')
        else:
            flash('You do not have permission to delete this note!', category='error')
       
       
    return jsonify({})


@views.route("/todolist")
@login_required
def todolist():
    todo_list = Todo.query.all()
    return render_template("todolist.html", todo_list=todo_list, user=current_user)


@views.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    due_date_str = request.form.get("due_date")
    if due_date_str:
        due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
    else:
        due_date = None
    new_todo = Todo(title=title, complete=False, date_created=datetime.datetime.utcnow(), due_date=due_date)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("views.todolist"))


@views.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("views.todolist"))


@views.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("views.todolist"))
