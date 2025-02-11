# from core import app
# from .responses import APIResponse
# app.response_class = APIResponse
from core.apis.assignments.teacher import teacher_assignments_resources

def register_blueprints(app):
    app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
