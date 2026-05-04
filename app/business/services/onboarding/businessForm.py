from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
from ....db_models import Business
import re

class Reg_NameAndWeb(FlaskForm):
    name = StringField("Business name",validators=[DataRequired()])
    
    website = StringField("Website", validators=[Optional()],
                           render_kw={"placeholder": "www.yourwebsite.com"})
    
    
    submit = SubmitField("Continue")

    def validate_businessName(self, name):
        existing_name = Business.query.filter_by(
            name=name.data).first()
        if existing_name:
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
                                     ("finger-nail","Nails"),
                                     ("hair-salon","Hair salon"),
                                     ("spa","Medspa")
                                     ])
    
    submit = SubmitField("Continue")


class Reg_Location(FlaskForm):
    location = StringField("Where's your business located?",validators=[DataRequired()])
    
    submit = SubmitField("Continue")

    def validate_location(self, location):
        # TODO: Location validation somehow
        pass


