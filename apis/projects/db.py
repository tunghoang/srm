from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

from ..projectStudentRels import Projectstudentrel
from ..projectAdvisorRels import Projectadvisorrel
from ..students import Student
from ..advisors import Advisor
from ..semesters import Semester
from ..projecttypes import Projecttype

__db = DbInstance.getInstance()



class Project(__db.Base):
  __tablename__ = "project"
  idProject = Column(Integer, primary_key = True)
  title = Column(Text)
  idProjecttype = Column(Integer, ForeignKey('projecttype.idProjecttype'))
  idSemester = Column(Integer, ForeignKey('semester.idSemester'))
  status = Column(String(20))
  grade = Column(Float)

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idProject" in dictModel) and (dictModel["idProject"] != None):
      self.idProject = dictModel["idProject"]
    if ("title" in dictModel) and (dictModel["title"] != None):
      self.title = dictModel["title"]
    if ("idProjecttype" in dictModel) and (dictModel["idProjecttype"] != None):
      self.idProjecttype = dictModel["idProjecttype"]
    if ("idSemester" in dictModel) and (dictModel["idSemester"] != None):
      self.idSemester = dictModel["idSemester"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]
    if ("grade" in dictModel) and (dictModel["grade"] != None):
      self.grade = dictModel["grade"]

  def __repr__(self):
    return '<Project idProject={} title={} idProjecttype={} idSemester={} status={} grade={} >'.format(self.idProject, self.title, self.idProjecttype, self.idSemester, self.status, self.grade, )

  def json(self):
    return {
      "idProject":self.idProject,"title":self.title,"idProjecttype":self.idProjecttype,"idSemester":self.idSemester,"status":self.status,"grade":self.grade,
    }

  def update(self, dictModel):
    if ("idProject" in dictModel) and (dictModel["idProject"] != None):
      self.idProject = dictModel["idProject"]
    if ("title" in dictModel) and (dictModel["title"] != None):
      self.title = dictModel["title"]
    if ("idProjecttype" in dictModel) and (dictModel["idProjecttype"] != None):
      self.idProjecttype = dictModel["idProjecttype"]
    if ("idSemester" in dictModel) and (dictModel["idSemester"] != None):
      self.idSemester = dictModel["idSemester"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]
    if ("grade" in dictModel) and (dictModel["grade"] != None):
      self.grade = dictModel["grade"]

def __recover():
  __db.newSession()

def __doList():
  return __db.session().query(Project).all()
  
def __doNew(instance):
  key = request.cookies.get('key')
  jwt = request.cookies.get('jwt')
  key = key if key is not None else request.headers.get('auth-key')
  jwt = jwt if jwt is not None else request.headers.get('authorization')

  sessionData = None
  if jwt is None or key is None:
    raise Unauthorized("Invalid request")
  elif key in session:
    salt = session[key]
    try:
      sessionData = doParseJWT(jwt, salt)
    except:
      raise Unauthorized("Invalid session")
  if sessionData['idStudent'] is None:
    raise BadRequest('Not allow to create project')

  try:
    __db.session().add(instance)
    __db.session().commit()
  except Exception as e:
    raise e

  projectStudentRelInst = Projectstudentrel({
    'idStudent': sessionData['idStudent'],
    'idProject': instance.idProject,
    'status': 1
  })

  try:
    __db.session().add(projectStudentRelInst)
    __db.session().commit()
  except Exception as e:
    raise BadRequest(e)

  return instance

def __doGet(id):
  instance = __db.session().query(Project).filter(Project.idProject == id).scalar()
  doLog("__doGet: {}".format(instance))
  return instance

def __doUpdate(id, model):
  instance = getProject(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getProject(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  if 'idAdvisor' in model:
    queryObj = __db.session().query(
      Project.idProject, 
      Project.title, 
      Project.status, 
      Project.grade, 
      Project.idSemester,
      Project.idProjecttype,
      Semester.year, Semester.semesterIndex,
      Projecttype.name,
      Projectadvisorrel.idProjectadvisorrel,
      Projectadvisorrel.idAdvisor,
      Projectadvisorrel.status,
      Advisor.fullname
    ).filter(
      Project.idSemester == Semester.idSemester,
      Project.idProjecttype == Projecttype.idProjecttype,
      Project.idProject == Projectadvisorrel.idProject,
      Projectadvisorrel.idAdvisor == Advisor.idAdvisor
    )
    queryObj = queryObj.filter(Projectadvisorrel.idAdvisor == model['idAdvisor'])
  elif 'idStudent' in model:
    queryObj = __db.session().query(
      Project.idProject, 
      Project.title, 
      Project.status, 
      Project.grade, 
      Project.idSemester,
      Project.idProjecttype,
      Semester.year, Semester.semesterIndex,
      Projecttype.name,
      Projectstudentrel.idProjectstudentrel,
      Projectstudentrel.idStudent,
      Projectstudentrel.status,
      Student.fullname, Student.studentNumber
    ).filter(
      Project.idSemester == Semester.idSemester,
      Project.idProjecttype == Projecttype.idProjecttype,
      Project.idProject == Projectstudentrel.idProject,
      Projectstudentrel.idStudent == Student.idStudent
    )
    queryObj = queryObj.filter(Projectstudentrel.idStudent == model['idStudent'])
  else:
    queryObj = __db.session().query(
      Project.idProject, 
      Project.title, 
      Project.status, 
      Project.grade, 
      Project.idSemester,
      Project.idProjecttype,
      Semester.year, Semester.semesterIndex,
      Projecttype.name
    ).filter(
      Project.idSemester == Semester.idSemester,
      Project.idProjecttype == Projecttype.idProjecttype
    )

  if 'title' in model:
    queryObj = queryObj.filter(Project.title.ilike(f'%{model["title"]}%'))
  if 'status' in model:
    queryObj = queryObj.filter(Project.status == model['status'])
  if 'idSemester' in model:
    queryObj = queryObj.filter(Project.idSemester == model['idSemester'])
  if 'idProjecttype' in model:
    queryObj = queryObj.filter(Project.idProjecttype == model['idProjecttype'])

  results = queryObj.all()

  return list(map(lambda x: {
    'idProject': x[0], 'title': x[1], 'status': x[2], 'grade': x[3], 'idSemester': x[4], 'idProjecttype': x[5], 'year': x[6],
    'semesterIndex': x[7], 'projecttypeName': x[8] 
  }, results))

def listProjects():
  doLog("list DAO function")
  try:
    return __doList()
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doList()
  except InterfaceError as e:
    doLog(e)
    __recover()
    return __doList()
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def newProject(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Project(model)
  res = False
  try:
    return __doNew(instance)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doNew(instance)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def getProject(id):
  doLog("get DAO function", id)
  try:
    return __doGet(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGet(id)
  except InterfaceError as e:
    doLog(e)
    __recover()
    return __doGet(id)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def updateProject(id, model):
  doLog("update DAO function. Model: {}".format(model))
  try:
    return __doUpdate(id, model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doUpdate(id, model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def deleteProject(id):
  doLog("delete DAO function", id)
  try:
    return __doDelete(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doDelete(id)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def findProject(model):
  doLog("find DAO function %s" % model)
  try:
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e
