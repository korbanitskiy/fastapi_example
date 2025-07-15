from app.settings import AppSettings


class EmailClient:
    def __init__(self, settings: AppSettings):
        self.settings = settings

    async def send(self, email: str, msg: str) -> None:
        print(f"send {msg} to email {email}")
