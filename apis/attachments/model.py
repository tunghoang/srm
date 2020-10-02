from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('attachment', {
    'idAttachment': Integer,
    'title': String,
    'uuid': String,
    'idProject': Integer,
    'idOwner': Integer,
    'uploadDate': DateTime 
  },mask='*');
  return model