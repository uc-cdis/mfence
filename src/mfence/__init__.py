import flask
from flask_cors import CORS

from werkzeug.middleware.dispatcher import DispatcherMiddleware
import prometheus_client
from prometheus_client import multiprocess, make_wsgi_app
#from prometheus_flask_exporter import PrometheusMetrics
from prometheus_flask_exporter.multiprocess import UWsgiPrometheusMetrics

from mfence.views import hello
from mfence.blueprints import test
from mfence.blueprints import another_test
from mfence.blueprints import other_metrics

registry = prometheus_client.CollectorRegistry()
multiprocess.MultiProcessCollector(registry)

app = flask.Flask(__name__)

app.secret_key = 'some key'

metrics = UWsgiPrometheusMetrics(app)

CORS(app=app, headers=["content-type", "accept"], expose_headers="*")

# static information as metric
metrics.info('app_info', 'Fence version info', version='4.24.3')

metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

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
    app.register_blueprint(other_metrics.blueprint, url_prefix="/other_metrics")

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

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app(registry=registry)
})
