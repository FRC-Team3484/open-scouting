<!-- 
@component
Generic component for displaying the user's auth state

Props:
    - `show_text` (`boolean`) - If true, shows the user's username
-->
<script lang="ts">
	import { dev } from "$app/environment";
	import { BookIcon, SignOutIcon, UserCircleIcon, WrenchIcon } from "phosphor-svelte";

    import Skeleton from "../ui/skeleton/skeleton.svelte";
    import Button from "../ui/button/button.svelte";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
    import * as Avatar from "$lib/components/ui/avatar/index.js";

    import { signOut } from "$lib/utils/user";
	import { goto } from "$app/navigation";
	import { user, type UserData } from "$lib/utils/auth";


    interface Props {
        show_text: boolean
    }
    let { show_text = true }: Props = $props();
</script>

{#if $user.loading}
    <Skeleton class="h-8 w-8 rounded-full" />
{:else if $user.user && !$user.loading && $user.authenticated}
    <Button variant="outline" size="icon" class="!rounded-full">
        <DropdownMenu.Root>
            <DropdownMenu.Trigger>
                <Avatar.Root>
                    <Avatar.Image src={$user.user.profile_picture_url} alt={$user.user.username} />
                    <Avatar.Fallback>{$user.user.username.substring(0, 1)}</Avatar.Fallback>
                </Avatar.Root>
            </DropdownMenu.Trigger>
            <DropdownMenu.Content class="w-56" align="start">
                <DropdownMenu.Label>{$user.user.username}</DropdownMenu.Label>
                <DropdownMenu.Group>
                    <DropdownMenu.Item onclick={async () => await goto("/profile")}>
                        <UserCircleIcon weight="bold" /> Profile
                    </DropdownMenu.Item>
                    {#if $user.user.is_superuser}
                        <DropdownMenu.Label>Admin Options</DropdownMenu.Label>
                        <DropdownMenu.Item onclick={async () => await goto("/admin")} class="bg-green-400/50 hover:bg-green-300/20! transition-colors m-1">
                            <WrenchIcon weight="bold" /> Admin Dashboard
                        </DropdownMenu.Item>
                        <DropdownMenu.Item onclick={() => {if (dev) window.location.href = "http://localhost:8000/docs"; else window.location.href = "/api/docs";}} class="bg-green-400/50 hover:bg-green-300/20! transition-colors m-1">
                            <BookIcon weight="bold" /> Swagger API Docs
                        </DropdownMenu.Item>
                    {/if}
                </DropdownMenu.Group>
                <DropdownMenu.Separator />
                <DropdownMenu.Item onclick={async () => {await signOut()}}>
                    <SignOutIcon weight="bold" /> Log out
                </DropdownMenu.Item>
            </DropdownMenu.Content>
        </DropdownMenu.Root>
    </Button>

    {#if show_text}
        <p class="text-muted-foreground">{$user.user.username}</p>
    {/if}
{:else}
    <Button variant="outline" href="/authentication">Login</Button>
{/if}