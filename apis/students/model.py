from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('student', {
    'idStudent': Integer,
    'studentNumber': Integer,
    'email': String,
    'fullname': String,
    'dob': Date,
    'gender': Boolean,
    'klass': String,
    'idKlass': Integer,
    'mobile': String,
    'notified': Boolean 
  },mask='*');
  return model