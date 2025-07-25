from backend.app.models import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Submission(db.Model):
    __tablename__='submissions'

    id=db.Column(db.Integer,primary_key=True)
    interviewee_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    assessment_id=db.Column(db.Integer,db.ForeignKey('assessments.id'),nullable=False)
    submitted=db.Column(db.Boolean,default=False)
    score=db.Column(db.Integer)
    status=db.Column(db.String(50),default='pending')
    start_time=db.Column(db.DateTime)
    end_time=db.Column(db.DateTime)
    time_taken=db.Column(db.Integer)

    interviewee=db.relationship('User',backref='submissions')
    assessment=db.relationship('Assessment',backref='submissions')

    serialize_rules=('-interviewee.submissions','-assessment.submissions')








