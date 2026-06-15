<!-- 
@component
Sign in mode for the universal authentication component

TODO: Support passkeys

-->
<script lang="ts">
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";
	import { slide } from "svelte/transition";
	import { ArrowLeftIcon, ArrowRightIcon, CheckCircleIcon, CircleNotchIcon, EnvelopeIcon, KeyIcon, WarningIcon } from "phosphor-svelte";

    import * as Avatar from "$lib/components/ui/avatar/index";
    import * as Card from "$lib/components/ui/card/index";
	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
    import * as Alert from "$lib/components/ui/alert/index";

	import { loginAuthLoginPost, meAuthMeGet } from "$lib/api/auth/auth";
	import type { UserResponse } from "$lib/api/model";


    let page: "username" | "passkey" | "password" | "success" = $state("username"); 

    let username: string = $state("");
    let password: string = $state("");

    let loading: boolean = $state(false);
    let message: string = $state("");

    let successUser: UserResponse | null = $state(null);
    let redirectTimer: number = $state(5);

    let interval: any = $state(null);

    /**
     * Sign the user in
     */
    async function signIn() {
        loading = true;
        await loginAuthLoginPost({username, password}).then(async (response) => {
            if (response.status == 200) {
                
                await meAuthMeGet().then((response) => {
                    if (response.status == 200) {
                        successUser = response.data.user;
                    }
                });
                
                interval = setInterval(async () => {
                    redirectTimer -= 1;
                    
                    if (redirectTimer == 0) {
                        clearInterval(interval);
                        await goto("/");
                        window.location.reload();
                    }
                }, 1000);
                page = "success";
            } else {
                message = response.data.detail;
            }
        });
        loading = false;
    }

    /**
     * Change page state when the enter key is pressed
     * @param e
     */
    function handleKeyDown(e: KeyboardEvent) {
        if (e.key == "Enter") {
            if (page == "username" && username.trim() != "") {
                page = "password";
            } else if (page == "password" && password.trim() != "") {
                signIn();
            } else if (page == "success") {
                clearInterval(interval);
                goto("/");
                window.location.reload();
            }
        }
    }

    onMount(() => {
        return () => {
            clearInterval(interval);
        }
    })
</script>

<svelte:window on:keydown={handleKeyDown} />

{#if message}
    <div transition:slide>
        <Alert.Root variant="destructive" class="mb-2 text-left">
            <WarningIcon weight="bold" />
            <Alert.Title>There was a problem</Alert.Title>
            <Alert.Description>{message}</Alert.Description>
        </Alert.Root>
    </div>
{/if}

{#if page == "username"}
    <div class="flex flex-col gap-2 text-left" transition:slide>
        <p class="font-bold mb-4 text-lg">Welcome back</p>

        <div class="flex flex-row gap-2 items-center">
            <EnvelopeIcon weight="bold" />
            <p class="font-bold">Username or email</p>
        </div>
        <Input placeholder="Username or email" type="text" bind:value={username} autofocus />
        <Button onclick={() => {page = "password"}} disabled={username.trim() == ""}><ArrowRightIcon weight="bold" /> Next</Button>
    </div>
{:else if page == "passkey"}
    <div class="flex flex-col gap-2 text-left" transition:slide>
        <p>Passkeys are not yet supported</p>
        <Button onclick={() => {page = "password"}}><ArrowLeftIcon weight="bold" /> Password Login</Button>
    </div>
{:else if page == "password"}
    <div class="flex flex-col gap-2 text-left" transition:slide>
        <div class="flex flex-row gap-2 items-center mb-4">
            <Button variant="outline" onclick={() => {page = "username"}}><ArrowLeftIcon weight="bold" /> Back</Button>
            <p>Signing in as <span class="font-bold">{username}</span></p>
        </div>
        <div class="flex flex-row gap-2 items-center">
            <KeyIcon weight="bold" />
            <p class="font-bold">Password</p>
        </div>
        <Input placeholder="Password" type="password" bind:value={password} autofocus />
        <Button onclick={() => {signIn()}} disabled={password.trim() == "" || loading} onkeydown={(e) => {if (e.key == "Enter") {signIn();}}}>
            {#if loading}
                <CircleNotchIcon class="animate-spin" size={16} /> Loading...
            {:else}
                <ArrowRightIcon weight="bold" /> Sign In
            {/if}
        </Button>
    </div>
{:else if page == "success"}
    <div class="flex flex-col gap-2 text-center items-center my-4" transition:slide>
        <div class="flex flex-row gap-2 items-center">
            <CheckCircleIcon weight="bold" />
            <p class="font-bold">Successfully signed in</p>
        </div>

        {#if successUser}
            <div transition:slide>
                <Card.Root>
                    <Card.Content>
                        <div class="flex flex-row gap-2 items-center">
                            <Avatar.Root class="size-16">
                                <Avatar.Image src={successUser.profile_picture_url} alt={successUser.username} />
                                <Avatar.Fallback>{successUser.username.substring(0, 1)}</Avatar.Fallback>
                            </Avatar.Root>
                            <div class="flex flex-col gap-1 items-start">
                                <p>{successUser.display_name}</p>
                                {#if successUser.username != successUser.display_name}
                                    <p class="text-muted-foreground">({successUser.username})</p>
                                {/if}
                                <p class="text-muted-foreground">{successUser.email}</p>
                            </div>
                        </div>
                    </Card.Content>
                </Card.Root>
            </div>
        {/if}

        <p class="text-muted-foreground animate-pulse">Redirecting home in {redirectTimer}...</p>
        <Button onclick={async () => {await goto("/"); window.location.reload()}}><ArrowRightIcon weight="bold" /> Home</Button>
    </div>
{/if}
