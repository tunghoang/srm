from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('semester', {
    'idSemester': Integer,
    'year': Integer,
    'semesterIndex': Integer,
    'active': Boolean 
  },mask='*');
  return model