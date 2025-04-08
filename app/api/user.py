from fastapi import APIRouter, Depends
from ..models.user import UserEdit, User
from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..services.user_service import UserService
from ..dependencies import get_db, get_current_user

class UserAPI:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["Users"])
        self.router.add_api_route("/{user_id}/", self.get_user, methods=["GET"])
        self.router.add_api_route("/me/edit/", self.edit_user, methods=["POST"])

    def get_user_service(self, db: Session) -> UserService:
        return UserService(UserRepository(db))

    def get_user(self, user_id: int, db: Session = Depends(get_db)):
        user_service = self.get_user_service(db)
        return user_service.get_user_info(user_id)

    def edit_user(self, new_user: UserEdit, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        user_service = self.get_user_service(db)
        return user_service.edit_user_profile(new_user, current_user.id)


user_api = UserAPI()
router = user_api.router    