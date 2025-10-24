from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
from app.blueprints.auth import login_required

customers = Blueprint('customers', __name__)

@customers.route('/', methods=['GET', 'POST'])
@login_required
def show_customers():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new customer
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        # Insert the new customer into the database
        cursor.execute('INSERT INTO customer (name, phone, email) VALUES (%s, %s, %s)',
                       (name, phone, email))
        db.commit()

        flash('New customer added successfully!', 'success')
        return redirect(url_for('customers.show_customers'))

    # Handle GET request to display all non-archived customers
    cursor.execute('SELECT * FROM customer WHERE is_archived = FALSE')
    all_customers = cursor.fetchall()
    return render_template('customers.html', all_customers=all_customers)

@customers.route('/update_customer/<int:customer_id>', methods=['POST'])
@login_required
def update_customer(customer_id):
    db = get_db()
    cursor = db.cursor()

    # Update the customer's details
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']

    cursor.execute('UPDATE customer SET name = %s, phone = %s, email = %s WHERE customer_id = %s',
                   (name, phone, email, customer_id))
    db.commit()

    flash('Customer updated successfully!', 'success')
    return redirect(url_for('customers.show_customers'))

@customers.route('/delete_customer/<int:customer_id>', methods=['POST'])
@login_required
def delete_customer(customer_id):
    db = get_db()
    cursor = db.cursor()

    # Archive the customer instead of deleting to preserve data integrity
    cursor.execute('UPDATE customer SET is_archived = TRUE, archived_at = NOW() WHERE customer_id = %s', (customer_id,))
    db.commit()

    flash('Customer archived successfully! Historical order data preserved.', 'warning')
    return redirect(url_for('customers.show_customers'))

@customers.route('/archived')
@login_required
def archived_customers():
    db = get_db()
    cursor = db.cursor()

    # Get all archived customers
    cursor.execute('SELECT * FROM customer WHERE is_archived = TRUE ORDER BY archived_at DESC')
    archived_customers = cursor.fetchall()

    return render_template('archived_customers.html', archived_customers=archived_customers)

@customers.route('/restore_customer/<int:customer_id>', methods=['POST'])
@login_required
def restore_customer(customer_id):
    db = get_db()
    cursor = db.cursor()

    # Restore the customer by setting is_archived to FALSE
    cursor.execute('UPDATE customer SET is_archived = FALSE, archived_at = NULL WHERE customer_id = %s', (customer_id,))
    db.commit()

    flash('Customer restored successfully!', 'success')
    return redirect(url_for('customers.archived_customers'))
