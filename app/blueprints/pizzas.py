from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
from app.blueprints.auth import login_required

pizzas = Blueprint('pizzas', __name__)

@pizzas.route('/', methods=['GET', 'POST'])
@login_required
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

    # Handle GET request to display all non-archived pizzas
    cursor.execute('SELECT * FROM pizza WHERE is_archived = FALSE ORDER BY name, size')
    all_pizzas = cursor.fetchall()
    return render_template('pizzas.html', all_pizzas=all_pizzas)

@pizzas.route('/update_pizza/<int:pizza_id>', methods=['POST'])
@login_required
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
@login_required
def delete_pizza(pizza_id):
    db = get_db()
    cursor = db.cursor()

    # Archive the pizza instead of deleting to preserve data integrity
    cursor.execute('UPDATE pizza SET is_archived = TRUE, archived_at = NOW() WHERE pizza_id = %s', (pizza_id,))
    db.commit()

    flash('Pizza archived successfully! Historical sales data preserved.', 'warning')
    return redirect(url_for('pizzas.show_pizzas'))
