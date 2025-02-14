from .. import models,schemas,outh2
from fastapi import Body, FastAPI,Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional,List


router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session=Depends(get_db),limit:int=10,skip:int=0,search:Optional[str]=""):
    
    
    posts = (
        db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id,isouter=True)
        .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip)
        .all()
    )
   
    return posts

# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts=cursor.fetchall()
    
#     return{"data":posts}





@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session=Depends(get_db),curr_user:int=Depends(outh2.get_current_user)):
    print(curr_user.email)
    new_post=models.Post(**post.model_dump())
    new_post.owner_id=curr_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_posts(post:Post):
    
#     # my_dict = post.model_dump()
#     # my_dict['id']=randrange(0,1000000)
#     # my_posts.append(my_dict)
#      cursor.execute(
#         """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
#         (post.title, post.content, post.published) )
#      new_post=cursor.fetchone()
#      conn.commit()
#      return{"data":new_post}
# # title string, content string , category 



@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,response:Response,db: Session=Depends(get_db),curr_user:int=Depends(outh2.get_current_user)):
    # cursor.execute(""" SELECT * from posts WHERE id=%s""",(str(id) ))
    # test_post=cursor.fetchone()
    # post=find_post(id)
    #posts= db.query(models.Post).filter(models.Post.id==id).first()
    post=(db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id,isouter=True)
        .group_by(models.Post.id).filter(models.Post.id==id).first())
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
       # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'Message':f"post with id:{id} was not found"}
       # Since `post` is a tuple (Post, votes), extract the actual Post object
    post_obj, vote_cnt = post

    # Check if the post belongs to the current user
    if post_obj.owner_id != curr_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"This post doesn't belong to you, it belongs to owner id: {post_obj.owner_id}",
        )

    # Return response in the expected format
    return post
    
    
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db: Session=Depends(get_db),curr_user:int=Depends(outh2.get_current_user)):
    # cursor.execute(""" DELETE from posts WHERE id=%s RETURNING *""",(str(id) ))
    # test_post=cursor.fetchone()
    # conn.commit() 
    
    # index=find_index_post(id)  
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
        
    if post.owner_id!=curr_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"This post doesnt belongs to you , it belongs to onwer id :{post.owner_id}")
    # my_posts.pop(index)
   
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post_data:schemas.PostBase,db: Session=Depends(get_db),curr_user:int=Depends(outh2.get_current_user)):
    # cursor.execute(""" Update posts SET title=%s,content=%s,published=%s  where id=%s RETURNING *""",(post.title,post.content,post.published , str(id)))
    # test_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    
    #index=find_index_post(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found")
    if post.owner_id!=curr_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"This post doesnt belongs to you , it belongs to onwer id :{post.owner_id}")
   
    post_query.update(post_data.model_dump(),synchronize_session=False)
    db.commit()
    return post
