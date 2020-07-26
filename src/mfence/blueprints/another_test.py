import flask

blueprint = flask.Blueprint("another_test", __name__)

@blueprint.route("/", methods=["GET", "POST"])
def another_test_page():
    return "<h1>Another test!</h1>"
