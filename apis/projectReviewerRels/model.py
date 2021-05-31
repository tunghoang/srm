from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('projectReviewerrRel', {
    'idProjectreviewerrel': Integer,
    'idReviewer': Integer,
    'idProject': Integer,
    'status': Integer 
  },mask='*');
  return model