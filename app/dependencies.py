from fastapi import Request, HTTPException, Depends
from app.repositories.user_repository import UserRepository
from app.db.database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = int(getattr(request.state, "user_id", None))
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user