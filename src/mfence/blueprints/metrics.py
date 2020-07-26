import flask
from flask import make_response
import random

blueprint = flask.Blueprint("metrics", __name__)

@blueprint.route("/", methods=["GET", "POST"])
def metrics():
  users = ['alice', 'bob', 'mallet']
  idps = ['nih', 'google', 'microsoft']

  ficitious_metrics = {
    'gcp_svc_acct_req_time{gcp_prj="customerA"}': round(random.uniform(1, 5), 1),
    'oidc_transactions{{user="{}", idp="{}"}}'.format(users[random.randint(0, 2)], idps[random.randint(0, 2)]): round(random.uniform(1, 100), 1),
    'presigned_url_time{acl="phs000123"}': round(random.uniform(1, 5), 1),
    'cirrus_retries': round(random.uniform(1, 100), 1),

    'num_s3_operations': round(random.uniform(1, 100), 1),
    'num_gs_operations': round(random.uniform(1, 100), 1),
    'reqs_from_shepherd': round(random.uniform(1, 100), 1)
  }
  payload = ""
  for k,v in ficitious_metrics.items():
    metric_name = k[:k.index('{')] if '{' in k else k
    payload += '# HELP {} describe metric here\n'.format(metric_name)
    payload += '# TYPE {} gauge\n'.format(metric_name)
    payload += k + ' ' + str(v) + '\n'
  response = make_response(payload, 200)
  response.mimetype = "text/plain"
  return response
