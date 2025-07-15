from app.domains.notification.clients import EmailClient
from app.domains.notification.exceptions import InvalidEmailError
from app.settings import AppSettings


class EmailNotificationService:
    def __init__(self, settings: AppSettings, client: EmailClient):
        self.settings = settings
        self.client = client

    def validate_email(self, email: str):
        is_valid = "@" in email
        if not is_valid:
            raise InvalidEmailError()

    async def send(self, email: str, msg: str) -> None:
        self.validate_email(email)
        await self.client.send(email, msg)
