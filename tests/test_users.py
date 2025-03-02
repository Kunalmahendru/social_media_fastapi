from app import schemas
import pytest
from app.config import settings
from jose import jwt





# def test_root(client):
#     res=client.get("/")
#     print(res.json())
#     assert res.json().get('message')=='Hy! Welcome to the api testing !!'
    
    
    
def test_create_user(client):
    res=client.post("/users/",json={'email':"hello123@gmail.com",'password':"password123"})
    new_user=schemas.UserOut(**res.json())
    assert new_user.email=="hello123@gmail.com"
    
    
    
def test_login_user(client,test_user):
        res=client.post("/login",data={'username':test_user['email'],'password':test_user['password']})
        login_res=schemas.Token(**res.json())
        payload=jwt.decode(login_res.access_token,settings.secret_key,settings.algorithm)
        id=payload.get('user_id')
        assert res.status_code==200
        assert login_res.token_type=='bearer'
        assert id==test_user['id']



@pytest.mark.parametrize("email,password,status_code",[
    ('wrongemail@gmail.com','wrongpass',403),
    ('hello123@gmail.com','wrongpass',403),
    ('wrongemail@gmail.com','password123',403),
    (None,'password123',403),
    ('hello123@gmail.com',None,403),
])
def test_login_incorrect(email,password,status_code,client,test_user):
    res=client.post("/login",data={'username':email,'password':password})
    assert res.status_code==status_code
    # assert res.json().get('detail')=="Invlid Credentials"
