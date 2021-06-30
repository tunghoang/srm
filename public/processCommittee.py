import pandas, math, json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+pymysql://root:!qaz@wsx@127.0.0.1/srm', echo=False)
SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()

data = pandas.read_excel('committee.xlsx', sheet_name="All", skiprows=0)
rows = data._values
logFile = open('email.error', 'w', encoding='utf-8')
sql1 = '''
select 
	stu.fullname, stu.studentNumber, psRel.idProject, prj.title, att.idAttachment, att.title
FROM student stu 
	LEFT JOIN studentSemesterRel ssRel
	ON stu.idStudent = ssRel.idStudent
	LEFT JOIN projectStudentRel psRel
	ON stu.idStudent = psRel.idStudent
	LEFT JOIN project prj
	ON psRel.idProject = prj.idProject
	RIGHT JOIN attachment att
	ON prj.idProject = att.idProject
WHERE ssRel.idStudentsemesterrel = :idSsr
'''

committees = dict()

def addToCommittees(prj, key, row):
  global committees
  if committees.get(key, None) is None:
    committees[key] = dict()
    committees[key]['email'] = f"{row[15]},{row[16]},{row[17]},{row[18]},{row[19]}"
    committees[key]['projects'] = list()
  obj = {'student': prj[0], 'MSSV':prj[1], 'title': prj[3], 'idAttachment': prj[4], 'filename': prj[5], 'advisor': row[6], 'reviewer': row[8] }
  #print(json.dumps(obj, ensure_ascii=False))
  committees[key]['projects'].append(obj)

def toArray(committees):
  output = list()
  for key in committees.keys():
    output.append({'committee':key, 'email': committees[key]['email'], 'projects': committees[key]['projects']})
  return output

for row in rows:
  advStr = str(row[6]).replace('\n', '/')
  project = session.execute(sql1, {'idSsr': str(row[10]).strip()}).fetchall()
  #print(f"{str(row[14])} - {str(row[15])}")
  if str(row[14]) != "nan":
    print(f"{str(row[0])} - {str(row[14])} - {str(row[15])}")
    logFile.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{advStr}\tError: Khong bao ve\n")
    continue
  elif len(project) == 0:
    logFile.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{advStr}\tError: Not upload thesis\n")
    continue
  elif len(project) > 1:
    logFile.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{advStr}\tError: Dupplication\n")
    continue
  prj = project[0]
  key = str(row[13]).strip()
  if key == "nan":
    logFile.write(str(row[0]).strip() + " - committee name\n")
    continue
  addToCommittees(prj, key, row)

outFile = open('data.json', 'w', encoding='utf-8')
emailArray = toArray(committees)
outFile.write(json.dumps(emailArray, ensure_ascii=False))
outFile.close();  

logFile.close()
