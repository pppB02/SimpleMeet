import re

from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    BooleanField,
    StringField,
    FileField,
    IntegerField,
    SelectField,
    DecimalField,
    RadioField,
    TextAreaField,
)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import (
    DataRequired,
    NumberRange,
    InputRequired,
    Length,
    Optional,
    ValidationError,
)
from ....db_models import UserAccount
from app import photos
from flask_login import current_user

lapos_choices = []

for ossz_perc in range(5, 721, 5):
    ora = ossz_perc // 60
    perc = ossz_perc % 60

    if ora == 0:
        megjelenes = f"{perc} perc"
    elif perc == 0:
        megjelenes = f"{ora} óra"
    else:
        megjelenes = f"{ora} óra {perc} perc"

    lapos_choices.append((str(ossz_perc), megjelenes))


class MemberProfile(FlaskForm):
    name = StringField("Név", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    photo = FileField(
        "Kép",
        validators=[
            FileAllowed(photos, "Csak képek!"),
            FileRequired("File kell"),
        ],
    )
    submit = SubmitField("Meghívó küldése")

    def validate_email(self, email):
        if email.data.strip() == current_user.email:
            raise ValidationError("Saját email címedre nem küldhetsz meghívót!")


class ConfirmInviteForm(FlaskForm):
    agreeTerms = BooleanField("agreeTerms", default=False, validators=[DataRequired()])
    submit = SubmitField("Csatlakozás")


class openHours(FlaskForm):
    # Monday
    monOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    monOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    monCloseHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    monCloseMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    monClosed = BooleanField("Closed", default=False)

    # Tuesday
    tueOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    tueOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    tueCloseHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    tueCloseMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    tueClosed = BooleanField("Closed", default=False)

    # Wednesday
    wedOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    wedOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    wedCloseHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    wedCloseMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    wedClosed = BooleanField("Closed", default=False)

    # Thursday
    thuOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    thuOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    thuCloseHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    thuCloseMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    thuClosed = BooleanField("Closed", default=False)

    # Friday
    friOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    friOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    friCloseHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    friCloseMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    friClosed = BooleanField("Closed", default=False)

    # Saturday
    satOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    satOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    satCloseHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    satCloseMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    satClosed = BooleanField("Closed", default=False)

    # Sunday
    sunOpenHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    sunOpenMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    sunCloseHour = IntegerField("Hour", default=0, validators=[NumberRange(min=0, max=23), InputRequired()])
    sunCloseMin = IntegerField("Min", default=0, validators=[NumberRange(min=0, max=59), InputRequired()])
    sunClosed = BooleanField("Closed", default=False)

    submit = SubmitField("Mentés")


class NewServiceForm(FlaskForm):
    def __init__(self, teamMembersData, *args, **kwargs):
        super(NewServiceForm, self).__init__(*args, **kwargs)

        if teamMembersData:
            self.teamMembers.choices = [
                (
                    str(member.id),
                    str(UserAccount.query.filter_by(id=member.user_id).first().username),
                )
                for member in teamMembersData
            ]
        else:
            self.teamMembers.render_kw = {"disabled": "disabled", "style": "pointer-events: none;", "tabindex": "-1"}
            self.teamMembers.choices = [("0", "Nem található munkatárs!")]

    name = StringField("Szolgáltatás neve", validators=[DataRequired()])

    serviceType = SelectField(
        "Szolgáltatás típusa:",
        validators=[DataRequired()],
        choices={
            "Barber": [
                ("beard-trimming", "Szakál Vágás"),
                ("mens-haircut", "Férfi hajvágás"),
                ("mens-shaving", "Férfi borotválkozás"),
            ],
            "Spa": [
                ("relaxation-massages", "Relaxációs masszázsok"),
                ("body-treatments-and-rituals", "Testkezelések és rituálék"),
                ("premium-skincare", "Prémium arcápolás"),
            ],
            "Kézápolás": [
                ("aesthetic-and-classic-manicure", "Esztétikai és klasszikus manikűr"),
                ("nail-application", "Tartós lakkozás és műkörömépítés"),
                ("SPA-Hand-Treatment", "SPA kézápolás"),
            ],
            "Hajszalon": [
                ("haircuts-and-styling", "Hajvágás és styling"),
                ("hair-coloring", "hajfestés és színváltoztatás"),
                ("corrective-treatments", "hajszerkezet-javító kezelések"),
            ],
        }
    )

    description = TextAreaField(
        "Leírása",
        validators=[
            DataRequired(message="Kérjük, írj egy rövid leírást!"),
            Length(min=10, max=1000, message="A leírásnak 10 és 1000 karakter között kell lennie."),
        ],
    )

    duration = SelectField("Időtartam", validators=[DataRequired()], choices=lapos_choices)
    priceType = SelectField("Ár típusa", validators=[DataRequired()], choices=[("Fixed", "Fix ár")])
    price = IntegerField(
        "Ár",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=500000, message="Az árnak %(min)s és %(max)s Ft között kell lennie!"),
        ],
    )

    teamMembers = RadioField()
    submit = SubmitField("Mentés")

