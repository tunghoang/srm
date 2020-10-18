from hashlib import sha256
from flask import jsonify
from jwt import encode, decode
from werkzeug.exceptions import *
SALT = 'fitresact'
def doHash(str):
  str1 = SALT + str
  hashObj = sha256(str1.encode('UTF-8'))
  return hashObj.hexdigest()
def doGenJWT(obj, salt):
  return encode(obj, salt)
def doParseJWT(key, salt):
  try:
    return decode(key, salt)
  except: 
    return None
def doLog(message, error = False):
  if error:
    print("*** %s" % message)
  else:
    print("--- %s" % message)
def doClear(dict):
  keys = [ k for k in dict ]
  for key in keys:
    del dict[key]
def matchOneOf(str, prefixes):
  for prefix in prefixes:
    if str.startswith(prefix):
      return True
  return False

def uidFromEmail(email):
  tokens = email.split('@')
  if len(tokens) != 2:
    raise BadRequest('Not valid email')
  return tokens[0]

def buildStudentRecordFromLDAPAttrs(attrs):
  return {
    'studentNumber': int(attrs['uid'][0].decode('utf-8')), 
    'email': f"{attrs['uid'][0].decode('utf-8')}@vnu.edu.vn",
    'fullname':attrs['cn'][0].decode('utf-8'), 
    'gender':True, 
    'dob': '2000-03-12'
  }

def buildAdvisorRecordFromLDAPAttrs(attrs):
  doLog(attrs)
  return {
    'email': f"{attrs['uid'][0].decode('utf-8')}@vnu.edu.vn",
    'fullname':attrs['cn'][0].decode('utf-8'),
    'idQuota': None,
    'idGuestadvisor': None
  }

