<!-- 
@component
Sign in mode for the universal authentication component

TODO: Support passkeys

-->
<script lang="ts">
	import { goto } from "$app/navigation";
	import { slide } from "svelte/transition";
	import { ArrowLeftIcon, ArrowRightIcon, CircleNotchIcon, EnvelopeIcon, KeyIcon, KeyReturnIcon, WarningIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
    import * as Alert from "$lib/components/ui/alert/index";
    import * as Kbd from "$lib/components/ui/kbd/index";

	import { createLoginPasskeyAuthPasskeysLoginCreatePost, loginAuthLoginPost, meAuthMeGet, verifyLoginPasskeyAuthPasskeysLoginVerifyPost } from "$lib/api/auth/auth";
	import type { UserResponse } from "$lib/api/model";
	import SignInConfirmation from "./SignInConfirmation.svelte";
	import Switch from "$lib/components/ui/switch/switch.svelte";
	import Label from "$lib/components/ui/label/label.svelte";
	import { startAuthentication } from "@simplewebauthn/browser";


    let page: "username" | "passkey" | "password" | "success" = $state("username"); 

    let username: string = $state("");
    let password: string = $state("");
    let showPassword: boolean = $state(false);

    let loading: boolean = $state(false);
    let message: string = $state("");

    let successUser: UserResponse | null = $state(null);
    

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
                page = "success";
            } else {
                message = response.data.detail;
            }
        });
        loading = false;
    }

    /**
     * Login with a passkey
     */
    async function loginWithPasskey() {
        try {
            const options = await createLoginPasskeyAuthPasskeysLoginCreatePost();

            const authenticationResponse = await startAuthentication({
                optionsJSON: options.data,
            });

            await verifyLoginPasskeyAuthPasskeysLoginVerifyPost(authenticationResponse, {challenge_uuid: options.data.challenge_uuid}).then(async (response) => {
                if (response.status == 200) {
                    await meAuthMeGet().then((response) => {
                        if (response.status == 200) {
                            successUser = response.data.user;
                        }
                    });
                    page = "success";
                }
            });
        } catch (error) {
            console.error(error);
            message = error.message
        }
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
                goto("/");
                window.location.reload();
            }
        }
    }
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
        <Button onclick={() => {page = "password"}} disabled={username.trim() == ""}><ArrowRightIcon weight="bold" /> Next <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root></Button>
        <Button variant="outline" size="sm" onclick={() => {loginWithPasskey()}}><KeyIcon weight="bold" /> Sign In with Passkey</Button>
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
        <Input placeholder="Password" type={showPassword ? "text" : "password"} bind:value={password} autofocus />
        <div class="flex flex-row gap-2 mb-4">
            <Switch id="show-password" bind:checked={showPassword} />
            <Label for="show-password">Show Password</Label>
        </div>

        <Button onclick={() => {signIn()}} disabled={password.trim() == "" || loading} onkeydown={(e) => {if (e.key == "Enter") {signIn();}}}>
            {#if loading}
                <CircleNotchIcon class="animate-spin" size={16} /> Loading...
            {:else}
                <ArrowRightIcon weight="bold" /> Sign In <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
            {/if}
        </Button>
    </div>
{:else if page == "success"}
    <SignInConfirmation user={successUser} redirect={5} />
{/if}
