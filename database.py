import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine 
from sqlalchemy.orm import DeclarativeBase , sessionmaker

load_dotenv()
user = os.getenv("db_user")
pass_ = os.getenv("db_password")
host = os.getenv("db_host")
port = os.getenv("db_port")
database = os.getenv("db_name")

password = quote_plus(pass_)



db_url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(db_url,echo=True)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()