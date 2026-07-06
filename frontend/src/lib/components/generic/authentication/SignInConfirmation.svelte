<!-- 
@component
Used in the universal authentication component

Shows user information for the user that was just authenticated, then redirects them to the home page

Props:
    - `user` (`UserResponse | null`) - The user that was just authenticated
    - `redirect` (`number`) - The number of seconds to redirect the user. Set to 0 to redirect immediately

-->
<script lang="ts">
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { ArrowRightIcon, CheckCircleIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";
    import Button from "$lib/components/ui/button/button.svelte";
    import * as Avatar from "$lib/components/ui/avatar/index.js";
    
	import type { UserResponse } from "$lib/api/model";
	import { slide } from "svelte/transition";


    interface Props {
        user: UserResponse | null
        redirect?: number
    }
    let { user, redirect = 5 }: Props = $props();

    let interval: any = $state(null);

    /**
     * When mounting the component, start the redirect timer
     */
    onMount(() => {
        interval = setInterval(async () => {
            redirect--;
            if (redirect <= 0) {
                clearInterval(interval);
                await goto("/");
                window.location.reload()
            }
        }, 1000);

        return () => {
            clearInterval(interval);
        };
    });
</script>

<div class="flex flex-col gap-2 text-center items-center my-4" transition:slide>
    <div class="flex flex-row gap-2 items-center">
        <CheckCircleIcon weight="bold" />
        <p class="font-bold">Successfully signed in</p>
    </div>

    {#if user}
        <div>
            <Card.Root>
                <Card.Content>
                    <div class="flex flex-row gap-2 items-center">
                        <Avatar.Root class="size-16">
                            <Avatar.Image src={user.profile_picture_url} alt={user.username} />
                            <Avatar.Fallback>{user.username.substring(0, 1)}</Avatar.Fallback>
                        </Avatar.Root>
                        <div class="flex flex-col gap-1 items-start">
                            <p>{user.display_name}</p>
                            {#if user.username != user.display_name}
                                <p class="text-muted-foreground">({user.username})</p>
                            {/if}
                            <p class="text-muted-foreground">{user.email}</p>
                        </div>
                    </div>
                </Card.Content>
            </Card.Root>
        </div>
    {/if}

    <p class="text-muted-foreground animate-pulse">Redirecting home in {redirect}...</p>
    <Button onclick={async () => {await goto("/"); window.location.reload()}}><ArrowRightIcon weight="bold" /> Redirect now</Button>
</div>