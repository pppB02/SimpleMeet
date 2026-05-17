from flask import Blueprint, render_template, url_for, send_from_directory, current_app
from ..db_models import Business, Staff, UserAccount

index = Blueprint("index", __name__, static_folder="static", template_folder="templates",static_url_path="/index/static")


@index.route("/get_file/<filename>")
def get_file(filename):
    return send_from_directory(current_app.config["UPLOADED_PHOTOS_DEST"],filename)

@index.route("/")
def home():
    return render_template("index.html")

@index.route("/adatvedelem")
def adatvedelem():
    return render_template("adatvedelem.html")

@index.route("/a/<slug>")
def business_site(slug):
    def get_public_id():
        for i in range(-1,-len(slug),-1):
            if slug[i] == "-":
                return slug[len(slug)+i+1:len(slug):1]
            
    public_id = get_public_id()
    print(public_id)

    business = Business.query.filter_by(public_id=public_id).first_or_404()
    staffs = Staff.query.filter_by(business_id=business.id).all()
    staffsDatas = []
    print(staffs)
    for staff in staffs:
        staffUser = UserAccount.query.filter_by(id=staff.user_id).first()
        staffsDatas.append({"name":staffUser.username,"pfp_name":staff.pfp_name})
        print(staff.id)
        print(staff.pfp_name)
    
    print(staffsDatas)

    return render_template("temp_for_services/szolgaltatas_minta.html", business=business, staffs=staffsDatas)