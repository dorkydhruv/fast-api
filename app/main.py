from typing import Optional
import psycopg
from psycopg.rows import dict_row
from fastapi import Body, FastAPI, Response,status,HTTPException
from pydantic import BaseModel
from random import randint
import time
import models
from database import engine ,get_db

app=FastAPI()
models.Base.metadata.create_all(bind=engine)



class Post(BaseModel):
    title :str
    content : str
    published :bool = True
    rating: Optional[int] = None
while True:
    try:
        conn = psycopg.connect(host='localhost',dbname='fastapi',user='postgres',password='3000')
        cursor = conn.cursor(row_factory=dict_row)
        print("Connected to the database")
        break
    except Exception as error:
        print("Failed to connect to the database")
        print(error)
        time.sleep(5)

@app.get("/")
async def root():
    return {"message": "Wassup:)"}

@app.get("/posts")
def read_posts():
    cursor.execute("""
    SELECT * FROM posts
    """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
                   (post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}

@app.get("/posts/{id}")
def get_post(id :int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    this_post = cursor.fetchone()
    if this_post:
        return {"data":this_post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE from posts WHERE id = %s RETURNING *""",(str(id),))
    post = cursor.fetchone()
    if post:
        conn.commit()
        return {"data":post}
    raise HTTPException(status_code=404,detail=f"post with id {id} not found")

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content=%s, published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id),))
    post= cursor.fetchone()
    if post:
        conn.commit()
        return {"data":post}
    raise HTTPException(status_code=404,detail=f"post with id {id} not found")