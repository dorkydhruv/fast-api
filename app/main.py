from typing import Optional
from fastapi import Body, FastAPI, Response,status,HTTPException
from pydantic import BaseModel
from random import randint
app=FastAPI()

class Post(BaseModel):
    title :str
    content : str
    published :bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Wassup:)"}

my_posts = [
    {"title": "Title 1" , "content": "Content 1","id": 1},
    {"title": "Title 2" , "content": "Content 2","id": 2},
    {"title": "Title 3" , "content": "Content 3","id": 3},
]

@app.get("/posts")
def read_posts():
    return my_posts

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randint(1,1000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id :int, response: Response):
    for post in my_posts:
        if post["id"] == id:
            return post
    raise HTTPException(status_code=404,detail="Post not found")

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    for post in my_posts:
        if post["id"] == id:
            my_posts.remove(post)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404,detail="Post not found")

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    for post in my_posts:
        if post["id"] == id:
            post["title"] = post.title
            post["content"] = post.content
            post["published"] = post.published
            post["rating"] = post.rating
            return post
    raise HTTPException(status_code=404,detail="Post not found")