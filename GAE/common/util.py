import json
import logging
from os import environ

from google.appengine.api import app_identity, urlfetch

debug = environ.get('SERVER_SOFTWARE', '').startswith('Dev')
app_id = app_identity.get_application_id()
app_url = "https://cognitive-services-project.appspot.com/"


# def hash_password(raw_password):
#     import base64
#     import hashlib
#     algo = hashlib.sha256()
#     algo.update(raw_password)
#     return base64.b64encode(algo.digest())


# def generate_password(size=8):
#     import random
#     import string
#     chars = string.ascii_uppercase + string.digits
#     return ''.join(random.choice(chars) for _ in range(size))


def log_json(text):
    logging.debug('%s' % json.dumps(text,
                                    indent=4,
                                    skipkeys=True,
                                    ensure_ascii=False,
                                    encoding="utf-8"))
