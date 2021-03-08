from flask import Flask, redirect, url_for

def created_app(config=None):
    app = Flask(__name__)

    if config is not None:
        app.config.from_object(config)

    from dashboard.views import dashboard
    app.register_blueprint(dashboard, url_prefix='/dashboard')

    @app.route('/')
    def home():
        return "hola"

    return app