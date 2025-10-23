from flask import Blueprint, request, redirect, url_for, flash, session
from app.db_connect import get_db
from functools import wraps

auth = Blueprint('auth', __name__)

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def process_login():
    """Process login request and record login history"""
    username = request.form['username']
    password = request.form['password']

    db = get_db()
    if db is None:
        flash('Database connection error. Please contact support.', 'danger')
        return redirect(url_for('index'))

    cursor = db.cursor()

    # Get employee from database
    cursor.execute('SELECT * FROM employee WHERE username = %s', (username,))
    employee = cursor.fetchone()

    if employee and employee['password'] == password:
        # Set session variables
        session['user_id'] = employee['user_id']
        session['username'] = employee['username']
        session['first_name'] = employee['first_name']
        session['last_name'] = employee['last_name']

        # Record login in login_history table
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')[:255]  # Limit to 255 chars

        cursor.execute('''
            INSERT INTO login_history (user_id, ip_address, user_agent)
            VALUES (%s, %s, %s)
        ''', (employee['user_id'], ip_address, user_agent))
        db.commit()

        flash(f'Welcome back, {employee["first_name"]}!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password. Please try again.', 'danger')
        return redirect(url_for('index'))

@auth.route('/logout')
def logout():
    # Get name before clearing session
    first_name = session.get('first_name', 'User')

    # Clear session
    session.clear()

    flash(f'Goodbye, {first_name}! You have been logged out successfully.', 'info')
    return redirect(url_for('index'))
