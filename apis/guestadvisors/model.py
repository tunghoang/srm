from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('guestadvisor', {
    'idGuestadvisor': Integer,
    'email': String,
    'fullname': String,
    'affiliation': String,
    'password': String 
  },mask='*');
  return model