from flask import Flask, session, request
from apis import api
from apis.db_utils import DbInstance
from apis.app_utils import *
from flask_session import Session
from werkzeug.exceptions import *
from werkzeug.contrib.fixers import ProxyFix
import os

db = DbInstance.getInstance()
__SESSION_DIR = '/tmp/srm'
if not os.path.isdir(__SESSION_DIR):
  os.mkdir(__SESSION_DIR);
app = Flask(__name__, static_url_path='/public', static_folder='public')
#app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['DEBUG'] = False
app.config['JSON_AS_ASCII'] = False
app.config['SERVER_NAME'] = os.getenv("SERVER_NAME","localhost:8000")
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = __SESSION_DIR
#app.config['SESSION_COOKIE_SECURE'] = True
app.secret_key = os.urandom(16)
api.init_app(app)

Session(app)

@app.before_request
def before_request():
  print("Request: " + request.path)
  key = request.cookies.get('key')
  jwt = request.cookies.get('jwt')
  key = key if key is not None else request.headers.get('auth-key')
  jwt = jwt if jwt is not None else request.headers.get('authorization')
  no_auth_routes = ('/', '/favicon.ico', '/swagger.json' )
  #no_auth_prefixes = ( '/swaggerui', '/')
  no_auth_prefixes = ( '/swaggerui', '/studentlogin', '/stafflogin', '/advisorlogin', '/guestlogin', '/upload' )

  print(key)
  print(jwt)
  if request.path in no_auth_routes or matchOneOf(request.path, no_auth_prefixes) :
    return None
  elif jwt is None or key is None:
    raise Unauthorized("Invalid request")
  elif key in session:
    salt = session[key]
    try:
      sessionData = doParseJWT(jwt, salt)
    except:
      raise Unauthorized("Invalid session")
  else:
    raise Unauthorized("Not login")

  print("Ok")
  return None

@app.after_request
def after_request(resp):
  host = request.headers.get('Host')
  resp.headers['Access-Control-Allow-Origin'] = 'http://' + host
  return resp

db.Base.metadata.create_all(db.engine)

if __name__ == "__main__":
  app.run()
