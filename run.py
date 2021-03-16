from apis.ldap import doList,search
from apis.db_utils import DbInstance
from apis.app_utils import buildAdvisorRecordFromLDAPAttrs
from apis.advisors import Advisor


def importAdvisorsFromLDAP():
  print("Hello world")
  __db = DbInstance.getInstance()
  result = search('ou=dhcn,ou=canbo,dc=vnu,dc=vn', 'tunghx')
  #results = doList('ou=bgh,ou=dhcn,ou=canbo,dc=vnu,dc=vn')
  #results = doList('ou=phongthinghiem,ou=dhcn,ou=canbo,dc=vnu,dc=vn')
  results = doList("ou=cntt,ou=khoa,ou=dhcn,ou=canbo,dc=vnu,dc=vn")
  #results = doList('ou=trungtam,ou=dhcn,ou=canbo,dc=vnu,dc=vn')
  #results = doList('ou=phongban,ou=dhcn,ou=canbo,dc=vnu,dc=vn')
  print(len(results))
  print("==================")
  for r in results:
    dn,attrs = r
    advisor = buildAdvisorRecordFromLDAPAttrs(attrs)
    print(advisor['email'])
    instance = __db.session().query(Advisor).filter(Advisor.email == advisor['email']).first()
    if instance is None:
      print("Insert ", advisor['email'])
      instance = Advisor(advisor)
      __db.session().add(instance)
  __db.session().commit()

from pandas import read_excel, DataFrame
from apis.students.db import newStudent,findStudent
from apis.projects import Project
from apis.semesters.db import findSemester
from apis.projectStudentRels.db import newProjectstudentrel
from apis.projectAdvisorRels.db import newProjectadvisorrel
from apis.studentSemesterRels.db import newStudentsemesterrel
import math
from datetime import datetime
def seedProjectsFromExcel(path, year, semesterIndex):
  __db = DbInstance.getInstance()
  f1 = open('log1.txt', 'w+')
  f2 = open('log2.txt', 'w+')
  semesters = findSemester({'year': year, 'semesterIndex': semesterIndex})
  if len(semesters) == 0: 
    return;
  idSemester = semesters[0].idSemester
  print(idSemester)

  data = read_excel(path, sheet_name='Data', skiprows=0)
  values = data._values
  print(len(values));
  for row in values:
    try:
      studentObj = {
        'studentNumber' : int(row[1]),
        'fullname': row[2].strip(),
        'email': f'{int(row[1])}@vnu.edu.vn',
        'dob': datetime.strptime(row[3].strip(), "%m/%d/%Y").date(),
        'klass': row[4]
      }
      idStudent = None
      results = findStudent({'studentNumber': int(row[1])})

      if len(results) == 0:
        student = newStudent(studentObj)
        idStudent = student.idStudent
      else:
        idStudent = results[0].idStudent
      projectObj = {
        'title': row[5],
        'idProjecttype': 1,
        'idSemester': idSemester,
        'status': 'on-going'
      }
      project = Project(projectObj)
      __db.session().add(project)
      __db.session().commit()
      #project = newProject(projectObj)
      f1.write(str(project.idProject) + " - " + str(idStudent) + "\n")
      idProject = project.idProject

      projectStudentRelObj = {
        'idStudent': idStudent,
        'idProject': idProject,
        'status': 1
      }
      newProjectstudentrel(projectStudentRelObj)

      idAdvisor = int(row[9]) if not math.isnan(row[9]) else None
      idAdvisor1 = int(row[10]) if not math.isnan(row[10]) else None
      if idAdvisor is not None:
        newProjectadvisorrel({'idAdvisor':idAdvisor, 'idProject': idProject, 'status': 1})
      if idAdvisor1 is not None:
        newProjectadvisorrel({'idAdvisor':idAdvisor1, 'idProject': idProject, 'status': 1})
      
      newStudentsemesterrel({
        'idStudent': idStudent,
        'idSemester': idSemester
      })

      #rowObj = { 
      #  'studentNumber' : int(row[1]),
      #  'fullname': row[2].strip(),
      #  'email': f'{int(row[1])}@vnu.edu.vn',
      #  'dob': row[3],
      #  'klass': row[4],
      #  'title': row[5],
      #  'idAdvisor': int(row[9]) if not math.isnan(row[9]) else None,
      #  'idAdvisor1': int(row[10]) if not math.isnan(row[10]) else None
      #}
    except Exception as e:
      f2.write(str(e) + "\n")
      f2.write(str(row))
      f2.write("\n")
    #print(rowObj)
  f1.close()
  f2.close()

#importAdvisorsFromLDAP()
#seedProjectsFromExcel('fit2016.xlsx', 2020, 1)
seedProjectsFromExcel('fit2021.xlsx', 2020, 1)
