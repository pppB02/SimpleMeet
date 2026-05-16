from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, FileField, IntegerField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired,NumberRange, InputRequired
from ....db_models import UserAccount
from app import photos

class MemberProfile(FlaskForm):
    name = StringField("Name",validators=[
                                        DataRequired()])
    
    email = StringField("Email",validators=[
                                        DataRequired()])
    
    photo = FileField("Kép", validators=[
        FileAllowed(photos, "Csak képek!"),
        FileRequired("File kell")
    ])
    
    submit = SubmitField("Send link")

    # def validate_email(self, email):
    #     # existing_user_email = UserAccount.query.filter_by(
    #     #     email=email.data).first()
    #     # if existing_user_email:
    #     #     raise ValidationError(f"Ezt az email címet már regisztrálták!")
    #     pass


class ConfirmInviteForm(FlaskForm):
    
    agreeTerms = BooleanField("agreeTerms",default=False,validators=[
                                        DataRequired()])

    submit = SubmitField("Sing Up")


class openHours(FlaskForm):
    
    # Monday
    monOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23, message='0-23 hours'), InputRequired()])
    monOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59, message='0-59 mins'), InputRequired()])
    monClosed = BooleanField("Closed", default=False)

    # Tuesday
    tueOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23, message='0-23 hours'), InputRequired()])
    tueOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59, message='0-59 mins'), InputRequired()])
    tueClosed = BooleanField("Closed", default=False)

    # Wednesday
    wedOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23, message='0-23 hours'), InputRequired()])
    wedOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59, message='0-59 mins'), InputRequired()])
    wedClosed = BooleanField("Closed", default=False)

    # Thursday
    thuOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23, message='0-23 hours'), InputRequired()])
    thuOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59, message='0-59 mins'), InputRequired()])
    thuClosed = BooleanField("Closed", default=False)

    # Friday
    friOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23, message='0-23 hours'), InputRequired()])
    friOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59, message='0-59 mins'), InputRequired()])
    friClosed = BooleanField("Closed", default=False)

    # Saturday
    satOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23, message='0-23 hours'), InputRequired()])
    satOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59, message='0-59 mins'), InputRequired()])
    satClosed = BooleanField("Closed", default=False)

    # Sunday
    sunOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23, message='0-23 hours'), InputRequired()])
    sunOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59, message='0-59 mins'), InputRequired()])
    sunClosed = BooleanField("Closed", default=False)

    submit = SubmitField("Sing Up")

