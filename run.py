from apis.ldap import doList,search
from apis.db_utils import DbInstance
from apis.app_utils import buildAdvisorRecordFromLDAPAttrs
from apis.advisors import Advisor


def importAdvisorsFromLDAP():
  print("Hello world")
  __db = DbInstance.getInstance()
  #result = search('ou=dhcn,ou=canbo,dc=vnu,dc=vn', 'tunghx')
  results = doList('ou=khoa,ou=dhcn,ou=canbo,dc=vnu,dc=vn')
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
import math
def seedProjectsFromExcel(path, year, semesterIndex):
  data = read_excel(path, sheet_name='Data', skiprows=1)
  values = data._values
  for row in values:
    try:
      rowObj = { 
        'studentNumber' : int(row[1]),
        'fullname': row[2].strip(),
        'email': f'{int(row[1])}@vnu.edu.vn',
        'dob': row[3],
        'title': row[5],
        'idAdvisor': int(row[9]) if not math.isnan(row[9]) else None,
        'idAdvisor1': int(row[10]) if not math.isnan(row[10]) else None
      }
    except:
      print(row)
    print(rowObj)


#importAdvisorsFromLDAP()
seedProjectsFromExcel('fit2016.xlsx', 2021, 0)
