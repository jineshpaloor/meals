# -*- coding: utf-8 -*-

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, \
    render_template, flash
from flask import jsonify


# create our little application :)
app = Flask(__name__)

# Load default configuration and override configuration from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'meals_db.db'),
    DEBUG=True,
    SECRET_KEY='development key',
))


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        print 'get db'
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute(
        'select id, title, description, active, price from meal_entries  order by id desc')
    meals = cur.fetchall()
    return render_template('show_meals.html', meals=meals)


@app.route('/meal_detail_page/<int:meal_id>')
def meal_detail_page(meal_id):
    # query the meal and show
    db = get_db()
    cur = db.execute(
        'select title, description, price from meal_entries where active=1 and id=' + str(meal_id) + ' order by id desc')
    meal = cur.fetchone()

    if not meal:
        flash('You don\'t have permission to do that')
        return redirect(url_for('show_entries'))

    return render_template('meal_detail_page.html', meal=meal)


@app.route('/meal_edit_page/<int:meal_id>')
def meal_edit_page(meal_id):
    # query the meal and show
    db = get_db()
    cur = db.execute(
        'select title, description, price from meal_entries where active=1 and id=' + str(meal_id) + ' order by id desc')
    meal = cur.fetchone()

    if not meal:
        flash('You don\'t have permission to do that')
        return redirect(url_for('show_entries'))

    return render_template('meal_edit_page.html', meal=meal)


@app.route('/add_meals_page')
def add_meals_page():
    return render_template('add_meals.html')


@app.route('/save_meals', methods=['POST'])
def save_meals():
    title = request.form['title'].strip()
    description = request.form['description'].strip()
    price = request.form['price'].strip()
    active = request.form.getlist('active')
    if active:
        active_value = "1"
    else:
        active_value = "0"
    db = get_db()
    db.execute(
        'insert into meal_entries (title, description, active,price) values (?, ?, ?, ?  )',[title,description,active_value,float(price)]
    )
    db.commit()
    flash('New menu item is added successfully')
    return redirect(url_for('show_entries'))


@app.route('/edit_meals/<int:meal_id>', methods=['POST', 'GET'])
def edit_meals(meal_id):
    print '*'*100
    print 'args is :', request.args
    dic =  request.__dict__
    for i in dic.keys():
        print '*'*100
        print dic[i]
    #title = request.form['title'].strip()
    #description = request.form['description'].strip()
    #active = request.form['active'].strip()
    #price = request.form['price'].strip()

    db = get_db()
    db.execute(
        'UPDATE meal_entries SET title={0}, description={1}, active={2}, price={3} WHERE id={4}'.format(title, description, active, price, meal_id))
    db.commit()

    return jsonify({'success':True})


if __name__ == '__main__':
    init_db()
    app.run()
