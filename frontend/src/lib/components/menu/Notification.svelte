<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";

	import { db, type Notification } from "$lib/utils/db";
	import { getNotifications } from "$lib/utils/notifications";
	import { onMount } from "svelte";
	import Button from "../ui/button/button.svelte";
	import Badge from "../ui/badge/badge.svelte";


    const DEBUG: boolean = true;

    interface Props {
        notification: Notification
    }
    let { notification }: Props = $props();

    let minutesAgo: string = $derived.by(() => {
        const seconds = Math.floor((new Date() - new Date(notification.created_at)) / 1000);

        const intervals = {
            year: 31536000,
            month: 2592000,
            day: 86400,
            hour: 3600,
            minute: 60
        };

        let counter;
        
        counter = Math.floor(seconds / intervals.year);
        if (counter > 0) return `${counter} year${counter === 1 ? '' : 's'} ago`;

        counter = Math.floor(seconds / intervals.month);
        if (counter > 0) return `${counter} month${counter === 1 ? '' : 's'} ago`;

        counter = Math.floor(seconds / intervals.day);
        if (counter > 0) return `${counter} day${counter === 1 ? '' : 's'} ago`;

        counter = Math.floor(seconds / intervals.hour);
        if (counter > 0) return `${counter}h ago`;

        counter = Math.floor(seconds / intervals.minute);
        if (counter > 0) return `${counter}m ago`;

        return `${Math.max(0, seconds)}s ago`;
    });

    async function toggleRead() {
        await db.notifications.where("uuid").equals(notification.uuid).modify({ read: !notification.read });
    }

    async function deleteNotification() {
        await db.notifications.where("uuid").equals(notification.uuid).modify({ deleted: true });
    }

    onMount(() => {
        getNotifications();
    });
</script>

<Card.Root>
    <Card.Content>
        <div class="flex flex-col gap-2">
            <div class="flex flex-row gap-2 justify-between">

                <div class="flex flex-row gap-2 items-center">
                    {#if !notification.read}
                        <span class="h-2 w-2 rounded-full bg-blue-500"></span>
                    {/if}
                    <p class="font-bold">{notification.title}</p>

                    {#if DEBUG}
                        {#if notification.read}
                            <Badge class="bg-green-500">Read</Badge>
                        {:else}
                            <Badge class="bg-red-500">Unread</Badge>
                        {/if}
                        
                        {#if notification.deleted}
                            <Badge class="bg-yellow-500">Deleted</Badge>
                        {/if}
                    {/if}
                </div>

                <div class="flex flex-row gap-2 items-center">
                    <p class="text-muted-foreground text-sm">{minutesAgo}</p>
                        <Button variant="outline" size="sm" onclick={() => {toggleRead()}}>
                            {#if notification.read}
                                Unread
                            {:else}
                                Read
                            {/if}
                        </Button>

                    <Button variant="outline" size="sm" onclick={() => {deleteNotification()}}>Delete</Button>
                </div>
            </div>
            <p class="text-muted-foreground text-sm">{notification.message}</p>
        </div>
    </Card.Content>
</Card.Root>