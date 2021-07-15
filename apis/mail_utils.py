from .db_utils import DbInstance
from .advisors.db import getAdvisor
from datetime import datetime
import requests

__BASE_URL = 'https://fit.uet.vnu.edu.vn/static'
def __sendmail(receipient, subject, content):
  print(f"send to {str(receipient)} - {subject} - {content}")
  url = 'http://fit.uet.vnu.edu.vn:8001/mails/'
  response = requests.post(url, json = {
    'application': 'srm',
    'receipient': receipient,
    'subject': subject,
    'content': content,
    'sent': False,
    'queueTime': str(datetime.now())
  } )
  print((response.status_code, response.reason))

def sendmail(r,s,c):
  __sendmail(r,s,c)

def __getProject(idProject):
  __db = DbInstance.getInstance()
  sql = """
    SELECT idProject, title FROM project where idProject = :idProject
  """
  params = {'idProject': idProject}
  results = __db.session().execute(sql, params).fetchall()
  __db.session().commit()
  return (list(map(lambda x: {'idProject': x[0], 'title':x[1]}, results)))[0]


def notifyAdvisorNewProject(idAdvisor, idProject, status):
  print(f'notifyAdvisorNewProject {idAdvisor} - {idProject} - {status}')
  advisor = getAdvisor(idAdvisor)
  project = __getProject(idProject)
  receipient = advisor['email']
  subject = '[SRM] Thầy/cô được yêu cầu hướng dẫn một đề tài'
  content = f"""
    <p>Thầy/cô được yêu cầu hướng dẫn đề tài <span style='color:#0f0'>{project['title']}</span>.</p>
    <p>Click vào link dưới để xem chi tiết (thầy/cô có thể phải thực hiện đăng nhập bằng tài khoản của mình).<br/>
      <a href='{__BASE_URL}/advisor.html#/newproject/idProject/{idProject}/idAdvisor/{idAdvisor}'>{__BASE_URL}/newproject/idProject/{idProject}/idAdvisor/{idAdvisor}</a>
    </p>
    <p>Xin thầy cô lưu ý thực hiện xác nhận hướng dẫn và xác nhận tên đề tài (ngay trên trang web ứng dụng) nếu thầy/cô đồng ý hướng dẫn
    </p>
    <p>Trân trọng</p>
    <p>Văn phòng khoa CNTT, ĐHCN, ĐHQGHN</p>
  """
  __sendmail(receipient, subject, content)

def __getMemberEmails(idProject):
  try:
    __db = DbInstance.getInstance()
    sql = '''
      SELECT stu.email, stu.idStudent
      FROM student stu LEFT JOIN projectStudentRel psr ON stu.idStudent = psr.idStudent
      WHERE psr.idProject = :idProject
    '''
    params = {"idProject": idProject}
    results = __db.session().execute(sql, params).fetchall()
    __db.session().commit()
    return list(map(lambda x: x[0], results))
  except Exception as e:
    print(e)

def __getAdvisors(idProject):
  try:
    __db = DbInstance.getInstance()
    sql = '''
      SELECT adv.email, adv.fullname
      FROM advisor adv LEFT JOIN projectAdvisorRel par ON adv.idAdvisor = par.idAdvisor
      WHERE par.idProject = :idProject
    '''
    params = {"idProject": idProject}
    results = __db.session().execute(sql, params).fetchall()
    __db.session().commit()
    return list(map(lambda x: x[0], results))
  except Exception as e:
    print(e)

def notifyStudentAdvisorReject(idAdvisor, idProject):
  print(f'notifyAdvisorRemoveProject {idAdvisor} {idProject}')
  advisor = getAdvisor(idAdvisor)
  project = __getProject(idProject)
  receipient = ",".join(__getMemberEmails(idProject))
  subject = f'[SRM] Thầy/cô {advisor["fullname"]} đã TỪ CHỐI hướng dẫn'
  content = f"""
    <p>Thầy/cô {advisor['fullname']} đã ĐỒNG Ý hướng dẫn đề tài <span style='color:#0f0'>{project['title']}</span>.</p>
    <p>Click vào link dưới để xem chi tiết (em có thể phải thực hiện đăng nhập bằng tài khoản của mình).<br/>
      <a href='{__BASE_URL}/student.html'>{__BASE_URL}/student.html</a>
    </p>
    <p>Trân trọng</p>
    <p>Văn phòng khoa CNTT, ĐHCN, ĐHQGHN</p>
  """
  __sendmail(receipient, subject, content)

