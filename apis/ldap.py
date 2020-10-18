import ldap
_ldapConnection = None
MAX_RETRIES = 3
_ldapConnectionRetries = MAX_RETRIES
_conn_str = 'ldap://112.137.142.11:389'
_admin = 'cn=admin,dc=vnu,dc=vn'
_cred = 'abc123'

ldapScope = ldap.SCOPE_SUBTREE
def _getLDAPConnection():
  global _ldapConnectionRetries
  global _ldapConnection
  global _conn_str
  global _admin
  global _cred

  if not _ldapConnection:
    l = ldap.initialize(_conn_str)
    l.set_option(ldap.OPT_TIMEOUT, 7)
    l.bind(_admin, _cred)
    _ldapConnection = l
    _ldapConnectionRetries = MAX_RETRIES

  return _ldapConnection

def search(base, uid):
  print(base, uid)
  global _ldapConnectionRetries
  global _ldapConnection
  conn = None
  try:
    conn = _getLDAPConnection()
  except Exception as e:
    _ldapConnectionRetries -= 1
    if _ldapConnectionRetries == 0:
      raise Exception("Cannot connecto to LDAP server: " + e)
    else:
      _ldapConnection = None
      search(base,uid)
  try:
    result = conn.search_s(base, ldap.SCOPE_SUBTREE, f'uid={uid}')
  except Exception as e:
    print(e)
    _ldapConnection = None
    return search(base, uid)
  return result

def authenticate(dn, cred):
  conn = None
  try:
    conn = _getLDAPConnection()
  except Exception as e:
    raise Exception("Cannot connecto to LDAP server: " + e)
  try:
    conn.bind(dn, cred)
    return True
  except ldap.INVALID_CREDENTIALS as e:
    return False
