import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from database_singleton import Singleton
from project.api.views import category_blueprint
from project.api.views import request_blueprint

# instantiate the app
def create_app(script_info=None):
    # Instantiate the app
    app = Flask(__name__)

    # Set Configuration
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db = Singleton().database_connection()
    migrate = Singleton().migration()

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(category_blueprint)
    app.register_blueprint(request_blueprint)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app


app = create_app()


@app.route("/users/ping", methods=["GET"])
def ping_pong():
    return jsonify({"status": "success", "message": "pong!"})
