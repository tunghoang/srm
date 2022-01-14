import pandas, math, json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+pymysql://root:!qaz@wsx@127.0.0.1/srm', echo=False)
SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()

data = pandas.read_excel('reviewer.xlsx', sheet_name="All", skiprows=0)
rows = data._values
logFile = open('email.error', 'w', encoding='utf-8')
sql1 = '''
select 
	stu.fullname, stu.studentNumber, psRel.idProject, prj.title, att.idAttachment, att.title
FROM student stu 
	LEFT JOIN projectStudentRel psRel
	ON stu.idStudent = psRel.idStudent
	LEFT JOIN project prj
	ON psRel.idProject = prj.idProject
	RIGHT JOIN attachment att
	ON prj.idProject = att.idProject
WHERE prj.idProject = :idPrj
'''

emails = dict()

def addToEmails(prj, key):
  global emails
  if emails.get(key, None) is None:
    emails[key] = list()
  obj = {'student': prj[0], 'MSSV':prj[1], 'title': prj[3], 'idAttachment': prj[4], 'filename': prj[5]}
  #print(json.dumps(obj, ensure_ascii=False))
  emails[key].append(obj)

def toArray(emails):
  output = list()
  for email in emails.keys():
    output.append({'email': email, 'projects': emails[email]})
  return output

for row in rows:
  advStr = str(row[6]).replace('\n', '/')
  project = session.execute(sql1, {'idPrj': str(row[10]).strip()}).fetchall()
  #print(f"{str(row[14])} - {str(row[15])}")
  if str(row[14]) != "nan":
    print(f"{str(row[14])}")
    logFile.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{advStr}\tError: Khong bao ve\n")
    continue
  elif len(project) == 0:
    logFile.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{advStr}\tError: Not upload thesis\n")
    continue
  elif len(project) > 1:
    logFile.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{advStr}\tError: Dupplication\n")
    continue
  prj = project[0]
  key = str(row[11]).strip()
  if key == "nan":
    logFile.write(str(row[0]).strip() + " - reviewer1-Email\n")
    continue
  addToEmails(prj, key)
  key = str(row[12]).strip()
  if key == "nan":
    pass
  else:
    addToEmails(prj, key)

outFile = open('reviewer.json', 'w', encoding='utf-8')
emailArray = toArray(emails)
outFile.write(json.dumps(emailArray, ensure_ascii=False))
outFile.close();  

logFile.close()
