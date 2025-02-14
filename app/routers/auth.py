from fastapi import APIRouter,FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils,outh2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router=APIRouter(
    tags=['Authentication']
)

@router.post('/login',response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user= db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invlid Credentials")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invlid Credentials")
 
    access_token=outh2.create_access_token(data={"user_id":user.id})
 
 ## create a token
 ## return a token
    return{"access_token":access_token,"token_type":"bearer"}