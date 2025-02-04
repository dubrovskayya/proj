from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
connection_string = os.getenv('CONNECTION_STRING')

# create db connection and session
engine = create_engine(connection_string, echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()


# function to export the session
def get_session():
    return db_session
