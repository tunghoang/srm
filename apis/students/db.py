from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

from ..sec_utils import *
__db = DbInstance.getInstance()



class Student(__db.Base):
  __tablename__ = "student"
  idStudent = Column(Integer, primary_key = True)
  studentNumber = Column(Integer)
  email = Column(String(100))
  fullname = Column(String(150))
  dob = Column(Date)
  gender = Column(Boolean)
  klass = Column(String(20))
  idKlass = Column(Integer, ForeignKey('klass.idKlass'))
  mobile = Column(String(20))
  notified = Column(Boolean)

  constraints = list()
  constraints.append(UniqueConstraint('studentNumber'))
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idStudent" in dictModel) and (dictModel["idStudent"] != None):
      self.idStudent = dictModel["idStudent"]
    if ("studentNumber" in dictModel) and (dictModel["studentNumber"] != None):
      self.studentNumber = dictModel["studentNumber"]
    if ("email" in dictModel) and (dictModel["email"] != None):
      self.email = dictModel["email"]
    if ("fullname" in dictModel) and (dictModel["fullname"] != None):
      self.fullname = dictModel["fullname"]
    if ("dob" in dictModel) and (dictModel["dob"] != None):
      self.dob = dictModel["dob"]
    if ("gender" in dictModel) and (dictModel["gender"] != None):
      self.gender = dictModel["gender"]
    if ("klass" in dictModel) and (dictModel["klass"] != None):
      self.klass = dictModel["klass"]
    if ("idKlass" in dictModel) and (dictModel["idKlass"] != None):
      self.idKlass = dictModel["idKlass"]
    if ("mobile" in dictModel) and (dictModel["mobile"] != None):
      self.mobile = dictModel["mobile"]
    if ("notified" in dictModel) and (dictModel["notified"] != None):
      self.notified = dictModel["notified"]

  def __repr__(self):
    return '<Student idStudent={} studentNumber={} email={} fullname={} dob={} gender={} klass={} idKlass={} mobile={} notified={} >'.format(self.idStudent, self.studentNumber, self.email, self.fullname, self.dob, self.gender, self.klass, self.idKlass, self.mobile, self.notified, )

  def json(self):
    return {
      "idStudent":self.idStudent,"studentNumber":self.studentNumber,"email":self.email,"fullname":self.fullname,"dob":str(self.dob),"gender":self.gender,"klass":self.klass,"idKlass":self.idKlass,"mobile":self.mobile,"notified":self.notified,
    }

  def update(self, dictModel):
    if ("idStudent" in dictModel) and (dictModel["idStudent"] != None):
      self.idStudent = dictModel["idStudent"]
    if ("studentNumber" in dictModel) and (dictModel["studentNumber"] != None):
      self.studentNumber = dictModel["studentNumber"]
    if ("email" in dictModel) and (dictModel["email"] != None):
      self.email = dictModel["email"]
    if ("fullname" in dictModel) and (dictModel["fullname"] != None):
      self.fullname = dictModel["fullname"]
    if ("dob" in dictModel) and (dictModel["dob"] != None):
      self.dob = dictModel["dob"]
    if ("gender" in dictModel) and (dictModel["gender"] != None):
      self.gender = dictModel["gender"]
    if ("klass" in dictModel) and (dictModel["klass"] != None):
      self.klass = dictModel["klass"]
    if ("idKlass" in dictModel) and (dictModel["idKlass"] != None):
      self.idKlass = dictModel["idKlass"]
    if ("mobile" in dictModel) and (dictModel["mobile"] != None):
      self.mobile = dictModel["mobile"]
    if ("notified" in dictModel) and (dictModel["notified"] != None):
      self.notified = dictModel["notified"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Student).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Student).filter(Student.idStudent == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getStudent(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getStudent(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  if 'email' in model:
    results = __db.session().query(Student).filter(Student.email.ilike(f"%{model['email']}%")).all()
  elif 'fullname' in model:
    results = __db.session().query(Student).filter(Student.fullname.ilike(f"%{model['fullname']}%")).all()
  else:
    results = __db.session().query(Student).filter_by(**model).all()
  __db.session().commit()
  return results


def listStudents():
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

def newStudent(model):
  shouldNotStudent(request, session)
  doLog("new DAO function. model: {}".format(model))
  instance = Student(model)
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

def getStudent(id):
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

def updateStudent(id, model):
  verifyIdStudent(request, session, {'idStudent': id})
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

def deleteStudent(id):
  shouldNotStudent(request, session)
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

def findStudent(model):
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
  except Exception as e:
    raise BadRequest(f"Error: {e}")

def sendNotification(student):
  shouldBeStaff(request, session)
  doLog(f"send email notification for student {student['studentNumber']}")
  try:
    notify4IncompleteProfile(student)
    return {success: true}
  except Exception as e:
    raise BadRequest(str(e))
