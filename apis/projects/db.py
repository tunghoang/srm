from sqlalchemy import ForeignKey, Column, distinct, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request,send_from_directory

from ..projectStudentRels import Projectstudentrel
from ..projectAdvisorRels import Projectadvisorrel
from ..students import Student
from ..advisors import Advisor
from ..semesters import Semester
from ..projecttypes import Projecttype
from ..configs.db import findConfig

from ..sec_utils import *

__db = DbInstance.getInstance()



class Project(__db.Base):
  __tablename__ = "project"
  idProject = Column(Integer, primary_key = True)
  title = Column(Text)
  idProjecttype = Column(Integer, ForeignKey('projecttype.idProjecttype'))
  idSemester = Column(Integer, ForeignKey('semester.idSemester'))
  status = Column(String(20))
  grade = Column(Float)
  titleConfirm = Column(Integer)
  description = Column(Text)

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
    if ("titleConfirm" in dictModel) and (dictModel["titleConfirm"] != None):
      self.titleConfirm = dictModel["titleConfirm"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

  def __repr__(self):
    return '<Project idProject={} title={} idProjecttype={} idSemester={} status={} grade={} titleConfirm={} description={} >'.format(self.idProject, self.title, self.idProjecttype, self.idSemester, self.status, self.grade, self.titleConfirm, self.description, )

  def json(self):
    return {
      "idProject":self.idProject,"title":self.title,"idProjecttype":self.idProjecttype,"idSemester":self.idSemester,"status":self.status,"grade":self.grade,"titleConfirm":self.titleConfirm,"description":self.description,
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
    if ("titleConfirm" in dictModel) and (dictModel["titleConfirm"] != None):
      self.titleConfirm = dictModel["titleConfirm"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Project).all()
  __db.session().commit()
  return result  
  
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
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  configs = findConfig({'key': 'Allow edit project'})
  if (configs[0].value == ""):
    raise BadRequest("Không thể sửa đổi được do đang không trong thời gian sửa đổi để tài");
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
  whereClause = "WHERE 1=1"
  whereClause1 = "WHERE 1=1"
  params = { }
  if model.get('email', None) != None:
    whereClause += " AND stu.email like :email_pattern"
    params['email_pattern'] = f'%{model["email"]}%'
  if model.get('fullname', None) != None:
    whereClause += " AND stu.fullname like :fullname_pattern"
    params['fullname_pattern'] = f'%{model["fullname"]}%'
  if model.get('title', None) != None:
    whereClause += " AND prj.title like :title_pattern"
    params['title_pattern'] = f'%{model["title"]}%'
  if model.get('idProjecttype', None) != None:
    whereClause += " AND pt.idProjecttype = :idProjecttype"
    params['idProjecttype'] = model['idProjecttype']
  if model.get('idSemester', None) != None:
    whereClause += " AND prj.idSemester = :idSemester"
    params['idSemester'] = model['idSemester']
  if model.get('status', None) != None:
    whereClause += " AND prj.status = :status"
    params['status'] = model['status']
  if model.get('members', None) != None:
    whereClause1 += " AND members like :member_pattern"
    params['member_pattern'] = f'%{model["members"]}%'
  if model.get('advisors', None) != None:
    whereClause1 += " AND advisors like :advisor_pattern"
    params['advisor_pattern'] = f'%{model["advisors"]}%'
  if model.get('idAdvisor', None) != None:
    whereClause1 += " AND JSON_CONTAINS(advisorIds, :idAdvisor, '$') = 1"
    params['idAdvisor'] = model["idAdvisor"]
  if model.get('idStudent', None) != None:
    #whereClause1 += " AND JSON_CONTAINS(memberIds, :idStudent, '$') = 1"
    whereClause1 += " AND idStudent = :idStudent"
    params['idStudent'] = model["idStudent"]

  queryStr = """
    SELECT prj.title, prj.status, pt.name, sem.year, sem.semesterIndex, prj.idProject, JSON_ARRAYAGG(prjAdv.status) as confirmeds,
      GROUP_CONCAT(adv.fullname SEPARATOR ',') as advisors, stu.fullname as members, stu.studentNumber as MSSV,
      JSON_ARRAYAGG(adv.idAdvisor) as advisorIds, stu.idStudent as idStudent, prj.titleConfirm as titleConfirm,
      att.idAttachment, att.advisorApproved, att.title as attTitle
    FROM projecttype as pt
      RIGHT JOIN project as prj
        ON prj.idProjecttype = pt.idProjecttype
      LEFT JOIN attachment as att
        ON prj.idProject = att.idProject
      LEFT JOIN projectStudentRel as prjStu 
        ON prj.idProject = prjStu.idProject
      LEFT JOIN student as stu
        on prjStu.idStudent = stu.idStudent
      JOIN semester as sem 
        ON prj.idSemester = sem.idSemester
      LEFT JOIN projectAdvisorRel as prjAdv
        ON prj.idProject = prjAdv.idProject
      LEFT JOIN advisor as adv
        ON prjAdv.idAdvisor = adv.idAdvisor
  """
  queryStr += whereClause
  groupbyClause = '\n GROUP BY prj.title, prj.status, pt.name, sem.year, sem.semesterIndex, prj.idProject, stu.fullname, stu.studentNumber, stu.idStudent, prj.titleConfirm, att.idAttachment, att.advisorApproved, att.title'

  queryStr += groupbyClause
  queryStr = "SELECT * FROM (" + queryStr + ") q " + whereClause1
  doLog(queryStr)
  doLog(params)

  results = __db.session().execute(queryStr, params).fetchall()
  __db.session().commit()
  return list(map(lambda x: {'project_title': x[0], 'project_status': x[1], 'project_type': x[2], 'semester_year': x[3], 'semester_semesterIndex': x[4], 'idProject':x[5], 'confirmeds': x[6], 'advisors': x[7], 'student':x[8], 'studentNumber': x[9], 'idAdvisors': x[10], 'titleConfirm':x[12], 'idAttachment': x[13], 'advisorApproved': x[14], 'attachmentTitle': x[15]}, results))


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
  onlyOneProjectTypeCondition(request, session, request.get_json())
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
  checkPermissionProject(request, session, id)

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
  checkPermissionProject(request, session, id)

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
  verifyIdStudent(request, session, request.get_json())
  doLog("find DAO function %s" % model)
  try:
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)
  except SQLAlchemyError as e:
    doLog(e, True);
    __db.session().rollback()
    raise e

def exportMatchedProjects(model):
  doLog('exportMachedProjects %s' % model)
  try:
    projects = findProject(model)
    df = toDataFrame(projects)
    df.to_excel('public/projects.xlsx', index=False, engine='xlsxwriter')
    doLog('Before sending file')
    return send_from_directory('public', 'projects.xlsx')
  except Exception as e:
    doLog('Exception %s ' % str(e), True);
    raise BadRequest(str(e))
