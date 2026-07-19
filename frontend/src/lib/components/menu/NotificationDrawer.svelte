<!-- 
@component
The notification drawer in the menu
-->
<script lang="ts">
	import { BellIcon, CheckCircleIcon, CircleNotchIcon, DotIcon, DotsThreeOutlineIcon, XCircleIcon } from "phosphor-svelte";

    import * as Sheet from "$lib/components/ui/sheet";
	import Button from "../ui/button/button.svelte";
	import { Separator } from "../ui/separator";

    import icon_rounded from "$lib/assets/icon_rounded.png"
	import { VERSION } from "$lib/utils/constants";
	import DrawerHeader from "../generic/drawers/DrawerHeader.svelte";
	import { liveQuery } from "dexie";
	import { db } from "$lib/utils/db";
	import Notification from "./Notification.svelte";
	import { slide } from "svelte/transition";
    import * as AlertDialog from "$lib/components/ui/alert-dialog";
	import { onMount } from "svelte";
	import { getNotifications, uploadNotifications } from "$lib/utils/notifications";

    let notifications = liveQuery(() => db.notifications.orderBy("created_at").reverse().toArray());
    let unreadCount = $derived.by(() => {
        if (!$notifications) return 0;
        return $notifications.filter((notification) => !notification.read).length
    });
    let allRead: boolean | null = $derived.by(() => {
        if (!$notifications) return null;
        if ($notifications.length === 0) return null;

        return $notifications.every((notification) => notification.read)
    });

    const DEBUG: boolean = true;

    async function syncNotifications() {
        await uploadNotifications().then(async () => {
            await getNotifications();
            console.log("Synced notifications")
        });
    }

    async function markAllAsRead() {
        if (!$notifications) return;
        await db.notifications.toCollection().modify({ read: true });
        await syncNotifications();
    }

    async function markAllAsUnread() {
        if (!$notifications) return;
        await db.notifications.toCollection().modify({ read: false });
        await syncNotifications();
    }

    async function deleteAll() {
        if (!$notifications) return;
        await db.notifications.filter((notification) => !notification.local).modify({ deleted: true });
        await db.notifications.filter((notification) => notification.local).delete();

        await syncNotifications();
    }

    onMount(async () => {
        await getNotifications();
    })
</script>

<Sheet.Root>
    <Sheet.Trigger>
        {#if notifications}
            <Button variant="ghost" class="text-lg">
                <BellIcon weight="bold" />
                {#if unreadCount > 0}
                    <div transition:slide={{ axis: "x" }}>
                        {unreadCount}
                    </div>
                {/if}
            </Button>
        {/if}
    </Sheet.Trigger>
    <Sheet.Content class="max-h-[80vh] min-h-[40vh] overflow-y-scroll lg:mx-64 2xl:mx-128 border-1 p-4 rounded-t-lg" side="bottom">
        <div class="overflow-y-scroll pr-2">
            <DrawerHeader title="Notifications" description="View and manage notifications" />

            {#if $notifications}
                <div class="flex flex-row gap-2 mb-2">
                    {#if allRead == false}
                        <Button variant="outline" size="sm" onclick={() => {markAllAsRead()}}>Mark all as read</Button>
                    {:else if allRead == true}
                        <Button variant="outline" size="sm" onclick={() => {markAllAsUnread()}}>Mark all as unread</Button>
                    {/if}

                    {#if DEBUG}
                        <Button size="sm" onclick={() => {syncNotifications()}}>Sync</Button>
                    {/if}

                    {#if $notifications.length > 0}
                        <AlertDialog.Root>
                            <AlertDialog.Trigger>
                                <Button variant="outline" size="sm">Delete all</Button>
                            </AlertDialog.Trigger>

                            <AlertDialog.Content>
                                <AlertDialog.Title>Delete all notifications</AlertDialog.Title>
                                <AlertDialog.Description>Are you sure you want to delete all notifications? This action cannot be undone.</AlertDialog.Description>
                                <AlertDialog.Footer>
                                    <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                    <AlertDialog.Action type="button" onclick={() => {deleteAll()}}>Delete</AlertDialog.Action>
                                </AlertDialog.Footer>
                            </AlertDialog.Content>
                        </AlertDialog.Root>
                    {/if}
                </div>

                <p class="text-muted-foreground">{$notifications.length} {$notifications.length === 1 ? "notification" : "notifications"} | {unreadCount} unread</p>

                <Separator orientation="horizontal" class="my-4" />

                <div class="flex flex-col gap-2">
                    {#each $notifications as notification}
                        <Notification notification={notification} />
                    {/each}
                </div>

                {#if $notifications.length === 0}
                    <div class="flex flex-col gap-2 justify-center items-center my-8 text-muted-foreground">
                        <CheckCircleIcon weight="bold" size={48} />
                        <p class="text-lg">No notifications</p>
                    </div>
                {/if}
            {:else}
                <CircleNotchIcon weight="bold" class="animate-spin" size={20} />
            {/if}
        </div>
    </Sheet.Content>
</Sheet.Root>