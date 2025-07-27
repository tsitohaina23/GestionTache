# etape 3: creation du app
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Tache
from config import get_database_uri

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= get_database_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def accueil():
    return "Bienvenu dans le API de creation de tache"

@app.route("/taches", methods=["POST"])
def ajoutTache():
    donne = request.json
    date_obj = datetime.strptime(donne["date"],"%Y-%m-%d").date()
    heure_obj = datetime.strptime(donne["heure"],"%H:%M:%S").time()
    newtache = Tache(tache= donne["tache"],description= donne["description"],date = date_obj,heure = heure_obj,status = donne["status"])
    db.session.add(newtache)
    db.session.commit()
    return jsonify({
        "id": newtache.id,
        "tache": newtache.tache,
        "description": newtache.description,
        "date":newtache.date,#.isoformat()
        "heure": newtache.heure.strftime("%H:%M:%S"),
        "status": newtache.status

    }),201

@app.route("/taches",methods=["GET"])
def affichageTache():
    newtache = Tache.query.all()
    return jsonify([{
        "id": t.id,
        "tache": t.tache,
        "description": t.description,
        "date": t.date.isoformat(),
        "heure": t.heure.strftime("%H:%M:%S"),
        "status": t.status
    } for t in newtache]), 201

@app.route("/taches/<int:tache_id>", methods=["PUT"])
def modifier(tache_id):
    taches= Tache.query.get(tache_id)
    if not taches:
        return jsonify({"error":"Tache introuvable"})
    donne = request.json
    taches.tache = donne.get("tache",taches.tache)
    taches.description = donne.get("description",taches.description)
    date_str = donne.get("date")
    heure_str = donne.get("heure")
    if date_str:
        taches.date = datetime.strptime(date_str,"%Y-%m-%d").date()
    if heure_str:
        taches.heure = datetime.strptime(heure_str,"%H:%M:%S").time()
    taches.status = donne.get("status",taches.status)
    db.session.commit()
    return jsonify({"message":"Tâche mise à jours"})

@app.route("/taches/<int:tache_id>",methods=["DELETE"])
def suppression(tache_id):
    taches = Tache.query.get(tache_id)
    if not taches:
        return jsonify({"error":"Tache introuvable"})
    db.session.delete(taches)
    db.session.commit()
    return jsonify({
        "message":"Tache supprimée"
    })


if __name__ == "__main__":
    app.run(debug=True,port=2000)