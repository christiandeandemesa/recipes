from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/recipe/<int:id>')
def user_recipe_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    recipe_data = {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('user_recipe.html', recipe = Recipe.read_one(recipe_data), user = User.read_by_id(user_data))

@app.route('/new/recipe')
def new_recipe_page():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('new_recipe.html')

@app.route('/edit/recipe/<int:id>')
def edit_recipe_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    return render_template('edit_recipe.html', recipe = Recipe.read_one(data))

@app.route('/create/recipe', methods = ['post'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.valid_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'thirty_minutes': request.form['thirty_minutes'],
        'instructions': request.form['instructions'],
        'date': request.form['date'],
        'user_id': session['user_id']
    }
    Recipe.create(data)
    return redirect('/dashboard')

@app.route('/edit/recipe', methods = ['post'])
def edit_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.valid_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        'id': request.form['id'], # Why doesn't it like this?
        'name': request.form['name'],
        'description': request.form['description'],
        'thirty_minutes': request.form['thirty_minutes'],
        'instructions': request.form['instructions'],
        'date': request.form['date']
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/delete/recipe/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    Recipe.delete(data)
    return redirect('/dashboard')