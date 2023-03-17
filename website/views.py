
# Standard routes for the app , where users can actually go to

# url deifned here , seperate app from blueprint
from flask import Blueprint, render_template , flash , request , jsonify
from flask_login import  login_required, current_user
from .models import Note
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
    

