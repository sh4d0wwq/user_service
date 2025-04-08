from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..services.auth_service import AuthService
from ..repositories.user_repository import UserRepository
from ..models.user import UserCreate, UserLogin
from ..services.jwt_service import JWTService
from ..dependencies import get_db

class AuthAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["Authentication"])
        self.router.add_api_route("/register", self.register_user, methods=["POST"])
        self.router.add_api_route("/login", self.login_user, methods=["POST"])
        self.router.add_api_route("/logout", self.logout, methods=["POST"])

    def get_auth_service(self, db: Session) -> AuthService:
        return AuthService(UserRepository(db))

    def register_user(self, user: UserCreate, db: Session = Depends(get_db)):
        auth_service = self.get_auth_service(db)
        return auth_service.register_user(user)

    def login_user(self, response: Response, user: UserLogin, db: Session = Depends(get_db)):
        auth_service = self.get_auth_service(db)
        user_db = auth_service.authenticate_user(user)
        if not user_db:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        access_token = JWTService.create_access_token({"sub": str(user_db.id)})
        refresh_token = JWTService.create_refresh_token({"sub": str(user_db.id)})

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True, 
            max_age=60 * 15  
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            max_age=60 * 60 * 24 * 15 
        )

        return {"message": "Login successful"}
    
    def logout(self, response: Response):
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return {"message": "Logged out successfully"}



auth_api = AuthAPI()
router = auth_api.router    