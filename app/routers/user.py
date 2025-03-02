from .. import models,schemas,utils,outh2
from fastapi import Body, FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional,List

# ************ User Operations *******************

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

#Create User

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db: Session=Depends(get_db)):
    #hash the pass before storing - user.password
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get All Users

@router.get("/",response_model=List[schemas.UserOut])
def get_users(db: Session=Depends(get_db)):
    users= db.query(models.User).all()
    return users


# get one user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db: Session=Depends(get_db)):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} does not exist")
    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db),current_user: models.User = Depends(outh2.get_current_user)):
    # Fetch the user from the database
    
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Delete the user
    db.delete(user)
    db.commit()

    return {"detail": "User deleted successfully"}
