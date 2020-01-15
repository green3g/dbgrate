from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Migration(Base):
    __tablename__ = 'migrations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
