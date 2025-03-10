# A conftest.py file is used in pytest (Python's testing framework) to define fixtures, hooks, and shared configurations that can be used across multiple test files. 

# any fixutre define here is avail to all the code in package
from app import models
from fastapi.testclient import TestClient
from app.main import app
import pytest
from app import schemas
from app.database import get_db,Base
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.outh2 import create_access_token


SQLALCHEMY_DATABASE_URL='postgresql://postgres:fastapi@localhost:5432/fastapi_test'
# SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False ,bind=engine)


        
# app.dependency_overrides[get_db]= override_get_db 
        
      
      
@pytest.fixture()      
def session():
    # print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()  
def client(session):
    # print("my lcient fixute ran")
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]= override_get_db 
    yield TestClient(app)
    #run our code after our test finishes


@pytest.fixture
def test_user(client):
    user_data={'email':"hello123@gmail.com"
               ,'password':"password123"}
    res=client.post("/users/",json=user_data)
    assert res.status_code==201
    # print(res.json())
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data={'email':"hello1234@gmail.com"
               ,'password':"password123"}
    res=client.post("/users/",json=user_data)
    assert res.status_code==201
    # print(res.json())
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id':test_user['id']})

@pytest.fixture
def authorized_client(client , token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,session,test_user2):
    posts_data=[{
        "title":"1st title",
        "content":"1st content",
        "owner_id":test_user['id']
    },{
        "title":"2nd title",
        "content":"2nd content",
        "owner_id":test_user['id']
    },{
        "title":"3rd title",
        "content":"3rd content",
        "owner_id":test_user['id']
    },{
        "title":"zero title",
        "content":"zero content",
        "owner_id":test_user2['id']
    }]
    
    def create_post_model(post):
       return models.Post(**post)
    
    post_map=map(create_post_model,posts_data)
    posts=list(post_map)
    session.add_all(posts)
    # session.add_all([models.Post(title="1st title",content="First content",owner_id=test_user['id']),
    #                  models.Post(title="2nd title",content="second content",owner_id=test_user['id']).
    #                  models.Post(title="3rd title",content="third title",owner_id=test_user['id'])])
        
    session.commit()
    posts=session.query(models.Post).all()
    return posts