from .. import models,schemas,outh2
from fastapi import Body, FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional,List
from .. import schemas,database,models,outh2

router=APIRouter(
    prefix="/votes",
    tags=['Votes']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(outh2.get_current_user)):
    vote_query=db.query(models.Votes).filter(models.Votes.post_id==vote.post_id, models.Votes.user_id==current_user.id)
    post_query=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if post_query is None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {vote.post_id} doesnt exist")
    if(post_query.owner_id==current_user.id):
        raise  HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"post {vote.post_id} is yours")
    print(post_query.owner_id,current_user.id)
    found_vote=vote_query.first()   
    if(vote.dir==1):
         if found_vote:
             raise  HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.email} already liked the post {vote.post_id}")
         new_vote=models.Votes(post_id=vote.post_id,user_id=current_user.id)
         db.add(new_vote)
         db.commit()
         return{"message":"successfully added vote "}
    else:
        if not found_vote:
            raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user {current_user.email} vote doesnt exist on {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successsfully deleted vote"}
    

        
     