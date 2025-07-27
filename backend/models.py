from flask_sqlalchemy import SQLAlchemy
from datetime import date, time

db = SQLAlchemy()
 # 1er etape On cree notre modele
class Tache(db.Model):
    id= db.Column(db.Integer,primary_key=True) # id
    tache = db.Column(db.String(250),nullable=False) # tache
    description = db.Column(db.String(1000),nullable=True) # description
    date = db.Column(db.Date, default=date.today) # date
    heure = db.Column(db.Time,nullable=True) # temps
    status = db.Column(db.Boolean, default=False)

