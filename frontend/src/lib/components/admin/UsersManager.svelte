<script lang="ts">
	import { deleteUserUsersDeleteUuidDelete, getUsersUsersGet, removeSuperuserUsersRemoveSuperuserUuidPost, setSuperuserUsersSetSuperuserUuidPost } from "$lib/api/auth/auth";
	import type { UserResponse } from "$lib/api/model";
    import * as Card from "$lib/components/ui/card";
	import { onMount } from "svelte";
	import Badge from "../ui/badge/badge.svelte";
	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";
    import * as AlertDialog from "$lib/components/ui/alert-dialog";
	import { toast } from "svelte-sonner";
	import { validateTokenOnline } from "$lib/utils/user";

    let users: UserResponse[] = $state([]);
    let selected: string[] = $state([]);
    let user_self = $state(null);

    async function getUsers() {
        selected = [];

        await getUsersUsersGet().then((res) => {
            if (res.status !== 200) {
                console.error(res)
                return
            } else {
                users = res.data

            }
        })
    }

    async function deleteUser(uuid: string) {
        await deleteUserUsersDeleteUuidDelete(uuid).then((res) => {
            if (res.status !== 200) {
                console.error(res)
                toast.error("Failed to delete user", { duration: 5000 });
                return
            } else {
                toast.success("User deleted", { duration: 5000 });
                getUsers();
            }
        })
    }

    async function deleteSelected() {
        for (const uuid of selected) {
            await deleteUser(uuid);
        }
    }

    async function makeSuperuser(uuid: string) {
        await setSuperuserUsersSetSuperuserUuidPost(uuid).then((res) => {
            if (res.status !== 200) {
                console.error(res)
                toast.error("Failed to make superuser", { duration: 5000 });
                return
            } else {
                toast.success("User made a superuser", { duration: 5000 });
                getUsers();
            }
        })
    }

    async function revokeSuperuser(uuid: string) {
        await removeSuperuserUsersRemoveSuperuserUuidPost(uuid).then((res) => {
            if (res.status !== 200) {
                console.error(res)
                toast.error("Failed to revoke superuser", { duration: 5000 });
                return
            } else {
                toast.success("Revoked superuser for user", { duration: 5000 });
                getUsers();
            }
        })
    }

    onMount(async () => {
        await getUsers();

        user_self = await validateTokenOnline();
    })
</script>

<div class="flex flex-col gap-4">
    <Card.Root class="w-auto">
        <Card.Header>
            <Card.Title>Users</Card.Title>
            <Card.Description>Manage users</Card.Description>
        </Card.Header>

        <Card.Content>
            <p>Found {users.length} users</p>
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Content class="flex flex-col gap-2">
            <div class="flex flex-row gap-2 items-center flex-wrap">
                <p>Selected {selected.length} users</p>
                <Button variant="outline" onclick={() => selected = users.map((user) => user.uuid)} disabled={selected.length == users.length}>Select All</Button>
                <Button variant="outline" onclick={() => selected = []} disabled={selected.length == 0}>Select None</Button>
                <Separator orientation="vertical" />
                <AlertDialog.Root>
                    <AlertDialog.Trigger>
                        <Button variant="destructive" disabled={selected.length == 0}>Delete {selected.length} users</Button>
                    </AlertDialog.Trigger>

                    <AlertDialog.Content>
                        <AlertDialog.Title>Delete {selected.length} users</AlertDialog.Title>
                        <AlertDialog.Description>
                            Are you sure you want to delete {selected.length} users? This action cannot be undone.
                        </AlertDialog.Description>
                        <AlertDialog.Footer>
                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                            <AlertDialog.Action type="button" onclick={deleteSelected}>Delete</AlertDialog.Action>
                        </AlertDialog.Footer>
                    </AlertDialog.Content>
                </AlertDialog.Root>
            </div>

            <Separator orientation="horizontal" />
            
            {#each users as user}
                <Card.Root>
                    <Card.Content>
                        <div class="flex flex-col gap-2">
                            <div class="flex flex-row gap-2 items-center flex-wrap">
                                <input type="checkbox" bind:group={selected} value={user.uuid} />
                                <p class="wrap-anywhere font-bold">{user.username}</p>
                                {#if user.is_superuser}
                                    <Badge>Superuser</Badge>
                                {/if}
                                {#if user_self != null}
                                    {#if user.uuid == user_self.uuid}
                                        <Badge>Self</Badge>
                                    {/if}
                                {/if}
                            </div>

                            <div class="flex flex-row gap-2 items-center flex-wrap">
                                <p class="wrap-anywhere">{user.email}</p>
                                <p class="text-sm text-muted-foreground">Created: {user.created_at}</p>
                            </div>

                            <div class="flex flex-row gap-2 items-center flex-wrap">
                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button variant="destructive" size="sm">Delete</Button>
                                    </AlertDialog.Trigger>

                                    <AlertDialog.Content>
                                        <AlertDialog.Title>Delete User "{user.username}"</AlertDialog.Title>
                                        <AlertDialog.Description>Are you sure you want to delete this user? This action cannot be undone.</AlertDialog.Description>
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action type="button" onclick={() => deleteUser(user.uuid)}>Delete</AlertDialog.Action>
                                        </AlertDialog.Footer>
                                    </AlertDialog.Content>
                                </AlertDialog.Root>
                                {#if !user.is_superuser}
                                    <Button variant="outline" size="sm" onclick={() => makeSuperuser(user.uuid)} disabled={user.uuid == user_self?.uuid}>Make Superuser</Button>
                                {:else}
                                    <Button variant="outline" size="sm" onclick={() => revokeSuperuser(user.uuid)} disabled={user.uuid == user_self?.uuid}>Remove Superuser</Button>
                                {/if}
                            </div>
                        </div>
                    </Card.Content>
                </Card.Root>
            {/each}
        </Card.Content>
    </Card.Root>
</div>