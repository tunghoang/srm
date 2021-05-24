from .db_utils import DbInstance
from .app_utils import doParseJWT, doLog
from werkzeug.exceptions import *

def isStaff(request, session): 
  jwt = jwtFromRequest(request)
  key = keyFromRequest(request)
  salt = session[key]
  print(jwt + " " + key)
  sessionData = doParseJWT(jwt, salt)
  doLog(sessionData)
  if sessionData.get('idStaff', None) is not None:
    return True
  else:
    return False

def isIdGuestAdvisorMatched(request, session, idGuestAdvisor):
  jwt = jwtFromRequest(request)
  key = keyFromRequest(request)
  salt = session[key]
  print(jwt + " " + key)
  sessionData = doParseJWT(jwt, salt)
  doLog(sessionData)
  if sessionData.get('idGuestadvisor', None) == idGuestAdvisor:
    return True
  else:
    return False

def jwtFromRequest(request):
  jwt = request.cookies.get('jwt')
  jwt = jwt if jwt is not None else request.headers.get('authorization')
  return jwt

def keyFromRequest(request):
  key = request.cookies.get('key')
  key = key if key is not None else request.headers.get('auth-key')
  return key

def getIdStudentsOfProject(idProject):
  __db = DbInstance.getInstance()
  sql = "SELECT idStudent FROM projectStudentRel WHERE idProject = :idProject"
  results = __db.session().execute(sql, {'idProject':idProject}).fetchall();
  return list(map(lambda x: int(x[0]) if x[0] is not None else None, results))

def getRelatedIdStudents(idStudent, idProject):
  if idStudent is not None:
    return ( int(idStudent), )
  elif idProject is not None:
    return getIdStudentsOfProject(idProject)

def validateStudent(request, idStudent, idProject, session):
  relatedIdStudents = getRelatedIdStudents(idStudent, idProject)
  jwt = jwtFromRequest(request)
  key = keyFromRequest(request)
  salt = session[key]
  print(jwt + " " + key)
  sessionData = doParseJWT(jwt, salt)
  sessionIdStudent = sessionData.get('idStudent', None)
  doLog(relatedIdStudents)
  doLog(sessionIdStudent)
  if sessionIdStudent in relatedIdStudents :
    pass
  else:
    raise BadRequest("Wrong idStudent")

def checkKLTNExist(idStudent):
  __db = DbInstance.getInstance()
  sql = "SELECT * FROM projectStudentRel psr LEFT JOIN project prj ON psr.idProject = prj.idProject WHERE psr.idStudent=:idStudent AND prj.idProjecttype = 1"
  doLog(sql)
  results = __db.session().execute(sql, {'idStudent':idStudent}).fetchall()
  if len(results) > 0:
    raise BadRequest("Cannot create. KLTN exists")

def checkPrjtypeExistInSemester(idStudent, idProjecttype, idSemester):
  __db = DbInstance.getInstance()
  sql = """SELECT * 
    FROM projectStudentRel psr LEFT JOIN project prj ON psr.idProject = prj.idProject 
    WHERE psr.idStudent=:idStudent AND prj.idSemester = :idSemester AND prj.idProjecttype = :idProjecttype
  """
  results = __db.session().execute(sql, {'idStudent':idStudent, 'idProjecttype': idProjecttype, 'idSemester': idSemester}).fetchall()
  if len(results) > 0:
    raise BadRequest("Cannot create. Only one project of this type in a semester exists")

def verifyIdStudent(request, session, requestBody):
  jwt = jwtFromRequest(request)
  key = keyFromRequest(request)
  salt = session[key]
  print(jwt + " " + key)
  sessionData = doParseJWT(jwt, salt)
  doLog(sessionData)
  if sessionData.get('idStaff',None) is not None:
    pass
  elif sessionData.get('idAdvisor', None) is not None:
    pass
  else:
    idStudent = sessionData['idStudent']
    if int(requestBody['idStudent']) != idStudent:
      raise BadRequest("Invalid idStudent")

def checkPermissionProject(request, session, idProject):
  print("hic")
  try:
    jwt = jwtFromRequest(request)
    key = keyFromRequest(request)
    salt = session[key]
    print("hicc")
    sessionData = doParseJWT(jwt, salt)
    doLog("SessionData=%s" % sessionData)
    if sessionData.get('idStaff',None) is not None:
      pass
    elif sessionData.get('idAdvisor', None) is not None:
      pass
    else:
      idStudent = sessionData['idStudent']
      doLog(idStudent, True)
      prjIdStudents = getIdStudentsOfProject(idProject)
      print("hiccc")
      doLog(prjIdStudents, True)
      if len(prjIdStudents) > 0 and idStudent not in prjIdStudents:
        raise BadRequest("You are not allowed!")
  except Exception as e:
    print(e)
    raise BadRequest(str(e))

def shouldNotStudent(request, session):
  jwt = jwtFromRequest(request)
  key = keyFromRequest(request)
  salt = session[key]
  print(jwt + " " + key)
  sessionData = doParseJWT(jwt, salt)
  doLog(sessionData)
  if sessionData.get('idStaff',None) is not None:
    pass
  elif sessionData.get('idAdvisor', None) is not None:
    pass
  else:
    raise BadRequest("Insufficient privilege")

def shouldBeStaff(request, session):
  jwt = jwtFromRequest(request)
  key = keyFromRequest(request)
  salt = session[key]
  print(jwt + " " + key)
  sessionData = doParseJWT(jwt, salt)
  doLog(sessionData)
  if sessionData.get('idStaff',None) is not None:
    pass
  else:
    raise BadRequest("Insufficient privilege")

def onlyOneProjectTypeCondition(request, session, json) :
  jwt = jwtFromRequest(request)
  key = keyFromRequest(request)
  salt = session[key]
  print(jwt + " " + key)
  sessionData = doParseJWT(jwt, salt)
  doLog(sessionData)
  if sessionData.get('idStaff',None) is not None:
    pass
  elif sessionData.get('idAdvisor', None) is not None:
    pass
  else:
    idStudent = sessionData.get('idStudent', None)
    idProjecttype = json.get('idProjecttype', None)
    idSemester = json.get('idSemester', None)
    doLog("%s ;; %s ;; %s" % (idStudent, idProjecttype, idSemester))
    if idSemester is None:
      raise BadRequest('Invalid semester')
    if idProjecttype is None:
      raise BadRequest('Invalid projecttype')
    elif int(idProjecttype) == 1:
      checkKLTNExist(idStudent)
    else:
      checkPrjtypeExistInSemester(idStudent, idProjecttype, idSemester)
