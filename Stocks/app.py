import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, Engine

from api_views import blp
from extensions import db, migrate
from filters import JinjaFilters
from routes import routes_bp
from models import *
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}},expose_headers=["X-Pagination"])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'phones-database.db')
app.config["PROPAGATE_EXCEPTIONS"] = True
db.init_app(app)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

migrate.init_app(app,db)
app.register_blueprint(routes_bp)
app.register_blueprint(blp)

JinjaFilters(app).reg_in_jinja_filter()




if __name__ == '__main__':
    app.run()
