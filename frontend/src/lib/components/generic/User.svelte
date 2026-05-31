<!-- 
@component
Generic component for displaying the user's auth state

TODO: Create a proper interface for the user

Props:
    - `show_text` (`boolean`) - If true, shows the user's username
-->
<script lang="ts">
	import { dev } from "$app/environment";
	import { onMount } from "svelte";
	import { BookIcon, SignOutIcon, UserCircleIcon, WrenchIcon } from "phosphor-svelte";

    import Skeleton from "../ui/skeleton/skeleton.svelte";
    import Button from "../ui/button/button.svelte";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
    import * as Avatar from "$lib/components/ui/avatar/index.js";

    import { signOut, validateTokenOnline } from "$lib/utils/user";


    interface Props {
        show_text: boolean
    }
    let { show_text = true }: Props = $props();

    let user = $state(null);

    onMount(async () => {
        user = await validateTokenOnline();
    })
</script>

{#if user === null}
    <Skeleton class="h-8 w-8 rounded-full" />
{:else if user}
    <Button variant="outline" size="icon" class="!rounded-full">
        <DropdownMenu.Root>
            <DropdownMenu.Trigger>
                <Avatar.Root>
                    <!-- TODO: Actually load avatar from user account -->
                    <!-- <Avatar.Image src={`https://github.com/${user.username}.png`} alt={user.username} /> -->
                    <Avatar.Fallback>{user.username.substring(0, 1)}</Avatar.Fallback>
                </Avatar.Root>
            </DropdownMenu.Trigger>
            <DropdownMenu.Content class="w-56" align="start">
                <DropdownMenu.Label>{user.username}</DropdownMenu.Label>
                <DropdownMenu.Group>
                    <DropdownMenu.Item>
                        <UserCircleIcon weight="bold" /> Profile
                    </DropdownMenu.Item>
                    {#if user.is_superuser}
                        <DropdownMenu.Label>Admin Options</DropdownMenu.Label>
                        <DropdownMenu.Item onclick={() => window.location.href = "/admin"} class="bg-green-400/50 hover:bg-green-300/20! transition-colors m-1">
                            <WrenchIcon weight="bold" /> Admin Dashboard
                        </DropdownMenu.Item>
                        <DropdownMenu.Item onclick={() => {if (dev) window.location.href = "http://localhost:8000/docs"; else window.location.href = "/api/docs";}} class="bg-green-400/50 hover:bg-green-300/20! transition-colors m-1">
                            <BookIcon weight="bold" /> Swagger API Docs
                        </DropdownMenu.Item>
                    {/if}
                </DropdownMenu.Group>
                <DropdownMenu.Separator />
                <DropdownMenu.Item onclick={() => {signOut(); window.location.reload()}}>
                    <SignOutIcon weight="bold" /> Log out
                </DropdownMenu.Item>
            </DropdownMenu.Content>
        </DropdownMenu.Root>
    </Button>

    {#if show_text}
        <p class="text-muted-foreground">{user.username}</p>
    {/if}
{:else}
    <Button variant="outline" href="/authentication">Login</Button>
{/if}