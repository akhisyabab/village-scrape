from flask_jwt_extended import (
    get_jwt_identity,
    verify_jwt_in_request,
)
from functools import wraps
from project.models.models import User


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        username = get_jwt_identity()
        current_user = User.find_by_username(username)

        if current_user.role != 'admin':
            return {
                'message': 'Permission denied. Admin only'
            }, 403
        else:
            return fn(*args, **kwargs)
    return wrapper
