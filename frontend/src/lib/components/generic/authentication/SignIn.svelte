<!-- 
@component
Sign in mode for the universal authentication component

Props:
    - `ref` (`string`) - The ref to redirect to
-->
<script lang="ts">
	import { goto } from "$app/navigation";
	import { ArrowRightIcon, CircleNotchIcon, EnvelopeIcon, KeyIcon, KeyReturnIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
    import * as Kbd from "$lib/components/ui/kbd/index";

	import { loginAuthLoginPost, meAuthMeGet } from "$lib/api/auth/auth";
	import type { UserResponse } from "$lib/api/model";
	import SignInConfirmation from "./SignInConfirmation.svelte";
	import Switch from "$lib/components/ui/switch/switch.svelte";
	import Label from "$lib/components/ui/label/label.svelte";
	import { startAuthentication } from "@simplewebauthn/browser";
	import AuthenticationMessage from "./AuthenticationMessage.svelte";
	import AuthenticationPage from "./AuthenticationPage.svelte";
	import { createLoginPasskeyPasskeysLoginCreatePost, verifyLoginPasskeyPasskeysLoginVerifyPost } from "$lib/api/passkeys/passkeys";


    interface Props {
        ref?: string;
    }
    let { ref = "/" }: Props = $props();

    let page: "username" | "password" | "success" = $state("username"); 

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
            const options = await createLoginPasskeyPasskeysLoginCreatePost();

            const authenticationResponse = await startAuthentication({
                optionsJSON: options.data,
            });

            await verifyLoginPasskeyPasskeysLoginVerifyPost(authenticationResponse, {challenge_uuid: options.data.challenge_uuid}).then(async (response) => {
                if (response.status == 200) {
                    await meAuthMeGet().then((response) => {
                        if (response.status == 200) {
                            successUser = response.data.user;
                        }
                    });
                    page = "success";
                    message = "";
                } else {
                    message = response.data.message;
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
                goto(ref);
                window.location.reload();
            }
        }
    }
</script>

<svelte:window on:keydown={handleKeyDown} />

<AuthenticationMessage {message} />

{#if page == "username"}
    <AuthenticationPage title="Username or email">
        {#snippet icon()}
            <EnvelopeIcon weight="bold" />
        {/snippet}

        {#snippet content()}
            <Input placeholder="Username or email" type="text" bind:value={username} autofocus />
            <Button onclick={() => {page = "password"}} disabled={username.trim() == ""}><ArrowRightIcon weight="bold" /> Next <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root></Button>
            <Button variant="outline" size="sm" onclick={() => {loginWithPasskey()}}><KeyIcon weight="bold" /> Sign In with Passkey</Button>
        {/snippet}
    </AuthenticationPage>

{:else if page == "password"}
    <AuthenticationPage title="Enter Password" onBackButtonClick={() => {page = "username"; message = ""; password = ""; loading = false}}>
        {#snippet icon()}
            <KeyIcon weight="bold" />
        {/snippet}

        {#snippet content()}
            <p class="mb-4">Signing in as <span class="font-bold">{username}</span></p>

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
        {/snippet}
    </AuthenticationPage>

{:else if page == "success"}
    <SignInConfirmation user={successUser} redirect={5} ref={ref} />
{/if}
