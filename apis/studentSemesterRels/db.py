from sqlalchemy import ForeignKey, Column, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from ..semesters import Semester
from ..projects import Project
from ..students import Student
from ..projectStudentRels import Projectstudentrel
from ..projecttypes import Projecttype
from werkzeug.exceptions import *
from flask import session,request,after_this_request

from ..sec_utils import *

__db = DbInstance.getInstance()



class Studentsemesterrel(__db.Base):
  __tablename__ = "studentSemesterRel"
  idStudentsemesterrel = Column(Integer, primary_key = True)
  idSemester = Column(Integer, ForeignKey('semester.idSemester'))
  idStudent = Column(Integer, ForeignKey('student.idStudent'))
  removed = Column(Integer)

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idStudentsemesterrel" in dictModel) and (dictModel["idStudentsemesterrel"] != None):
      self.idStudentsemesterrel = dictModel["idStudentsemesterrel"]
    if ("idSemester" in dictModel) and (dictModel["idSemester"] != None):
      self.idSemester = dictModel["idSemester"]
    if ("idStudent" in dictModel) and (dictModel["idStudent"] != None):
      self.idStudent = dictModel["idStudent"]
    if ("removed" in dictModel) and (dictModel["removed"] != None):
      self.removed = dictModel["removed"]

  def __repr__(self):
    return '<Studentsemesterrel idStudentsemesterrel={} idSemester={} idStudent={} removed={} >'.format(self.idStudentsemesterrel, self.idSemester, self.idStudent, self.removed, )

  def json(self):
    return {
      "idStudentsemesterrel":self.idStudentsemesterrel,"idSemester":self.idSemester,"idStudent":self.idStudent,"removed":self.removed,
    }

  def update(self, dictModel):
    if ("idStudentsemesterrel" in dictModel) and (dictModel["idStudentsemesterrel"] != None):
      self.idStudentsemesterrel = dictModel["idStudentsemesterrel"]
    if ("idSemester" in dictModel) and (dictModel["idSemester"] != None):
      self.idSemester = dictModel["idSemester"]
    if ("idStudent" in dictModel) and (dictModel["idStudent"] != None):
      self.idStudent = dictModel["idStudent"]
    if ("removed" in dictModel) and (dictModel["removed"] != None):
      self.removed = dictModel["removed"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Studentsemesterrel).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Studentsemesterrel).filter(Studentsemesterrel.idStudentsemesterrel == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getStudentsemesterrel(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getStudentsemesterrel(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  whereClause = "WHERE sem.idSemester = :idSemester AND pt.idProjecttype = :idProjecttype"
  whereClause1 = "WHERE 1=1"
  params = {
    'idSemester': model['idSemester'],
    'idProjecttype': 1
  }
  if model.get('title', None) != None:
    whereClause += " AND prj.title like :title_pattern"
    params['title_pattern'] = f'%{model["title"]}%'
  if model.get('studentNumber', None) != None:
    whereClause += " AND stu.studentNumber = :studentNumber"
    params['studentNumber'] = model["studentNumber"]
  if model.get('fullname', None) != None:
    whereClause += " AND stu.fullname like :fullname_pattern"
    params['fullname_pattern'] = f'%{model["fullname"]}%'
  if model.get('advisors', None) != None:
    whereClause1 += " AND advisors like :advisor_pattern"
    params['advisor_pattern'] = f'%{model["advisors"]}%'

  queryStr = """
    SELECT prj.title, prj.status, pt.name, stu.studentNumber, stu.fullname, sem.year, sem.semesterIndex, stuSem.idStudentSemesterRel, stu.dob, k.className, 
      GROUP_CONCAT(adv.fullname SEPARATOR ',') as advisors,
      GROUP_CONCAT(IFNULL(guest.affiliation, 'DHCN') SEPARATOR ',') as affiliations,
      prj.titleConfirm
    FROM projecttype as pt
      RIGHT JOIN project as prj
        ON prj.idProjecttype = pt.idProjecttype
      RIGHT JOIN projectStudentRel as prjStu 
        ON prj.idProject = prjStu.idProject
      LEFT JOIN student as stu
        on prjStu.idStudent = stu.idStudent
      LEFT JOIN klass as k
        on stu.idKlass = k.idKlass
      RIGHT JOIN studentSemesterRel as stuSem
        ON stu.idStudent = stuSem.idStudent
      LEFT JOIN semester as sem 
        ON stuSem.idSemester = sem.idSemester
      LEFT JOIN projectAdvisorRel as prjAdv
        ON prj.idProject = prjAdv.idProject
      LEFT JOIN advisor as adv
        ON prjAdv.idAdvisor = adv.idAdvisor
      LEFT JOIN guestadvisor as guest
        ON adv.idGuestadvisor = guest.idGuestadvisor
  """
  queryStr += whereClause
  groupbyClause = '\n GROUP BY prj.title, prj.status, pt.name, stu.studentNumber, stu.fullname, sem.year, sem.semesterIndex, stuSem.idStudentSemesterRel, stu.dob, k.className, prj.titleConfirm'
  queryStr += groupbyClause
  queryStr = """
    SELECT *,
	RIGHT(fullname, INSTR(REVERSE(fullname), " ") - 1) as name,
	LEFT(fullname, CHAR_LENGTH(fullname) - INSTR(REVERSE(fullname), " ")) as firstAndMiddleName
    FROM (%s) q 
    %s
    ORDER BY className, name, firstAndMiddleName
  """ % (queryStr, whereClause1)
  doLog(queryStr)
  doLog(params)

  results = __db.session().execute(queryStr, params).fetchall()
  __db.session().commit()
  return list(map(lambda x: {
    'student_studentNumber': x[3], 
    'student_fullname': x[4], 
    'student_dob': str(x[8]),
    'student_klass': x[9], 
    'project_title': x[0], 
    'advisors': x[10],
    'affiliations': x[11],
    'project_status': x[1], 
    'project_type': x[2], 
    'semester_year': x[5], 
    'semester_semesterIndex': x[6], 
    'idStudentSemesterRel': x[7],
    'titleConfirm': x[12]
  }, results))


def listStudentsemesterrels():
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

def newStudentsemesterrel(model):
  shouldBeStaff(request, session)
  doLog("new DAO function. model: {}".format(model))
  instance = Studentsemesterrel(model)
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

def getStudentsemesterrel(id):
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

def updateStudentsemesterrel(id, model):
  shouldBeStaff(request, session)
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

def deleteStudentsemesterrel(id):
  shouldBeStaff(request, session)
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

def findStudentsemesterrel(model):
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
