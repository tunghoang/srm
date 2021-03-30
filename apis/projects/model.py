from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('project', {
    'idProject': Integer,
    'title': Text,
    'idProjecttype': Integer,
    'idSemester': Integer,
    'status': String,
    'grade': Float,
    'titleConfirm': Integer,
    'description': Text 
  },mask='*');
  return model