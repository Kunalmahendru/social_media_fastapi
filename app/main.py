from fastapi import Body, FastAPI
from app import models
from .database import  engine
from .routers import post,user,auth,votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
# pip install uvicorn
# uvicorn app.main:app --reload
# inside app directory look for file name main and in main file look for the app instance of fastapi

# this tells the sqlalchemy to create tables . but now that will handle by alembic 
 # models.Base.metadata.create_all(bind=engine)

origin=["*"]


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# my_posts=[{"title":"Title of post 1","content":"Content of post 1","id":1},
#           {"title":"Favourite Food","content":"I like rice","id":2}]



# def find_post(id):
#     for p in my_posts:
#         if p['id']==id:
#             return p

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id']==id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
async def root():
    return{"message":"Welcome to my APi !!"}




