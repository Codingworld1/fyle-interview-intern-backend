import json
from flask import request, jsonify
from core.libs import assertions
from functools import wraps
from core.models.teachers import Teacher
from core import db

class AuthPrincipal:
    def __init__(self, user_id, student_id=None, teacher_id=None, principal_id=None):
        self.user_id = user_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.principal_id = principal_id


def accept_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        incoming_payload = request.json
        return func(incoming_payload, *args, **kwargs)
    return wrapper


def authenticate_principal(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')
        assertions.assert_auth(p_str is not None, 'principal not found')
        p_dict = json.loads(p_str)
        p = AuthPrincipal(
            user_id=p_dict['user_id'],
            student_id=p_dict.get('student_id'),
            teacher_id=p_dict.get('teacher_id'),
            principal_id=p_dict.get('principal_id')
        )

        if request.path.startswith('/student'):
            assertions.assert_true(p.student_id is not None, 'requester should be a student')
        elif request.path.startswith('/teacher'):
            assertions.assert_true(p.teacher_id is not None, 'requester should be a teacher')
        elif request.path.startswith('/principal'):
            assertions.assert_true(p.principal_id is not None, 'requester should be a principal')
        else:
            assertions.assert_found(None, 'No such api')

        return func(p, *args, **kwargs)
    return wrapper
def authenticate_teacher(f):
    """Decorator to authenticate teachers"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        principal_header = request.headers.get("X-Principal")
        if not principal_header:
            return jsonify({"error": "Unauthorized", "message": "Missing authentication header"}), 401

        try:
            principal = json.loads(principal_header)  # Parse JSON
            teacher_id = principal.get("teacher_id")

            if not teacher_id:
                return jsonify({"error": "Unauthorized", "message": "Invalid credentials"}), 401

            teacher = db.session.get(Teacher, teacher_id)  # Corrected SQLAlchemy call

            if not teacher:
                return jsonify({"error": "Unauthorized", "message": "Teacher not found"}), 403

        except Exception as e:
            return jsonify({"error": "Invalid request", "message": str(e)}), 400

        return f(teacher, *args, **kwargs)

    return decorated_function