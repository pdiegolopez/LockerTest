from app.db.models import Base
from sqlalchemy import create_engine

engine = create_engine("sqlite:///db.db", echo=True)

Base.metadata.create_all(engine)
