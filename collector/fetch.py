import jwt
import os
import requests


def create_token(secret):
    payload = {
        'iat': 12312312312,
        'exp': 12312312312,
    }
    if os.environ.get("NAIS_CLUSTER_NAME"):
        payload["iss"] = os.environ.get("NAIS_APP_NAME") + "_" + os.environ.get("NAIS_CLUSTER_NAME")
        payload["iss_version"] = os.environ.get("NAIS_APP_IMAGE")
    else:
        payload["iss"] = "local"

    return jwt.encode(payload, secret, algorithm='HS256')


def make_authorized_request(url, data):
    token = create_token("hemmelig")
    r = requests.post(url=url, headers={"Authorization": "Bearer " + str(token)}, json=data)
    return r.text
