from passlib.context import CryptContext

from ..models.user import UserCreate
from ..repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def register_user(self, user: UserCreate):
        hashed_password = self.hash_password(user.password)
        return self.user_repo.create_user(user.username, user.email, hashed_password)

    def authenticate_user(self, user):
        userDB = self.user_repo.get_user_by_email(user.email)
        if not userDB or not self.verify_password(user.password, userDB.hashed_password):
            return None
        return userDB
    

