from app import create_app, db
from app.db_models import Business
app = create_app()

if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        # db.create_all()
        businesses = Business.query.all()

        for business in businesses:
            print(business.public_id)
            
    app.run(debug=True, host="0.0.0.0")