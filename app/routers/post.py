from fastapi import Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas

router= APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/",response_model=list[schemas.Post])
def read_posts(db: Session=Depends(get_db)):
    # cursor.execute("""
    # SELECT * FROM posts
    # """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session=Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post =models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.Post)
def get_post(id :int, response: Response,db: Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # this_post = cursor.fetchone()
    this_post = db.query(models.Post).filter(models.Post.id == id).first()
    if this_post:
        return this_post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""DELETE from posts WHERE id = %s RETURNING *""",(str(id),))
    # post = cursor.fetchone()
    post =db.query(models.Post).filter(models.Post.id == id)
    if post.first():
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404,detail=f"post with id {id} not found")

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content=%s, published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id),))
    # post= cursor.fetchone()
    post_query=db.query(models.Post).filter(models.Post.id == id)
    if post_query.first():
        # conn.commit()
        post_query.update(post.dict())
        db.commit()
        return post_query.first()
    raise HTTPException(status_code=404,detail=f"post with id {id} not found")
