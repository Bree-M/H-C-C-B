from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.app.models import db, Assessment

assessment_bp = Blueprint('assessments', __name__, url_prefix='/assessments')

@assessment_bp.route('/', methods=['POST'])
@jwt_required()
def create_assessment():
    data = request.get_json()
    user = get_jwt_identity()
    assessment = Assessment(
        title=data['title'],
        description=data['description'],
        time_limit=data['time_limit'],
        recruiter_id=user['id']
    )
    db.session.add(assessment)
    db.session.commit()
    return jsonify({'message': 'Assessment created'}), 201

@assessment_bp.route('/', methods=['GET'])
@jwt_required()
def get_assessments():
    assessments = Assessment.query.all()
    return jsonify([{
        "id": a.id,
        "title": a.title,
        "description": a.description,
        "time_limit": a.time_limit,
        "recruiter_id": a.recruiter_id,
        "difficulty": a.difficulty,
        "category": a.category,
        "is_published": a.is_published,
        "created_at": a.created_at,
        "updated_at": a.updated_at
    }  for a in assessments]), 200
