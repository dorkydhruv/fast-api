from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
SQL_ALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker( autoflush= False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#For connecting to sql raw
# while True:
#     try:
#         conn = psycopg.connect(host='localhost',dbname='fastapi',user='postgres',password='3000')
#         cursor = conn.cursor(row_factory=dict_row)
#         print("Connected to the database")
#         break
#     except Exception as error:
#         print("Failed to connect to the database")
#         print(error)
#         time.sleep(5)