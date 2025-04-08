from ..models.user import UserEdit
from ..repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def get_user_info(self, user_id: int):
        user = self.user_repo.get_user_by_id(user_id)
        return {field: getattr(user, field) for field in ["username", "avatar_url", "user_status", "created_at"]}
    
    def edit_user_profile(self, new_user: UserEdit, user_id: int):
        return self.user_repo.update_user(user_id, new_user)