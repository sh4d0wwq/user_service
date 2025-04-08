from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email):
        return self.db.query(User).where(User.email == email).first()
    
    def get_user_by_username(self, username):
        return self.db.query(User).where(User.username == username).first()
    
    def get_user_by_id(self, id):
        return self.db.query(User).where(User.id == id).first()

    def create_user(self, username: str, email: str, hashed_password: str):
        new_user = User(username=username, email=email, hashed_password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def update_user(self, id, new_user):
        cur_user = self.get_user_by_id(id)
        cur_user.username = new_user.username
        self.db.commit()