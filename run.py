from apis.ldap import doList,search
from apis.db_utils import DbInstance
from apis.app_utils import buildAdvisorRecordFromLDAPAttrs
from apis.advisors import Advisor
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
