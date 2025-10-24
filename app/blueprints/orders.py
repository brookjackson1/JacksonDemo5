from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
from app.blueprints.auth import login_required

orders = Blueprint('orders', __name__)

@orders.route('/', methods=['GET', 'POST'])
@login_required
def show_orders():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new order
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        date = request.form['date']

        # Insert the new order into the database
        cursor.execute('INSERT INTO `order` (customer_id, date) VALUES (%s, %s)',
                       (customer_id, date))
        db.commit()

        flash('New order added successfully!', 'success')
        return redirect(url_for('orders.show_orders'))

    # Handle GET request to display all orders with customer details
    cursor.execute('''
        SELECT o.order_id, o.customer_id, c.name as customer_name, o.date,
               o.created_at, o.updated_at
        FROM `order` o
        JOIN customer c ON o.customer_id = c.customer_id
        ORDER BY o.date DESC, o.order_id DESC
    ''')
    all_orders = cursor.fetchall()

    # Get all non-archived customers for the dropdown
    cursor.execute('SELECT customer_id, name FROM customer WHERE is_archived = FALSE ORDER BY name')
    all_customers = cursor.fetchall()

    return render_template('orders.html', all_orders=all_orders, all_customers=all_customers)

@orders.route('/update_order/<int:order_id>', methods=['POST'])
@login_required
def update_order(order_id):
    db = get_db()
    cursor = db.cursor()

    # Update the order's details
    customer_id = request.form['customer_id']
    date = request.form['date']

    cursor.execute('UPDATE `order` SET customer_id = %s, date = %s WHERE order_id = %s',
                   (customer_id, date, order_id))
    db.commit()

    flash('Order updated successfully!', 'success')
    return redirect(url_for('orders.show_orders'))

@orders.route('/delete_order/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    db = get_db()
    cursor = db.cursor()

    # Delete order details first (foreign key constraint)
    cursor.execute('DELETE FROM order_detail WHERE order_id = %s', (order_id,))

    # Delete the order
    cursor.execute('DELETE FROM `order` WHERE order_id = %s', (order_id,))
    db.commit()

    flash('Order and associated details deleted successfully!', 'danger')
    return redirect(url_for('orders.show_orders'))

@orders.route('/details/<int:order_id>')
@login_required
def order_details(order_id):
    db = get_db()
    cursor = db.cursor()

    # Get order information
    cursor.execute('''
        SELECT o.order_id, o.customer_id, c.name as customer_name, c.phone, c.email, o.date
        FROM `order` o
        JOIN customer c ON o.customer_id = c.customer_id
        WHERE o.order_id = %s
    ''', (order_id,))
    order = cursor.fetchone()

    if not order:
        flash('Order not found!', 'danger')
        return redirect(url_for('orders.show_orders'))

    # Get order details with pizza information
    cursor.execute('''
        SELECT od.order_detail_id, od.pizza_id, p.name as pizza_name, p.size,
               p.price, od.quantity, (p.price * od.quantity) as subtotal
        FROM order_detail od
        JOIN pizza p ON od.pizza_id = p.pizza_id
        WHERE od.order_id = %s
    ''', (order_id,))
    order_details = cursor.fetchall()

    # Get all non-archived pizzas for the dropdown
    cursor.execute('SELECT pizza_id, name, size, price FROM pizza WHERE is_archived = FALSE ORDER BY name, size')
    all_pizzas = cursor.fetchall()

    # Calculate totals
    from decimal import Decimal
    subtotal = sum(detail['subtotal'] for detail in order_details)
    tax_rate = Decimal('0.07')  # 7% sales tax
    tax = subtotal * tax_rate
    total = subtotal + tax

    return render_template('order_details.html', order=order, order_details=order_details,
                         all_pizzas=all_pizzas, subtotal=subtotal, tax=tax, total=total, tax_rate=tax_rate)

@orders.route('/details/<int:order_id>/add', methods=['POST'])
@login_required
def add_order_detail(order_id):
    db = get_db()
    cursor = db.cursor()

    pizza_id = request.form['pizza_id']
    quantity = request.form['quantity']

    # Insert the new order detail
    cursor.execute('INSERT INTO order_detail (order_id, pizza_id, quantity) VALUES (%s, %s, %s)',
                   (order_id, pizza_id, quantity))
    db.commit()

    flash('Pizza added to order successfully!', 'success')
    return redirect(url_for('orders.order_details', order_id=order_id))

@orders.route('/details/update/<int:order_detail_id>', methods=['POST'])
@login_required
def update_order_detail(order_detail_id):
    db = get_db()
    cursor = db.cursor()

    pizza_id = request.form['pizza_id']
    quantity = request.form['quantity']
    order_id = request.form['order_id']

    cursor.execute('UPDATE order_detail SET pizza_id = %s, quantity = %s WHERE order_detail_id = %s',
                   (pizza_id, quantity, order_detail_id))
    db.commit()

    flash('Order detail updated successfully!', 'success')
    return redirect(url_for('orders.order_details', order_id=order_id))

@orders.route('/details/delete/<int:order_detail_id>', methods=['POST'])
@login_required
def delete_order_detail(order_detail_id):
    db = get_db()
    cursor = db.cursor()

    # Get order_id before deleting
    cursor.execute('SELECT order_id FROM order_detail WHERE order_detail_id = %s', (order_detail_id,))
    result = cursor.fetchone()
    order_id = result['order_id']

    # Delete the order detail
    cursor.execute('DELETE FROM order_detail WHERE order_detail_id = %s', (order_detail_id,))
    db.commit()

    flash('Item removed from order successfully!', 'danger')
    return redirect(url_for('orders.order_details', order_id=order_id))
