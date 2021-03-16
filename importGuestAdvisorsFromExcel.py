from apis.db_utils import DbInstance
from apis.app_utils import buildAdvisorRecordFromLDAPAttrs, doHash
from apis.advisors import Advisor

from pandas import read_excel, DataFrame
from apis.advisors.db import newAdvisor
from apis.guestadvisors.db import newGuestadvisor
import math
from datetime import datetime
def importGuestAdvisorsFromExcel(path):
  f1 = open('log1.txt', 'w+')
  f2 = open('log2.txt', 'w+')
  __db = DbInstance.getInstance()
  data = read_excel(path, sheet_name='Sheet2', skiprows=0)
  values = data._values
  for row in values:
    try:
      guestObj = {
        'email': row[2].strip(),
        'fullname': row[0].strip(),
        'affiliation': row[1].strip(),
        'password': 'abc123'
      }
      print('0000000000000000000\n')
      print(guestObj)
      guest = newGuestadvisor(guestObj)
    except Exception as e:
      f2.write(str(e))
      f2.write("\n")
      print(str(e))
      print(row)
      f2.write("\n")
      f2.write("\n")

  f1.close()
  f2.close()

importGuestAdvisorsFromExcel('guestAdvisor.xlsx')
