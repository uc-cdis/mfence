import flask
from flask import make_response
import random

blueprint = flask.Blueprint("metrics", __name__)

@blueprint.route("/", methods=["GET", "POST"])
def metrics():
  users = ['alice', 'bob', 'mallet']
  idps = ['nih', 'google', 'microsoft']

  ficitious_metrics = {
#    'gcp_svc_acct_req_time{gcp_prj="customerA"}': round(random.uniform(1, 5), 2),
#    'oidc_transactions{{user={}, idp={}}}'.format(users[random.randint(0, 2)], idps[random.randint(0, 2)]): random.randint(1, 100),
#    'presigned_url_time{acl=phs000123}': round(random.uniform(1, 5), 2),
    'cirrus_retries': round(random.uniform(1, 100), 1),

#    'num_s3_operations': random.randint(1, 100),
#    'num_gs_operations': random.randint(1, 100),
#    'reqs_from_shepherd': random.randint(1, 100)
  }
  payload = ""
  for k,v in ficitious_metrics.items():
    payload += k + ' ' + str(v) + '\n'
  response = make_response(payload, 200)
  response.mimetype = "text/plain"
  return response
