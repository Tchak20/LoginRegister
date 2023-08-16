"""
Ce module contient des fonctions pour établir une connexion à la base de données.
Il fournit une fonction pour créer une connexion à la base de données en utilisant
les paramètres de configuration spécifiés.
"""
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
DBCON = "mysql+mysqlconnector://root:@localhost/mydatabase"
engine = create_engine(DBCON)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
DATABASE_URL: Optional[str] = None
SECRET_KEY: Optional[str] = "cairocoders"
def sess_db():
    """
    Crée et retourne une connexion à la base de données.
    
    Cette fonction crée une connexion à la base de données en utilisant les
    paramètres de configuration spécifiés. Elle renvoie l'objet de connexion
    prêt à être utilisé pour exécuter des requêtes SQL.
    
    Returns:
        db_connection (database connection): L'objet de connexion à la base de données.
    """
    db_connection = SessionFactory()
    try:
        yield db_connection
    finally:
        db_connection.close()
