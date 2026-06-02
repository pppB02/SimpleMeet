import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, ValidationError, Optional

from ....db_models import Business


class Reg_NameAndWeb(FlaskForm):
    name = StringField("Vállalkozás neve", validators=[DataRequired()])

    website = StringField(
        "Weboldal",
        validators=[Optional()],
        render_kw={"placeholder": "www.yourwebsite.com"},
    )

    submit = SubmitField("Tovább")

    def validate_name(self, name):
        existing_name = Business.query.filter_by(name=name.data).first()
        if existing_name:
            raise ValidationError("Ez a név már foglalt!")

    def validate_website(self, website):
        pattern = re.compile(r"^(https?:\/\/)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(\/\S*)?$")
        if website.data and not pattern.match(website.data):
            raise ValidationError("Érvénytelen link!")


class Reg_ServiceType(FlaskForm):
    categories = RadioField(
        validators=[DataRequired()],
        choices=[
            ("barber-shop", "Barber"),
            ("finger-nail", "Körmös"),
            ("hair-salon", "Fodrász"),
            ("spa", "Wellness"),
        ],
    )

    submit = SubmitField("Tovább")


class Reg_Location(FlaskForm):
    location = StringField("Hol található a vállalkozása?", validators=[DataRequired()])
    submit = SubmitField("Tovább")

    def validate_location(self, location):
        pass