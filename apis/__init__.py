from flask_restplus import Api
api = Api(title="Student research management", version="1.0")

from .quotas import create_api as create_quotas
api.add_namespace(create_quotas())
from .guestadvisors import create_api as create_guestadvisors
api.add_namespace(create_guestadvisors())
from .advisors import create_api as create_advisors
api.add_namespace(create_advisors())
from .staffs import create_api as create_staffs
api.add_namespace(create_staffs())
from .students import create_api as create_students
api.add_namespace(create_students())
from .klass import create_api as create_klass
api.add_namespace(create_klass())
from .semesters import create_api as create_semesters
api.add_namespace(create_semesters())
from .projecttypes import create_api as create_projecttypes
api.add_namespace(create_projecttypes())
from .projects import create_api as create_projects
api.add_namespace(create_projects())
from .attachments import create_api as create_attachments
api.add_namespace(create_attachments())
from .projectStudentRels import create_api as create_projectStudentRels
api.add_namespace(create_projectStudentRels())
from .projectAdvisorRels import create_api as create_projectAdvisorRels
api.add_namespace(create_projectAdvisorRels())
from .studentSemesterRels import create_api as create_studentSemesterRels
api.add_namespace(create_studentSemesterRels())
from .projectReviewerRels import create_api as create_projectReviewerRels
api.add_namespace(create_projectReviewerRels())
from .stafflogin import create_api as create_stafflogin
api.add_namespace(create_stafflogin())
from .advisorlogin import create_api as create_advisorlogin
api.add_namespace(create_advisorlogin())
from .guestlogin import create_api as create_guestlogin
api.add_namespace(create_guestlogin())
from .studentlogin import create_api as create_studentlogin
api.add_namespace(create_studentlogin())
from .logout import create_api as create_logout
api.add_namespace(create_logout())
from .upload import uploadApi
api.add_namespace(uploadApi)
from .exports import exportAdvisorApi,exportStudentSemesterApi,recordCheckpointApi
api.add_namespace(exportAdvisorApi)
api.add_namespace(exportStudentSemesterApi)
api.add_namespace(recordCheckpointApi)
from .configs import create_api as create_configs
api.add_namespace(create_configs())
