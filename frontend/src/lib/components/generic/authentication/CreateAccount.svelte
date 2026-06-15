<!-- 
@component
Used by the universal authentication component, for creating a user account

First, the user provides a username and email. These are verified to be unique on the server.
Then, the user is asked to verify their email (if enabled). This component listens to 
    the `verified` prop of the `EmailVerification` component, and if it is true, the 
    user can proceed to the next step.
Then, the user will be asked to create a password, and the password strength will be shown.Alert
Finally, the user will be asked to provide a display name and a team number.
Then, the account will be created on the server, and the user will be authenticated.Alert
Finally, ask the user to create a passkey.
Then show the user the `SignInConfirmation` component.
-->
<script lang="ts">
	import { slide } from "svelte/transition";
	import { ArrowRightIcon, CircleNotchIcon, EnvelopeIcon, WarningIcon } from "phosphor-svelte";

    import * as Alert from "$lib/components/ui/alert/index";
	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";

	import EmailVerification from "./EmailVerification.svelte";
	import { checkUniqueUsernameAuthCheckUniqueUsernameGet } from "$lib/api/auth/auth";


    let page: "username" | "verify" | "password" | "profile" | "passkey" | "success" = $state("username");

    const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    let username: string = $state("");
    let email: string = $state("");
    let emailVerified: boolean = $state(false);

    let checkingUsername: boolean = $state(false);
    let message: string = $state("");

    async function checkUsername() {
        checkingUsername = true;
        await checkUniqueUsernameAuthCheckUniqueUsernameGet({ username: username, email: email }).then((response) => {
            if (response.status == 200) {
                page = "verify";
                message = "";
            } else {
                message = response.data.message;
            }
        })
        checkingUsername = false;
    }

    $effect(() => {
        if (emailVerified) {
            page = "password";
        }
    })
</script>

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
        <div class="flex flex-row gap-2 items-center">
            <EnvelopeIcon weight="bold" />
            <p class="font-bold">First, choose a username and enter your email</p>
        </div>

        <Input placeholder="Username" type="text" bind:value={username} autofocus />
        <p class="text-sm text-muted-foreground">You will use your username to sign in. <br>It must be unique on this server. You can choose a display name later.</p>

        <Input placeholder="Email" type="email" bind:value={email} />
        <p class="text-sm text-muted-foreground">You can also use your email to sign in. <br>We will use this email to send you verification emails (if supported).</p>

        <Button onclick={() => {checkUsername()}} disabled={username.trim() == "" || !EMAIL_REGEX.test(email) || checkingUsername}>
            {#if checkingUsername}
                <CircleNotchIcon class="animate-spin" size={16} /> Checking...
            {:else}
                <ArrowRightIcon weight="bold" /> Next
            {/if}
        </Button>
    </div>
{:else if page == "verify"}
    <EmailVerification email={email} bind:verified={emailVerified} />

{:else if page == "password"}

{:else if page == "profile"}

{:else if page == "passkey"}

{:else if page == "success"}

{/if}