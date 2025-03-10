from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional


        
        
class UserCreate(BaseModel):
    email:EmailStr
    password:str
    
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        from_attributes=True
        ## because we were returning sqlemy object not pydantic so this will tell just ignore the face that it is not pydantic and go on convert it to dict
        
        
        
class UserLogin(BaseModel):
    email:EmailStr
    password:str


class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True
   

class PostCreate(PostBase):
    pass


# us sending data to user

class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserOut
    
    class Config:
        from_attributes=True
        ## because we were returning sqlemy object not pydantic so this will tell just ignore the face that it is not pydantic and go on convert it to dict

class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
        from_attributes=True
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:Optional[str]=None
    
    
class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
    
    