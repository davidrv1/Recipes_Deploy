from flask import render_template, request, redirect, session

from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/create')
def create_recipe():
    if not session['user_id']:
        redirect('/home')
    #validate create
    Recipe.save(request.form)
    return render_template('add_new_recipe.html', current_user = User.getById({'id': session['user_id']}))

@app.route('/save/new/recipe', methods=['post'])
def save_new():
    if not session['user_id']:
        return redirect('/home')
    print("trying to save recipe")
    if not Recipe.validate_create(request.form):
        return redirect('/create')
    Recipe.save(request.form)
    return redirect('/home')

# @app.route('/edit')
# def edit_recipe():
#     return render_template('edit.html')

@app.route('/view/recipe/<int:post_id>')
def view_recipe(post_id):
    return render_template('view_recipe.html', current_user = User.getById({'id': session['user_id']}), recipe = Recipe.getById({'id':post_id}))

# @app.route('/show/<int:post_id>')
# def show(post_id):
#     return render_template("show.html", user = User.getById({'id':post_id}))

# @app.route('/edit/<int:post_id>')
# def edit(post_id):
#     return render_template('update.html', user = User.getById({'id':post_id}))
@app.route('/edit/<int:post_id>')
def edit(post_id):
    return render_template('edit.html', recipe = Recipe.getById({'id':post_id}))

@app.route('/update', methods=['post'])
def update():
    if not session['user_id']:
        redirect('/home')
    if not Recipe.validate_create(request.form):
        return redirect(f'/edit/{request.form["id"]}')
    Recipe.update(request.form)
    return redirect('/home')

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    Recipe.deleteById({'id':post_id})
    return redirect('/home')