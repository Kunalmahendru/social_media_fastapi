from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_password}'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False ,bind=engine)

Base=declarative_base()
# ceating dependency function created to create a session
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# while True:
#     try:
#         conn =psycopg2.connect(host='localhost',database='fastapi',user='postgres',
#                                password='fastapi',cursor_factory=RealDictCursor)

#         cursor=conn.cursor()
#         print("DataBase connection was successful!")
#         break
#     except Exception as error:
#         print("Connecting to Database Failed")
#         print("Error: ",error)
#         time.sleep(2)
        
# using raw sql to connect to datbase. but now we r using the sqlalchemy

