import flask
from flask import request, session

from prometheus_client import Counter

blueprint = flask.Blueprint("test", __name__)

c = Counter('test_info_requests', 'test_info requests', ['client_ip', 'endpoint'])
# _total suffix is added automagically
# two labels

@blueprint.route("/", methods=["GET", "POST"])
def test_info():
    session['Username'] = 'Admin'
    c.labels(request.remote_addr, 'test').inc()
    info = {
      "dummy_data": "foo",
      "whatever": 123
    }
    return flask.jsonify(info)
