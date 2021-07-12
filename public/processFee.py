import sys, pandas, math, json

shName = "All"
print(shName)
data = pandas.read_excel('fee.xlsx', sheet_name=shName, skiprows=0)
rows = data._values
logFile = open('email.error', 'w', encoding='utf-8')

emails = []

def addToEmails(row):
  global emails
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

for row in rows:
  email = str(row[2])
  addToEmails(row)

outFile = open('fee.json', 'w', encoding='utf-8')
outFile.write(json.dumps(emails, ensure_ascii=False))
outFile.close();  

logFile.close()
