from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField
from wtforms.validators import DataRequired
from ....db_models import UserAccount

class MemberProfile(FlaskForm):
    name = StringField("Name",validators=[
                                        DataRequired()])
    
    email = StringField("Email",validators=[
                                        DataRequired()])
    
    submit = SubmitField("Sing Up")

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

