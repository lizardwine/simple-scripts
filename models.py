from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, JSON, String, BOOLEAN, create_engine
from sqlalchemy.sql.expression import Select

FILE_PATH = "./test.sqlite3" # change this to database path
ENGINE_NAME = "sqlite" # change this to engine name


engine = create_engine(f"{ENGINE_NAME}:///{FILE_PATH}")
Base = declarative_base()

Session = sessionmaker(engine)
session = Session()

def create_session():
    return sessionmaker(engine)()

def drop_all():
    Base.metadata.drop_all(engine)

def create_all():
    Base.metadata.create_all(engine)

def reset():
    drop_all()
    create_all()

def add(_object, session=session):
    session.add(_object)

def commit(session=session):
    session.commit()

def save(_object,session=session):
    session.add(_object)
    session.commit()

def save_many(*objects, session = session):
    session.add_all(objects)
    session.commit()

def get_all(_object,session=session):
    return session.query(_object).all()

def filter(condition,*fields_or_class,session=session):
    return session.query(*fields_or_class).filter(condition)

def query(*fields_or_class,session=session):
    return session.query(*fields_or_class)




# Create your models here
# Example: 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), nullable=False, unique=True)
    cash = Column(Integer(), nullable=False)
    bank = Column(Integer(), nullable=False)
    inventory = Column(JSON())
    actions = Column(JSON())

    def __str__(self):
        return str(self.user_id)
