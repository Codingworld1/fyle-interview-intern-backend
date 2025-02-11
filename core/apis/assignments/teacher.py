from flask import Blueprint, request, jsonify
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core import db
from .schema import AssignmentSchema


teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.authenticate_principal
def grade_assignment(p):
    """Grades an assignment"""

    # Parse request data
    data = request.get_json()
    assignment_id = data.get("id")
    grade = data.get("grade")

    if not assignment_id or not grade:
        return APIResponse.respond(error="Missing assignment ID or grade", status=400)

    # Fetch the assignment
    assignment = Assignment.query.filter_by(id=assignment_id, teacher_id=p.teacher_id).first()

    if not assignment:
        return APIResponse.respond(error="Assignment not found or unauthorized", status=404)

    if assignment.state == "GRADED":
        return APIResponse.respond(error="Assignment is already graded", status=400)

    # Update and save assignment
    assignment.grade = grade
    assignment.state = "GRADED"
    db.session.commit()

    # Serialize response
    assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=assignment_dump, status=200)
