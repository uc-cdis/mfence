from flask import Blueprint, render_template

blueprint = Blueprint('hello', __name__)

@blueprint.route("/hello")
def hello():
    return "Hello World!"
