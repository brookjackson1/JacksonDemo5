from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db

pizzas = Blueprint('pizzas', __name__)

@pizzas.route('/', methods=['GET', 'POST'])
def show_pizzas():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new pizza
    if request.method == 'POST':
        name = request.form['name']
        size = request.form['size']
        price = request.form['price']
        cost = request.form['cost']

        # Insert the new pizza into the database
        cursor.execute('INSERT INTO pizza (name, size, price, cost) VALUES (%s, %s, %s, %s)',
                       (name, size, price, cost))
        db.commit()

        flash('New pizza added successfully!', 'success')
        return redirect(url_for('pizzas.show_pizzas'))

    # Handle GET request to display all pizzas
    cursor.execute('SELECT * FROM pizza ORDER BY name, size')
    all_pizzas = cursor.fetchall()
    return render_template('pizzas.html', all_pizzas=all_pizzas)

@pizzas.route('/update_pizza/<int:pizza_id>', methods=['POST'])
def update_pizza(pizza_id):
    db = get_db()
    cursor = db.cursor()

    # Update the pizza's details
    name = request.form['name']
    size = request.form['size']
    price = request.form['price']
    cost = request.form['cost']

    cursor.execute('UPDATE pizza SET name = %s, size = %s, price = %s, cost = %s WHERE pizza_id = %s',
                   (name, size, price, cost, pizza_id))
    db.commit()

    flash('Pizza updated successfully!', 'success')
    return redirect(url_for('pizzas.show_pizzas'))

@pizzas.route('/delete_pizza/<int:pizza_id>', methods=['POST'])
def delete_pizza(pizza_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the pizza
    cursor.execute('DELETE FROM pizza WHERE pizza_id = %s', (pizza_id,))
    db.commit()

    flash('Pizza deleted successfully!', 'danger')
    return redirect(url_for('pizzas.show_pizzas'))
