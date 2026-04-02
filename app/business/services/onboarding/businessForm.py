from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
from ....db_models import Business
import re

class Reg_Name(FlaskForm):
    business_name = StringField("Business name",validators=[DataRequired()])
    
    website = StringField("Website", validators=[Optional()],
                           render_kw={"placeholder": "www.yourwebsite.com"})
    
    
    submit = SubmitField("Continue")

    def validate_businessName(self, business_name):
        existing_business_name = Business.query.filter_by(
            business_name=business_name.data).first()
        if existing_business_name:
            print("Ez a név már foglalt!")
            raise ValidationError(f"Ez a név már foglalt!")

    def validate_website(self, website):
        pattern = re.compile(
            r'^(https?:\/\/)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(\/\S*)?$'
        )
        if website.data and not pattern.match(website.data):
            raise ValidationError("Érvénytelen link!")


class Reg_ServiceType(FlaskForm):
    categories = RadioField(validators=[DataRequired()],choices=[("barber-shop","Barber"),
                                     ("finger-with-nail","Nails"),
                                     ("hair-salon","Hair salon"),
                                     ("spa","Medspa")
                                     ])
    
    submit = SubmitField("Continue")


