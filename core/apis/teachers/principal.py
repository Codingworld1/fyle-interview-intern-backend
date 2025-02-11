from flask import Blueprint, jsonify
from core.models import Teacher
from core.libs import auth_principal  # Ensure the auth system is in place

principal_bp = Blueprint('principal_bp', __name__)

@principal_bp.route('/principal/teachers', methods=['GET'])
@auth_principal
def get_all_teachers():
    """Get a list of all teachers."""
    teachers = Teacher.query.all()
    teacher_list = [{'id': teacher.id, 'user_id': teacher.user_id} for teacher in teachers]
    return jsonify({'data': teacher_list}), 200
