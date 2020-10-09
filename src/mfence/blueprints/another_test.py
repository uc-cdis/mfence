import flask
from prometheus_client import Gauge
from prometheus_client import Counter
import time
import random

c = Counter('my_failures', 'Description of counter')
g = Gauge('another_test_time', 'gauge example')
google_svc_acct_patch = Counter('google_svc_acct_path', 'tracking gcp svc acct patch requests', ['num_of_projects', 'svc_account'])
num_users_per_project = Gauge('num_users_per_project', 'num of users with permissions to access a given project', ['project'])

blueprint = flask.Blueprint("another_test", __name__)

@blueprint.route("/", methods=["GET", "POST"])
@g.track_inprogress()
@c.count_exceptions()
def another_test_page():
    google_svc_acct_patch.labels(3, 'scientist.svc.acct1@someuniversity.iam.gserviceaccount.com').inc()
    google_svc_acct_patch.labels(1, 'scientist.svc.acct2@someuniversity.iam.gserviceaccount.com').inc()
    try:
      # before running usersync
      num_users_per_project.labels('1000Genomes').inc(200)
      num_users_per_project.labels('CMG-Broad-GRU').inc(50)

      time.sleep(random.randint(5,7))
      if (random.randint(0,3) == 3):
        raise Exception("illustrating exception counter")
    finally:
      print('Done')
      # after usersync
      num_users_per_project.labels('1000Genomes').dec(20)
    return "<h1>Another test!</h1>"
