from typing import Any
import uuid as uuid_module

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import Identity, require_user
from ..models import Notification, User
from ..schemas.generic import MessageResponse
from ..schemas.notifications import NotificationRequest, NotificationResponse
from ..utils import IS_DEV


router: APIRouter = APIRouter(
    tags=["Notifications"],
    include_in_schema=IS_DEV
)

async def send_notification(
    user: User,
    title: str,
    message: str,
    type: str,
    action_type: str | None = None,
    action_data: dict[Any, Any] | None = None,
    read: bool = False,
    uuid: uuid_module.UUID | None = None
):
    """
    Send a notification to a user

    This function can be used by other parts of the backend to send notifications

    Parameters:
        user (User): The user to send the notification to
        title (str): The title of the notification
        message (str): The message of the notification
        type (str): The type of the notification
        action (dict): The action of the notification
        read (bool): Whether the notification is read
        uuid (UUID): The uuid of the notification

    Returns:
        Notification: The notification that was sent
    """
    if not uuid:
        uuid = uuid_module.uuid4()

    return await Notification.get_or_create(
        uuid=uuid,
        user=user,
        title=title,
        message=message,
        type=type,
        action_type=action_type,
        action_data=action_data,
        read=read
    )

@router.get("/notifications", response_model=list[NotificationResponse])
async def get_notifications(identity: Identity = Depends(require_user)):
    """
    Get all notifications for the current user

    Requires user authentication

    Returns:
        list[Notification]: A list of all notifications
    """
    print(await Notification.filter(user=identity.user))
    return [
        NotificationResponse(
            uuid=notification.uuid,
            title=notification.title,
            message=notification.message,
            type=notification.type,
            action_type=notification.action_type,
            action_data=notification.action_data,
            read=notification.read,
            created_at=notification.created_at
        ) for notification in await Notification.filter(user=identity.user)
    ]

@router.delete("/notifications/delete/{notification_uuid}", response_model=MessageResponse)
async def delete_notification(notification_uuid: uuid_module.UUID, identity: Identity = Depends(require_user)) -> MessageResponse:
    """
    Delete a notification

    Requires user authentication

    Parameters:
        notification_uuid (`UUID`): The UUID of the notification to delete

    Returns:
        MessageResponse: A message indicating that the notification was deleted
    """
    _ = await Notification.filter(uuid=notification_uuid, user=identity.user).delete()
    return MessageResponse(message="Notification deleted")

@router.put("/notifications/set_read/{notification_uuid}/{read}", response_model=MessageResponse)
async def set_notification_read(notification_uuid: uuid_module.UUID, read: bool, identity: Identity = Depends(require_user)) -> MessageResponse:
    """
    Mark a notification as read or unread

    Requires user authentication

    Parameters:
        notification_uuid (`UUID`): The UUID of the notification to mark as read
        read (`bool`): The read status of the notification

    Returns:
        MessageResponse: A message indicating that the notification was marked as read or unread
    """
    _ = await Notification.filter(uuid=notification_uuid, user=identity.user).update(read=read)
    return MessageResponse(message=f"Notification marked read = {read}")

@router.post("/notifications/send", response_model=NotificationResponse | MessageResponse)
async def add_notification(data: NotificationRequest, identity: Identity = Depends(require_user)):
    """
    Add a notification to the database

    This is used when the client creates a notification that needs to be synced to the server

    Requires user authentication

    Parameters:
        data (`NotificationRequest`): The data to create the notification with

    Returns:
        NotificationResponse: The notification that was created
    """
    if not identity.user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if data.deleted:
        print("deleting notification", data.uuid)
        notification = await Notification.get(uuid=data.uuid, user=identity.user)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")

        await notification.delete()

        return MessageResponse(message="Notification deleted")

    print("adding notification", data.uuid)
    notification, created = await send_notification(
        user=identity.user,
        title=data.title,
        message=data.message,
        type=data.type,
        action_type=data.action_type,
        action_data=data.action_data,
        uuid=data.uuid
    )


    return NotificationResponse(
        uuid=notification.uuid,
        title=notification.title,
        message=notification.message,
        type=notification.type,
        action_type=notification.action_type,
        action_data=notification.action_data,
        read=notification.read,
        created_at=notification.created_at
    )