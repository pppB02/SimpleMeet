from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError, Optional, URL
from ....db_models import Business

class NameAndWebsite(FlaskForm):
    business_name = StringField("Business name",validators=[DataRequired()])
    
    website = StringField("Website", validators=[Optional(),URL()],
                           render_kw={"placeholder": "www.yourwebsite.com"})
    
    #categories = 
    
    submit = SubmitField("Continue")

    def validate_email(self, business_name):
        existing_business_name = Business.query.filter_by(
            business_name=business_name.data).first()
        if existing_business_name:
            raise ValidationError(f"Ez a név már foglalt!")

