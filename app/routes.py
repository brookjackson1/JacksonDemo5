from flask import render_template, redirect, url_for, session, request
from . import app
from app.blueprints.auth import login_required

@app.route('/', methods=['GET', 'POST'])
def index():
    from app.blueprints.auth import process_login
    # If user is logged in, redirect to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    # Handle login POST request
    if request.method == 'POST':
        return process_login()

    # Otherwise show login page
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    from app.db_connect import get_db
    from datetime import datetime

    db = get_db()
    cursor = db.cursor()

    # Get total customers
    cursor.execute('SELECT COUNT(*) as count FROM customer')
    customer_count = cursor.fetchone()['count']

    # Get total sales for current year
    current_year = datetime.now().year
    cursor.execute('''
        SELECT COALESCE(SUM(od.quantity * p.price), 0) as total_sales
        FROM `order` o
        JOIN order_detail od ON o.order_id = od.order_id
        JOIN pizza p ON od.pizza_id = p.pizza_id
        WHERE YEAR(o.date) = %s
    ''', (current_year,))
    total_sales = cursor.fetchone()['total_sales']

    # Get total pizzas in inventory
    cursor.execute('SELECT COUNT(*) as count FROM pizza')
    pizza_count = cursor.fetchone()['count']

    # Get recent orders (last 5)
    cursor.execute('''
        SELECT
            o.order_id,
            o.date,
            c.name as customer_name,
            COUNT(od.order_detail_id) as item_count,
            SUM(od.quantity * p.price) as order_total
        FROM `order` o
        JOIN customer c ON o.customer_id = c.customer_id
        JOIN order_detail od ON o.order_id = od.order_id
        JOIN pizza p ON od.pizza_id = p.pizza_id
        GROUP BY o.order_id, o.date, c.name
        ORDER BY o.date DESC, o.order_id DESC
        LIMIT 5
    ''')
    recent_orders = cursor.fetchall()

    return render_template('dashboard.html',
                         customer_count=customer_count,
                         total_sales=total_sales,
                         pizza_count=pizza_count,
                         recent_orders=recent_orders,
                         current_year=current_year)

@app.route('/about')
def about():
    # About page is accessible to everyone
    return render_template('about.html')

@app.route('/profile')
@login_required
def profile():
    from app.db_connect import get_db

    db = get_db()
    cursor = db.cursor()

    # Get employee details
    cursor.execute('SELECT * FROM employee WHERE user_id = %s', (session['user_id'],))
    employee = cursor.fetchone()

    # Get login history for this employee
    cursor.execute('''
        SELECT login_timestamp, ip_address, user_agent
        FROM login_history
        WHERE user_id = %s
        ORDER BY login_timestamp DESC
        LIMIT 10
    ''', (session['user_id'],))
    login_history = cursor.fetchall()

    return render_template('profile.html', employee=employee, login_history=login_history)
