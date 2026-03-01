from flask import Flask, render_template, url_for, request, redirect
from app.init import create_app, db
import app.db_models as models
from datetime import datetime, time, timedelta

app = create_app()

@app.route("/", methods=['POST','GET'])
def index():

    tb_model = models.UserAccount.query.all()
    print(tb_model)

    return render_template("test.html", tb_model=tb_model)

if __name__ == "__main__":
    with app.app_context():

        # Ha tiszta adatbázist akarsz:
        db.drop_all()
        db.create_all()

        admin_user = models.UserAccount(
            email="admin@test.hu",
            name="Admin József",
            password_hash="hashed_pw",
            role="business_admin"
        )

        db.session.add(admin_user)
        db.session.commit()

    app.run(debug=True)


