from functools import wraps
from flask import redirect, url_for
from flask_login import current_user
import re

def role_required(role,return_page):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                if role == "business_admin":
                    return redirect(url_for("business.login"))
                else:
                    return redirect(url_for("user.login"))
            
            if current_user.role != role:
                return redirect(url_for(return_page))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def is_safe_input(text):
    # < > (XSS), ' " (SQLi), ; (SQL command chaining), -- (SQL comment)
    # \ (Escape character), / (Path traversal)
    dangerous_pattern = r"[<>'\"\;\\/\-\-]"

    if re.search(dangerous_pattern, text):
        return False
    
    return True