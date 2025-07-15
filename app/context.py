from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.database.session import get_session
from app.domains.notification.clients import EmailClient
from app.domains.notification.services import EmailNotificationService
from app.domains.user.repo import UserRepository
from app.domains.user.services import UserService


async def get_app_settings() -> settings.AppSettings:
    return settings.get_app_settings()


async def get_user_repo(
    settings: Annotated[settings.AppSettings, Depends(get_app_settings)],
    db_session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRepository:
    return UserRepository(
        settings,
        db_session,
    )


async def get_email_notification_client(
    settings: Annotated[settings.AppSettings, Depends(get_app_settings)],
) -> EmailClient:
    return EmailClient(
        settings=settings,
    )


async def get_notification_service(
    settings: Annotated[settings.AppSettings, Depends(get_app_settings)],
    email_client: Annotated[EmailClient, Depends(get_email_notification_client)],
) -> EmailNotificationService:
    return EmailNotificationService(
        settings=settings,
        client=email_client,
    )


async def get_user_service(
    settings: Annotated[settings.AppSettings, Depends(get_app_settings)],
    user_repo: Annotated[UserRepository, Depends(get_app_settings)],
    notification_service: Annotated[EmailNotificationService, Depends(get_notification_service)],
) -> UserService:
    return UserService(
        settings=settings,
        notification_service=notification_service,
        repo=user_repo,
    )
