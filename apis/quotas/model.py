from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('quota', {
    'idQuota': Integer,
    'name': String,
    'description': String,
    'n_kltn': Integer,
    'n_dakh': Integer 
  },mask='*');
  return model