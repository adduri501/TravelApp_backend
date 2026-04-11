
from app.orm.models.user_model import UserTable
from app.repositories.base_repository import BaseRepository

class AdminRepository(BaseRepository[UserTable]):pass
    
