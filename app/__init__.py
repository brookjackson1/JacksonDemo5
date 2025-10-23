from flask import Flask, g, session
from .app_factory import create_app
from .db_connect import close_db, get_db
import os

app = create_app()
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Register Blueprints
from app.blueprints.auth import auth
from app.blueprints.customers import customers
from app.blueprints.pizzas import pizzas
from app.blueprints.orders import orders

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(customers, url_prefix='/customers')
app.register_blueprint(pizzas, url_prefix='/pizzas')
app.register_blueprint(orders, url_prefix='/orders')

from . import routes

@app.before_request
def before_request():
    g.db = get_db()
    if g.db is None:
        print("Warning: Database connection unavailable. Some features may not work.")

@app.after_request
def add_header(response):
    """Add headers to prevent caching and back button navigation after logout"""
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)