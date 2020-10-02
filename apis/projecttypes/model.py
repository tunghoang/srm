from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('projecttype', {
    'idProjecttype': Integer,
    'name': String,
    'description': String 
  },mask='*');
  return model