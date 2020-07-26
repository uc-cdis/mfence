import flask
from flask_cors import CORS

from mfence.views import hello
from mfence.blueprints import test
from mfence.blueprints import another_test
from mfence.blueprints import metrics

app = flask.Flask(__name__)
CORS(app=app, headers=["content-type", "accept"], expose_headers="*")

def warn_about_logger():
    raise Exception(
        "Flask 0.12 will remove and replace all of our log handlers if you call "
        "app.logger anywhere. Use get_logger from cdislogging instead."
    )

def app_init(
    app,
    root_dir=None,
    config_path=None,
    config_file_name=None,
):
    app.__dict__["logger"] = warn_about_logger

    app_register_blueprints(app)


def app_register_blueprints(app):
    app.register_blueprint(hello.blueprint)
    app.register_blueprint(test.blueprint, url_prefix="/test")
    app.register_blueprint(another_test.blueprint, url_prefix="/another_test")
    app.register_blueprint(metrics.blueprint, url_prefix="/metrics")

    @app.route("/")
    def root():
        """
        Register the root URL.
        """
        endpoints = {
            "test endpoint": "/test",
            "another_test endpoint": "/another_test",
        }
        return flask.jsonify(endpoints)