class BusinessEditForm(FlaskForm):
    name = StringField("Vállalkozás neve", validators=[DataRequired(), Length(min=2, max=255)])
    location = StringField("Hely", validators=[Optional(), Length(max=255)])
    website = StringField("Weboldal", validators=[Optional()], render_kw={"placeholder": "www.yourwebsite.com"})
    submit = SubmitField("Mentés")

    def validate_name(self, name):
        existing = UserAccount.query.filter_by(username=name.data).first()
        # ez csak példa volt; ezt business szinten fogjuk használni a route-ban is
        return True

    def validate_website(self, website):
        pattern = re.compile(r'^(https?:\/\/)?(www\.)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(\/\S*)?$')
        if website.data and not pattern.match(website.data):
            raise ValidationError("Érvénytelen link!")


class AboutBusinessForm(FlaskForm):
    about_description = TextAreaField(
        "Rólunk",
        validators=[
            DataRequired(message="Kérlek írj egy bemutatkozást az üzletről."),
            Length(min=20, max=2000, message="A leírás 20 és 2000 karakter között legyen.")
        ]
    )

    about_business_image = FileField(
        "Üzletről kép",
        validators=[FileAllowed(photos, "Csak képek tölthetők fel!")]
    )

    about_team_image = FileField(
        "Csapatkép",
        validators=[FileAllowed(photos, "Csak képek tölthetők fel!")]
    )

    further_info = SelectField(
        "További információk:",
        validators=[Optional()],
        choices={
            "Foglalás": [
                ("instant-confirmation", "Azonnali megerősítés"),
                ("online-booking", "Online foglalás")
            ],
            "Kényelem és Elérhetőség": [
                ("wheelchair-accessible", "Akadálymentesített"),
                ("kid-friendly", "Gyerekbarát"),
                ("pet-friendly", "Állatbarát"),
                ("free-wifi", "Ingyenes Wi-Fi"),
                ("air-conditioned", "Légkondicionált helyiség"),
                ("bike-parking", "Kerékpártároló"),
                ("on-site-parking", "Parkolás a helyszínen"),
                ("easy-public-transport", "Tömegközlekedéssel könnyen megközelíthető"),
                ("ev-charging", "Elektromos autó töltési lehetőség")
            ],
            "Fizetés és Árazás": [
                ("credit-card", "Bankkártyás fizetés"),
                ("szep-card", "SZÉP kártya elfogadóhely"),
                ("cashless-only", "Készpénzmentes hely"),
                ("free-consultation", "Ingyenes konzultáció")
            ],
            "Szolgáltatás jellege": [
                ("open-on-weekends", "Hétvégén is nyitva"),
                ("on-site-services", "Kiszállással is vállal munkát"),
                ("own-webshop", "Saját webshop")
            ],
            "Nyelvtudás": [
                ("english-speaking", "Angolul beszélő személyzet"),
                ("german-speaking", "Németül beszélő személyzet")
            ],
            "Értékek": [
                ("eco-friendly", "Környezetbarát"),
                ("lgbtq-friendly", "LMBTQ+ barát hely")
            ]
        }
    )

    submit = SubmitField("Mentés")


class UserProfileForm(FlaskForm):
    username = StringField("Felhasználónév", validators=[DataRequired(), Length(min=2, max=255)])
    email = StringField("Email", validators=[DataRequired(), Length(min=5, max=255)])
    photo = FileField("Profilkép", validators=[FileAllowed(photos, "Csak képek tölthetők fel!")])
    submit = SubmitField("Mentés")

    def validate_email(self, email):
        existing = UserAccount.query.filter(UserAccount.email == email.data, UserAccount.id != current_user.id).first()
        if existing:
            raise ValidationError("Ez az email cím már foglalt!")