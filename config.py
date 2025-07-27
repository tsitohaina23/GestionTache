# etape 2 : configuration pour la connexion automatique au base de donne 
import os
def get_database_uri():
    db_url = os.getenv("DATABASE_URL","sqlite:///local.db")
    if db_url.startswith("postgress://"):
        db_url = db_url.replace("postgress://","postgresssql://",1)
    return db_url
    
