import flask
from prometheus_client import Gauge
from prometheus_client import Counter
import time
import random

c = Counter('my_failures', 'Description of counter')
g = Gauge('another_test_time', 'gauge example')

blueprint = flask.Blueprint("another_test", __name__)

@blueprint.route("/", methods=["GET", "POST"])
#@g.track_inprogress()
@c.count_exceptions()
def another_test_page():
    g.inc(21)
    try:
      time.sleep(random.randint(1,3))
      if (random.randint(0,3) == 3):
        raise Exception("illustrating exception counter")
    finally:
      g.dec(21)
    return "<h1>Another test!</h1>"
