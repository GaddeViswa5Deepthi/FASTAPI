
from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import engine, get_db
from .. import models,schema,oauth2
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/posts",
    tags=['POSTS']
   
)
# @app.get('/')
# def root():
#     return{'message':"welcome to api"}

# @app.get('/sqlalchemy')
# def test_posts(db:Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return{ "data":posts}
# my_posts= [{"title":"title of the post 1","content":"content of post1","id":1},{"title":"favouritefood",'content':"I like pizza",'id':2}]
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#          if p['id'] == id:
#             return i


@router.get("/",response_model=list[schema.Postout])
async def get_posts(
    db: Session = Depends(get_db), 
    current_user: int = Depends(oauth2.get_current_user)
):
    # Query posts along with vote count
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)  # Outer join to include posts with zero votes
        .group_by(models.Post.id)
        .all()
    )

    # Convert to JSON-serializable format
    posts_with_votes = [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at,
            "owner_id": post.owner_id,
            **{"votes": votes_count}  
        }
        for post, votes_count in results
    ]

    return jsonable_encoder(posts_with_votes)  # Ensure serialization

# @router.get('/',response_model=list[schema.Postout])

# async def get_post(db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
   
#       results= db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id ==models.Post.id).group_by(models.Post.id).all()
    
    
#       return results
# @router.get('/')
# #@router.get('/',response_model=schema.Posts)
# async def get_post(db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
#    # cursor.execute(""" SELECT * FROM posts""")
#     #posts = cursor.fetchall()
# # limit:int=10,skip:int=2,search:Optional[str]=""
#     # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#     results= db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id ==models.Post.id).group_by(models.Post.id).all()
#     # results= db.query(models.Post).join(models.Vote,models.Vote.post_id ==models.Post.id).all()    
    
#     return results    

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.PostCreate)
def create_post(post:schema.PostCreate, db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute(""" INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """,        (post.title,post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #new_post = models.Post(title=post.title,content=post.content,published=post.published)
    #print(current_user.id)
    #print(current_user.email)
    new_post = models.Post(owner_id=current_user.id,title=post.title,content=post.content,published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
   
    return new_post

#@app.get("/posts/latest")
#def get_latest_post():
 #   post = my_posts[len(my_posts)-1]
  #  return post
@router.get("/{id}",response_model=schema.Posts)
def get_post(id: str, db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts WHERE id= %s """, (str(id)),)
    #post = cursor.fetchall()
    post=db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    

    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #deleting post
    #find the index in the array
    #cursor.execute(""" DELETE FROM posts WHERE id =%s RETURNING *""",(str(id),))
    #delete_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post =post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} doesnt exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform request action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schema.Posts)

def update_post(id : int, post:schema.PostCreate,db:Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute(""" UPDATE posts SET title=%s,content=%s,published=%s  WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)),)
    #update_post=cursor.fetchone()
    #conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)
    current_post=post_query.first()

    
    if current_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} doesnt exist")
    if current_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform request action")
    post_query.update({
        "title":post.title,
        "content":post.content
    },synchronize_session=False)    
    db.commit()
    return post_query.first()