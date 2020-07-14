from flask import request, make_response
import jwt
import traceback
import json
import requests


def error_page(code, title, description, publicDebug="", internalDebug=""):
  internalDebug += "\n\n" + "".join(traceback.format_stack())
  resp = make_response(
      json.dumps({
          "Code": code,
          "Title": title,
          "Description": description,
          "PublicDebug": publicDebug,
          "InternalDebug": internalDebug
      }), code)
  resp.headers["Content-Type"] = "ctfproxy/error"
  return resp


def get_user():
  with open("/jwtRS256.key.pub", 'r') as f:
    return jwt.decode(
        request.headers.get('X-CTFProxy-JWT'), f.read(), algorithms=['RS256'])


def get_username():
  username = get_user()["username"]
  return username.split("@")[0]
