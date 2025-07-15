from app.domains.notification.services import EmailNotificationService
from app.domains.user.exceptions import UserNotExistError
from app.domains.user.models import UserEntity
from app.domains.user.repo import UserRepository
from app.settings import AppSettings


class UserService:

    def __init__(
        self,
        settings: AppSettings,
        notification_service: EmailNotificationService,
        repo: UserRepository,
    ):
        self.settings = settings
        self.repo = repo
        self.notification_service = notification_service

    async def select_user(self, user_id: int) -> UserEntity:
        user = await self.repo.select_user(user_id)
        if user is None:
            raise UserNotExistError()
        return user

    async def set_user_as_admin(self, user_id: int) -> None:
        user = await self.select_user(user_id)
        await self.repo.set_user_as_admin(user_id)
        await self.notification_service.send(user.email, f"You're admin now, {user.name}")
