import { addNotificationNotificationsSendPost, getNotificationsNotificationsGet } from "$lib/api/notifications/notifications";
import { toast } from "svelte-sonner";
import { db } from "./db";

type ToastOptions = {
    description?: string;
    duration?: number;
}

class NotificationManager {
    private async create(
        title: string, 
        message: string | null = null, 
        type: string = "info", 
        action_type: string | null = null, 
        action_data: string | null = null, 
        local: boolean = true,
        duration: number | null = null
    ) {
        
        await db.notifications.add({
            uuid: crypto.randomUUID(),
            title: title,
            message: message || "",
            type: type,
            action_type: action_type,
            action_data: action_data,
            read: false,
            deleted: false,
            local: local,
            created_at: new Date()
        });

        let toastOptions: ToastOptions = {}

        if (message) {
            toastOptions.description = message;
        }

        if (duration) {
            toastOptions.duration = duration;
        }

        if (type == "success") {
            toast.success(title, toastOptions);
        } else if (type == "info") {
            toast.info(title, toastOptions);
        } else if (type == "warning") {
            toast.warning(title, toastOptions);
        } else if (type == "error") {
            toast.error(title, toastOptions);
        } else {
            toast(title, toastOptions);
        }
    }

    public success(title: string, message: string) {
        this.create(title, message, "success");
    }

    public info(title: string, message: string) {
        this.create(title, message, "info");
    }

    public warning(title: string, message: string) {
        this.create(title, message, "warning");
    }

    public error(title: string, message: string) {
        this.create(title, message, "error");
    }
}

const notifications = new NotificationManager();

/*
* Get the user's notifications from the server
* 
* If a new one is found, show a notification using toast
*/
async function getNotifications() {
    console.log("getting notifications from server")
    await getNotificationsNotificationsGet().then((response) => {
        if (response.status == 200) {
            response.data.forEach((notification) => {
                console.log("notification " + notification.uuid + " received");
                db.notifications.get(notification.uuid).then((result) => {
                    if (!result) {
                        db.notifications.put({
                            uuid: notification.uuid,
                            title: notification.title,
                            message: notification.message,
                            type: notification.type,
                            action_type: notification.action_type,
                            action_data: notification.action_data,
                            read: notification.read,
                            deleted: notification.deleted,
                            local: notification.local,
                            created_at: notification.created_at
                        });

                        notifications.create(notification.title, notification.message, notification.type, notification.action_type, notification.action_data, notification.local);
                    }
                });
            })
        }
    });
}

/*
* Upload all non local notifications to the server
*/
async function uploadNotifications() {
    // return (await uploadNotificationsNotificationsPost()).data;
    console.log("uploading notifications to server")

    await db.notifications.filter((notification) => !notification.local).toArray().then(async (notifications) => {
        notifications.forEach(async (notification) => {
            console.log(notification.uuid, notification.deleted)


            await addNotificationNotificationsSendPost({
                uuid: notification.uuid,
                title: notification.title,
                message: notification.message,
                type: notification.type,
                action_type: notification.action_type,
                action_data: notification.action_data,
                read: notification.read,
                deleted: notification.deleted
            }).then((response) => {
                if (response.status == 200) {
                    console.log("notification " + notification.uuid + " sent");
                }
            })
        });
    })
}

export {
    notifications,
    getNotifications,
    uploadNotifications
}