from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import psycopg2
import os 
#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
# SECRET_KEY = os.environ.get('SECRET_KEY')
# SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_URL = 'database.db'

engine = create_engine('DATABASE_URL', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
init_db()