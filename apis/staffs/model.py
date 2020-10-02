from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('staff', {
    'idStaff': Integer,
    'email': String,
    'fullname': String 
  },mask='*');
  return model