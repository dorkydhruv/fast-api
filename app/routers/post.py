from typing import Optional,List
from fastapi import Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models,schemas
from .. import oauth
router= APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/",response_model=list[schemas.PostOut])
def read_posts(db: Session=Depends(get_db),limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute("""
    # SELECT * FROM posts
    # """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts = list ( map (lambda x : x._mapping, posts) )
    post_data=[]
    for row in posts:
        post={
            "Post":row[0],
            "votes":row[1]
        }
        post_data.append(post)
    return post_data

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session=Depends(get_db),current_user :int=Depends(oauth.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post =models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id :int,db: Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # this_post = cursor.fetchone()
    this_post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if this_post:
        return{
            "Post":this_post[0],
            "votes":this_post[1]
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user :int=Depends(oauth.get_current_user)):
    # cursor.execute("""DELETE from posts WHERE id = %s RETURNING *""",(str(id),))
    # post = cursor.fetchone()
    post =db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=404,detail=f"post with id {id} not found")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="You are not allowed to delete this post")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db),current_user :int=Depends(oauth.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content=%s, published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id),))
    # post= cursor.fetchone()
    post_query=db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=404,detail=f"post with id {id} not found")
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=403,detail="You are not allowed to update this post")
    # conn.commit()
    post_query.update(post.dict())
    db.commit()
    return post_query.first()
