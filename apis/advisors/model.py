from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('advisor', {
    'idAdvisor': Integer,
    'email': String,
    'fullname': String,
    'idQuota': Integer,
    'idGuestadvisor': Integer 
  },mask='*');
  return model