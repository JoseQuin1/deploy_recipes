from flask import render_template, redirect, request, session, flash
from flask_app.models.user import Users
from flask_app.models.recipe import Recipe
from flask_app import app


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    return render_template('dashboard.html', users = Users.get_by_id(data), recipes = Recipe.get_all_recipes())
    

@app.route("/create/new")
def recipe_new():
    if 'user_id' not in session:
        return redirect('/')
    else:
        return render_template('recipe_new.html')

@app.route("/create/recipe", methods=['post'])
def save():

    if not Recipe.validate_recipe(request.form):
        return redirect('/create/new')
    
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id'],
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date_cooked':request.form['date_cooked'],
            'under_30_minutes':request.form['under_30_minutes'],
        }
        # print(data)
        Recipe.save(data)
    return redirect('/dashboard')

@app.route("/recipe/view/<int:id>")
def recipe_view(id):
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        data = {'id':id}

        user_data = {
        'id' : session['user_id']
        }

        r = Recipe.get_by_id(data)
    return render_template('recipe_view.html', users = Users.get_by_id(user_data), get_recipe = r)

@app.route('/recipe/edit/<int:id>')
def recipe_edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        data = {'id':id}
        user_data = {
            'id' : session['user_id']
        }

        r = Recipe.get_by_id(data)
        return render_template('recipe_edit.html', get_recipe = r, users = Users.get_by_id(user_data))

@app.route('/edit/recipe/<int:id>', methods=['post'])
def update(id):
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'under_30_minutes': request.form['under_30_minutes'],
            'date_cooked': request.form['date_cooked'],
            'id':id,
        }
        Recipe.update(data)
        return redirect('/dashboard')

@app.route('/remove/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    else:
        data = {
            'id':id,
        }
        Recipe.delete(data)
        return redirect('/dashboard')