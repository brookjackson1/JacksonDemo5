from flask import Flask, g
from .app_factory import create_app
from .db_connect import close_db, get_db

app = create_app()
app.secret_key = 'your-secret'  # Replace with an environment

# Register Blueprints
from app.blueprints.customers import customers
from app.blueprints.pizzas import pizzas
from app.blueprints.orders import orders

app.register_blueprint(customers, url_prefix='/customers')
app.register_blueprint(pizzas, url_prefix='/pizzas')
app.register_blueprint(orders, url_prefix='/orders')

from . import routes

@app.before_request
def before_request():
    g.db = get_db()
    if g.db is None:
        print("Warning: Database connection unavailable. Some features may not work.")

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)