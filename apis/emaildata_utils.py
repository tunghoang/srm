import pandas, math, json
from .db_utils import *

def addToCommittees(committees, prj, key, row):
  if committees.get(key, None) is None:
    committees[key] = dict()
    committees[key]['email'] = f"{row[15]},{row[16]},{row[17]},{row[18]},{row[19]}"
    committees[key]['projects'] = list()
  obj = {'student': prj[0], 'MSSV':prj[1], 'title': prj[3], 'idAttachment': prj[4], 'filename': prj[5], 'advisor': row[6], 'reviewer': row[8] }
  #print(json.dumps(obj, ensure_ascii=False))
  committees[key]['projects'].append(obj)

def toArrayCommittee(committees):
  output = list()
  for key in committees.keys():
    output.append({'committee':key, 'email': committees[key]['email'], 'projects': committees[key]['projects']})
  return output

def processCommittee(path):
  __db = DbInstance.getInstance()
  data = pandas.read_excel(path, sheet_name="All", skiprows=0)
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

  for row in rows:
    advStr = str(row[6]).replace('\n', '/')
    project = __db.session().execute(sql1, {'idSsr': str(row[10]).strip()}).fetchall()
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
    addToCommittees(committees, prj, key, row)

  outFile = open('public/committee.json', 'w', encoding='utf-8')
  emailArray = toArrayCommittee(committees)
  outFile.write(json.dumps(emailArray, ensure_ascii=False))
  outFile.close();  
  logFile.close()
  
def addToEmails(emails, prj, key):
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

def processReviewer(path):
  __db = DbInstance.getInstance()
  data = pandas.read_excel(path, sheet_name="All", skiprows=0)
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

  emails = dict()

  for row in rows:
    advStr = str(row[6]).replace('\n', '/')
    project = __db.session().execute(sql1, {'idSsr': str(row[10]).strip()}).fetchall()
    if str(row[14]) != "nan" or str(row[15]) != "nan":
      print(f"{str(row[14])} - {str(row[15])}")
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
    addToEmails(emails, prj, key)
    key = str(row[12]).strip()
    if key == "nan":
      pass
    else:
      addToEmails(emails, prj, key)

  outFile = open('public/reviewer.json', 'w', encoding='utf-8')
  emailArray = toArray(emails)
  outFile.write(json.dumps(emailArray, ensure_ascii=False))
  outFile.close()
  logFile.close()

def processFee(path):
  shName = "All"
  print(shName)
  data = pandas.read_excel(path, sheet_name=shName, skiprows=0)
  rows = data._values
  logFile = open('email.error', 'w', encoding='utf-8')

  emails = []

  for row in rows:
    email = str(row[2])
    emails.append({
      'email': row[2],
      'hoidongEng': row[3] if not math.isnan(row[3]) else 0.0,
      'hoidongViet': row[4] if not math.isnan(row[4]) else 0.0,
      'huongdan': row[5] if not math.isnan(row[5]) else 0.0,
      'phanbien': row[6] if not math.isnan(row[6]) else 0.0,
      'tong': row[7] if not math.isnan(row[7]) else 0.0,
      'thue': row[8] if not math.isnan(row[8]) else 0.0,
      'thucnhan': row[9] if not math.isnan(row[9]) else 0.0,
      'category': row[10]
    })

  outFile = open('public/fee.json', 'w', encoding='utf-8')
  outFile.write(json.dumps(emails, ensure_ascii=False))
  outFile.close();  
  logFile.close()
  
def process(mode, path):
  if mode == 'committee':
    processCommittee(path)
  elif mode == 'reviewer':
    processReviewer(path)
  elif mode == 'fee':
    processFee(path)
  else:
    raise Exception('Wrong mode value')