def notifyStudentAdvisorAccept(idAdvisor, idProject):
  print(f'notifyAdvisorAcceptProject {idAdvisor} {idProject}')
  advisor = getAdvisor(idAdvisor)
  project = __getProject(idProject)
  receipient = ",".join(__getMemberEmails(idProject))
  subject = f'[SRM] Thầy/cô {advisor["fullname"]} đã ĐỒNG Ý hướng dẫn'
  content = f"""
    <p>Thầy/cô {advisor['fullname']} đã ĐỒNG Ý hướng dẫn đề tài <span style='color:#0f0'>{project['title']}</span>.</p>
    <p>Click vào link dưới để xem chi tiết (em có thể phải thực hiện đăng nhập bằng tài khoản của mình).<br/>
      <a href='{__BASE_URL}/student.html'>{__BASE_URL}/student.html</a>
    </p>
    <p>Trân trọng</p>
    <p>Văn phòng khoa CNTT, ĐHCN, ĐHQGHN</p>
  """
  __sendmail(receipient, subject, content)
def notifyAdvisorStudentUpload(idProject):
  print(f'notifyAdvisorStudentUpload {idProject}')
  advisors = __getAdvisors(idProject)
  project = __getProject(idProject)
  receipient = ",".join(advisors)
  subject = f'[SRM] Yêu cầu Thầy/Cô kiểm tra và phê duyệt tài liệu tải lên'
  content = f"""
    <p>Dự án <span style='color:#0f0'>{project['title']}</span> Thầy/cô đang hướng dẫn có một tài liệu mới được tải lên. Thầy/Cô cần kiểm tra và phê duyệt (approve) tài liệu này trên ứng dụng quản lý tại <a href='{__BASE_URL}/advisor.html'>{__BASE_URL}/advisor.html</a></p>
    <p>Trân trọng</p>
    <p>Văn phòng khoa CNTT, ĐHCN, ĐHQGHN</p>
  """
  __sendmail(receipient, subject, content)

def notifyStudentsAdvisorApproved(idProject, idAdvisor):
  advisor = getAdvisor(idAdvisor)
  project = __getProject(idProject)
  receipient = ",".join(__getMemberEmails(idProject))
  subject = f'[SRM] Thầy/cô {advisor["fullname"]} đã phê duyệt tài liệu'
  content = f"""
    <p>Thầy/cô {advisor['fullname']} đã phê duyệt tài liệu tải lên của dự án <span style='color:#0f0'>{project['title']}</span>.</p>
    <p>Click vào link dưới để xem chi tiết (em có thể phải thực hiện đăng nhập bằng tài khoản của mình).<br/>
      <a href='{__BASE_URL}/student.html'>{__BASE_URL}/student.html</a>
    </p>
    <p>Trân trọng</p>
    <p>Văn phòng khoa CNTT, ĐHCN, ĐHQGHN</p>
  """
  __sendmail(receipient, subject, content)

def notify4IncompleteProfile(student):
  receipient = student['email']
  subject = f'[SRM] Yêu cầu sinh viên hoàn thiện thông tin cá nhân'
  content = f"""
    <p>Thân gửi em,</p>
    <p>
      Hiện nay trên hệ thống <a href='https://fit.uet.vnu.edu.vn/static/student.html'>SRM</a>, thông tin cá nhân của em chưa được cập nhật đầy đủ, đề nghị em khẩn trương cập nhật:
      <ul>
        <li>Họ và tên</li>
        <li>Lớp</li>
        <li>Mobile</li>
      </ul>
    </p>
    <p>
      Chúc các em học tập tốt
    </p>
  """
  __sendmail(receipient, subject, content)

