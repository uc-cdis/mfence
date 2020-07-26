import flask

blueprint = flask.Blueprint("test", __name__)

@blueprint.route("/", methods=["GET", "POST"])
def test_info():
    info = {
      "dummy_data": "foo",
      "whatever": 123
    }
    return flask.jsonify(info)
