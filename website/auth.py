from flask import Blueprint , render_template , request , flash , redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash   # never want to store the password to what it is .. convet it to much more security around it.
from . import db 
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # look in the database for the user with that email / returns the first result 
        if user:
            if check_password_hash(user.password, password):
                flash('Login Successful!' , category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password', category='error')
        else:
            flash('Email not found', category='error')


    return render_template("login.html" , user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/Sign_up', methods=['GET', 'POST'])
def Sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')          
        elif len(email) < 4:
            flash('Email must be greater than 3 characters ', category='error')        
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters ', category='error')       
        elif password1!= password2:
            flash('Passwords don\'t match', category='error')        
        elif len(password1) < 7:
            flash('Password must be atleast 7 characters long', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Registration Successful', category='success')
            return redirect(url_for('views.home'))

            # add the user to the database
            pass
    return render_template("Sign_up.html", user=current_user)
