from typing import List
from app import schemas
import pytest
def test_get_all_posts(authorized_client,test_posts):
    res=authorized_client.get("/posts/")
    print(res.json())  
    def validate(post):
        return schemas.PostOut(**post)
    posts_map=map(validate,res.json())
    posts_list=list(posts_map)
    print(list(posts_map))
    
    assert len(res.json())==len(test_posts)
    assert res.status_code==200
    
def test_unathorized_user_get_all_posts(client,test_posts):
    res=client.get('/posts/')
    print(res)
    assert res.status_code==401
    
def test_unathorized_user_get_one_posts(client,test_posts):
    res=client.get(f'/posts/{test_posts[0].id}')
    print(res)
    assert res.status_code==401
    
def test_get_one_post_not_Exist(authorized_client,test_posts):
        res=authorized_client.get(f'/posts/{8888}')
        print(res)
        assert res.status_code==404

def test_one_post(authorized_client,test_posts):
        res=authorized_client.get(f'/posts/{test_posts[0].id}')
        print(res.json())
        post=schemas.PostOut(**res.json())
        print(post)
        assert post.Post.id==test_posts[0].id
        assert post.Post.content==test_posts[0].content
        assert res.status_code==200


@pytest.mark.parametrize("title,content,published",[
    ("Awsm new title","Awsm new content",True),
    ("Gym","Squats",True),
    ("Browni","dessert",False),
])
def test_create_post(authorized_client,test_user,test_posts,title,content,published):
    res=authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})
    print(res.json())
    created_post=schemas.Post(**res.json())
    
    assert res.status_code==201
    assert created_post.title==title
    assert created_post.content==content
    assert created_post.published==published
    assert created_post.owner_id==test_user['id']
    
def test_create_post_default_published_true(authorized_client,test_user,test_posts):
    res=authorized_client.post("/posts/",json={"title":"hell","content":"contenta"})
    print(res.json())
    created_post=schemas.Post(**res.json())
    
    assert res.status_code==201
    assert created_post.title=="hell"
    assert created_post.content=="contenta"
    assert created_post.published==True
    assert created_post.owner_id==test_user['id']
    
    
def test_unathorized_user_create_one_posts(client,test_posts):
    res=client.post("/posts/",json={"title":"hell","content":"contenta"})
    print(res)
    assert res.status_code==401
    
def test_unauthorized_user_delete_Post(client,test_user,test_posts):
    res=client.delete(f"/posts/{test_posts[0].id}")
    print(res)
    assert res.status_code==401
    
def test_authorized_user_delete_Post(authorized_client,test_user,test_posts):
    print(len(test_posts))
    res=authorized_client.delete(f"/posts/{test_posts[0].id}")
    print(len(test_posts))
    print(res)
    assert res.status_code==204
    
def test_Delete_post_nonexist(authorized_client,test_user,test_posts):
    
    res=authorized_client.delete(f"/posts/{8888}")
    
    assert res.status_code==404
    
def test_delete_other_user_postdef(authorized_client,test_user,test_posts):
    res=authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code==401
    
    
def test_update_pest(authorized_client,test_user,test_posts):
    # print(test_posts[0])
    res=authorized_client.put(f"/posts/{test_posts[0].id}",json={"title":"hello","content":"content"})
    updated_post=schemas.PostBase(**res.json())
    assert updated_post.title=='hello'
    assert updated_post.content=='content'
    assert res.status_code==200
    
    
def test_update_other_user_post(authorized_client,test_user,test_user2,test_posts):
    data={
        "title":"update title",
        "content":"update content"
    }
    # print(test_posts[0])
    res=authorized_client.put(f"/posts/{test_posts[3].id}",json=data)
    assert res.status_code==401
    
def test_unathourzied_update_other_user_post(client,test_user,test_user2,test_posts):
    data={
        "title":"update title",
        "content":"update content"
    }
    # print(test_posts[0])
    res=client.put(f"/posts/{test_posts[3].id}",json=data)
    assert res.status_code==401
    
def update_post_not_Exist(client,test_user,test_user2,test_posts):
    data={
        "title":"update title",
        "content":"update content"
    }
    # print(test_posts[0])
    res=client.put(f"/posts/{22}",json=data)
    assert res.status_code==404