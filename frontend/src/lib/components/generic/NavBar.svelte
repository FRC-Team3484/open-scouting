<script lang="ts">
	import { onMount } from "svelte";
	import Button from "../ui/button/button.svelte";
	import Logo from "./Logo.svelte";
	import { signOut, validateTokenOnline } from "$lib/utls/user";
	import * as Avatar from "../ui/avatar/index.js";
	import Skeleton from "../ui/skeleton/skeleton.svelte";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";

    let user = null;

    onMount(async () => {
        user = await validateTokenOnline();
    })
</script>

<div class="flex w-full h-24 flex-row justify-between items-center border-1 sticky top-0 bg-background/50 border-accent rounded-b-lg backdrop-blur-lg p-2">
    <Logo text={true} style="tiny" href="/" />

    <div class="flex flex-row gap-4 items-center">
        <Button variant="outline" href="/">Home</Button>
        <Button variant="outline" href="/" disabled>View Data</Button>
        <Button variant="outline" href="/" disabled>Events</Button>
    </div>

    <div class="flex flex-row gap-4 items-center">
        <Button variant="default" href="/start">Get Started</Button>

        {#if user === null}
            <Skeleton class="h-8 w-8 rounded-full" />
        {:else if user}
            <Button variant="outline" size="icon" class="!rounded-full">
                <DropdownMenu.Root>
                    <DropdownMenu.Trigger>
                        <Avatar.Root>
                            <!-- TODO: Actually load avatar from user account -->
                            <Avatar.Image src={`https://github.com/${user.username}.png`} alt={user.username} />
                            <Avatar.Fallback>{user.username}</Avatar.Fallback>
                        </Avatar.Root>
                    </DropdownMenu.Trigger>
                    <DropdownMenu.Content class="w-56" align="start">
                        <DropdownMenu.Label>{user.username}</DropdownMenu.Label>
                        <DropdownMenu.Group>
                            <DropdownMenu.Item>
                                Profile
                            </DropdownMenu.Item>
                        </DropdownMenu.Group>
                        <DropdownMenu.Separator />
                        <DropdownMenu.Item onclick={() => {signOut(); window.location.reload()}}>
                            Log out
                        </DropdownMenu.Item>
                    </DropdownMenu.Content>
                </DropdownMenu.Root>
            </Button>
        {:else}
            <Button variant="outline" href="/authentication">Login</Button>
        {/if}
    </div>
</div>