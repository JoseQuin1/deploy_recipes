from flask import render_template, redirect, request, session, flash
from flask_app.models.user import Users
from flask_app.models.recipe import Recipe
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('index.html')


@app.route('/user_login', methods=['post'])
def user_login():
    user = Users.get_by_email(request.form)

    if not user:
        flash("Invalid Credentials","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Credentials","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route('/register', methods=['post'])
def register():
    if not Users.validate_register(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
    }
    
    id = Users.save(data)
    session['user_id'] = id

    return redirect('/dashboard')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')