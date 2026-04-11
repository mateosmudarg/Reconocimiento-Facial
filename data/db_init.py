from . import db

def init_db():
    db.init_engine()
    db.Base.metadata.create_all(bind=db.engine)