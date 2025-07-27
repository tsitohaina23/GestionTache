# etape 4
from app import app, db

with app.app_context():
    db.create_all()
    print("Base de donnée initiliser")

