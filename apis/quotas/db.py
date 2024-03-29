from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Quota(__db.Base):
  __tablename__ = "quota"
  idQuota = Column(Integer, primary_key = True)
  name = Column(String(100))
  description = Column(String(255))
  n_kltn = Column(Integer)
  n_dakh = Column(Integer)

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idQuota" in dictModel) and (dictModel["idQuota"] != None):
      self.idQuota = dictModel["idQuota"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]
    if ("n_kltn" in dictModel) and (dictModel["n_kltn"] != None):
      self.n_kltn = dictModel["n_kltn"]
    if ("n_dakh" in dictModel) and (dictModel["n_dakh"] != None):
      self.n_dakh = dictModel["n_dakh"]

  def __repr__(self):
    return '<Quota idQuota={} name={} description={} n_kltn={} n_dakh={} >'.format(self.idQuota, self.name, self.description, self.n_kltn, self.n_dakh, )

  def json(self):
    return {
      "idQuota":self.idQuota,"name":self.name,"description":self.description,"n_kltn":self.n_kltn,"n_dakh":self.n_dakh,
    }

  def update(self, dictModel):
    if ("idQuota" in dictModel) and (dictModel["idQuota"] != None):
      self.idQuota = dictModel["idQuota"]
    if ("name" in dictModel) and (dictModel["name"] != None):
      self.name = dictModel["name"]
    if ("description" in dictModel) and (dictModel["description"] != None):
      self.description = dictModel["description"]
    if ("n_kltn" in dictModel) and (dictModel["n_kltn"] != None):
      self.n_kltn = dictModel["n_kltn"]
    if ("n_dakh" in dictModel) and (dictModel["n_dakh"] != None):
      self.n_dakh = dictModel["n_dakh"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Quota).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Quota).filter(Quota.idQuota == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getQuota(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getQuota(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  ''' implement quota checking here '''
  idSemester = model.get('idSemester', None)
  if idSemester is None:
    raise BadRequest('idSemester missing')
  whereClause = "WHERE sem.idSemester = :idSemester AND prj.idProjecttype = 1"
  params = {'idSemester':idSemester}

  if model.get('advisor', None) != None:
    whereClause += " AND adv.fullname like :advisor_pattern"
    params['advisor_pattern'] = f'%{model["advisor"]}%'

  queryStr = '''
    SELECT adv.idAdvisor, adv.fullname, sem.idSemester, sem.year, sem.semesterIndex, count(prj.title), quo.name, adv.idGuestadvisor, 
      quo.n_kltn, sum(1.0/subq.count) 
    FROM project prj
      LEFT JOIN (
        SELECT prj1.idProject, prj1.title, count(adv1.idAdvisor) count
        FROM project prj1 
          LEFT JOIN projectAdvisorRel par1
            ON prj1.idProject = par1.idProject
          RIGHT JOIN advisor adv1
            ON par1.idAdvisor = adv1.idAdvisor
        GROUP BY prj1.idProject, prj1.title
      ) subq
      ON prj.idProject = subq.idProject
      LEFT JOIN projectAdvisorRel par
        ON prj.idProject = par.idProject
      RIGHT JOIN advisor adv
        ON par.idAdvisor = adv.idAdvisor
      LEFT JOIN quota quo
        ON adv.idQuota = quo.idQuota
      LEFT JOIN projectStudentRel psr
        ON prj.idProject = psr.idProject
      RIGHT JOIN student stu
        ON psr.idStudent = stu.idStudent
      LEFT JOIN studentSemesterRel ssr
        ON stu.idStudent = ssr.idStudent
      RIGHT JOIN semester sem
        ON ssr.idSemester = sem.idSemester
  ''' + whereClause + '''
    GROUP BY adv.idAdvisor, adv.fullname, sem.idSemester, sem.year, sem.semesterIndex, quo.name, adv.idGuestadvisor, quo.n_kltn
  '''
  results = __db.session().execute(queryStr, params).fetchall()
  __db.session().commit()
  return list(map(lambda x: {'idAdvisor': x[0], 
      'advisor': x[1], 'semester': str(x[3]) + "-HK" + str(x[4]+1), 
      'count': x[5], 'title': x[6], 'idGuestadvisor':x[7], 'quota':x[8], 'count1': float(x[9])}, results))
  return results


def listQuotas():
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

def newQuota(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Quota(model)
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

def getQuota(id):
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

def updateQuota(id, model):
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

def deleteQuota(id):
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

def findQuota(model):
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
