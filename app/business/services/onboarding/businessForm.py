from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError, Optional, URL
from ....db_models import Business

class BusinessRegistration(FlaskForm):
    business_name = StringField("Business name",validators=[DataRequired()])
    
    website = StringField("Website", validators=[Optional(),URL()],
                           render_kw={"placeholder": "www.yourwebsite.com"})
    
    categories = RadioField(choices=[("barber-shop","Barber"),
                                     ("finger-with-nail","Nails"),
                                     ("hair-salon","Hair salon"),
                                     ("spa","Medspa")
                                     ])
    
    submit = SubmitField("Continue")

    def validate_email(self, business_name):
        existing_business_name = Business.query.filter_by(
            business_name=business_name.data).first()
        if existing_business_name:
            raise ValidationError(f"Ez a név már foglalt!")

