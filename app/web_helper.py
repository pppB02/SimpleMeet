from functools import wraps
from flask import redirect, url_for, current_app
from flask_login import current_user
import os, secrets
from PIL import Image


def role_required(role, return_page):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                if role == "business_admin":
                    return redirect(url_for("business.login"))
                return redirect(url_for("user.login"))

            if current_user.role != role:
                return redirect(url_for(return_page))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def business_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("business.login"))

            if current_user.role != "business_admin":
                return redirect(url_for("index.home"))

            if not current_user.has_business:
                return redirect(url_for("business.businessName"))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def staff_profile_required(return_page="user.dashboard"):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("user.login"))

            if not getattr(current_user, "staff_profile", None):
                return redirect(url_for(return_page))

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def save_photo(photo,output_size=(256, 265)):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if photo and allowed_file(photo.filename):
        ext = photo.filename.rsplit('.', 1)[1].lower()
        random_hex = secrets.token_hex(8)
        secure_name = f"{random_hex}.{ext}"

        filepath = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], secure_name)

        i = Image.open(photo)
        i.thumbnail(output_size)

        os.makedirs(current_app.config['UPLOADED_PHOTOS_DEST'], exist_ok=True)
        i.save(filepath, optimize=True, quality=85)

        return secure_name

    return None


def time_format(osszes_perc):
    ora = osszes_perc // 60
    perc = osszes_perc % 60

    if ora > 0 and perc > 0:
        return f"{ora} óra {perc} perc"
    elif ora > 0:
        return f"{ora} óra"
    else:
        return f"{perc} perc"