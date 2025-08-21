from functools import wraps
from flask import request, jsonify

def require_role(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            role = request.headers.get('AuthRole')
            if role not in allowed_roles:
                return jsonify({'error': 'Forbidden: Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
