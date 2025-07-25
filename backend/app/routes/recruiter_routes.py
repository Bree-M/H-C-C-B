from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.models import db, Invitation, Response, Result, Submission
from datetime import datetime

recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/recruiter')

@recruiter_bp.route('/invitations', methods=['POST'])
@jwt_required()
def send_invitation():
    data = request.get_json()
    invitation = Invitation(
        interviewee_id=data['interviewee_id'],
        assessment_id=data['assessment_id'],
        status='pending'
    )
    db.session.add(invitation)
    db.session.commit()
    return jsonify({'message': 'Invitation sent'}), 201

@recruiter_bp.route('/response', methods=['POST'])
@jwt_required()
def give_feedback():
    data = request.get_json()

    submission=Submission.query.get(data['submission_id'])
    if not submission:
        return jsonify({"error":"Submission not found!"}),404
    
    response = Response(
        question_id=data['question_id'],
        submission_id=submission.id,
        recruiter_id=get_jwt_identity()['id'],
        interviewee_id=submission.interviewee_id, 
        assessment_id=submission.assessment_id,
        feedback=data['feedback'],
        score=data['score'],
        submitted_at=datetime.utcnow(),
        status='pending'
    )
    db.session.add(response)
    db.session.commit()
    return jsonify({
    'message': 'Response submitted',
    'response': response.to_dict()
}), 201


@recruiter_bp.route('/results', methods=['PATCH'])
@jwt_required()
def release_results():
     data = request.get_json()
     result = Result.query.get(data['result_id'])
     if result:
         result.released = True
         db.session.commit()
         return jsonify({'message': 'Results released'}), 200
     return jsonify({'error': 'Result not found'}), 404
