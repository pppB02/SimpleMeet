from app import db
from ....db_models import Business
from ....web_helper import save_photo
from flask import request


def save_about_business(business: Business, form, raw_tags):
    business.about_description = form.about_description.data
    print("raw_tags",raw_tags)
    print(type(raw_tags))
    print("gsjfhgsjh")
    saveD = raw_tags.split(',') if raw_tags else []
    
    print(saveD,"niggr")
    business.further_info = saveD

    if form.about_business_image.data:
        filename = save_photo(form.about_business_image.data, output_size=(580,520))
        if filename:
            business.about_business_image = filename

    if form.about_team_image.data:
        filename = save_photo(form.about_team_image.data, output_size=(580,520))
        if filename:
            business.about_team_image = filename

    db.session.commit()
    print("saved")
    return business


def load_about_business_to_form(business: Business, form):
    form.about_description.data = business.about_description or ""

    