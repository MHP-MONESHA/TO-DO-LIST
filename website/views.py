
# Standard routes for the app , where users can actually go to

# url deifned here , seperate app from blueprint
from flask import Blueprint, render_template

# Makes things more organised 
views = Blueprint('views', __name__) 

@views.route('/')
def home():
    return render_template("/templates/home.html")