from fastapi.testclient import TestClient
from app.main import app
import pytest
from app import schemas
from app.database import get_db,Base
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base



SQLALCHEMY_DATABASE_URL='postgresql://postgres:fastapi@localhost:5432/fastapi_test'
# SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False ,bind=engine)


        
# app.dependency_overrides[get_db]= override_get_db 
        
      
      
@pytest.fixture()      
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()  
def client(session):
    print("my lcient fixute ran")
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]= override_get_db 
    yield TestClient(app)
    #run our code after our test finishes




