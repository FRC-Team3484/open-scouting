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

Props:
    - `ref` (`string`) - The ref to redirect to after creating the account
-->
<script lang="ts">
	import { ArrowRightIcon, CircleNotchIcon, EnvelopeIcon, KeyIcon, KeyReturnIcon, UserCircleIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
    import * as Kbd from "$lib/components/ui/kbd/index";

	import EmailVerification, { type EmailVerificationStatus } from "./EmailVerification.svelte";
	import SignInConfirmation from "./SignInConfirmation.svelte";
	import { checkUniqueUsernameAuthCheckUniqueUsernameGet, meAuthMeGet, signupAuthSignupPost } from "$lib/api/auth/auth";
	import type { SignupRequest, UserResponse } from "$lib/api/model";
	import CreatePasskey, { type CreatePasskeyStatus } from "./CreatePasskey.svelte";
	import AuthenticationMessage from "./AuthenticationMessage.svelte";
	import AuthenticationPage from "./AuthenticationPage.svelte";
	import PasswordInput from "./PasswordInput.svelte";
	import { goto } from "$app/navigation";


    interface Props {
        ref?: string
    }
    let { ref = "/" }: Props = $props();

    let page: "username" | "verify" | "password" | "profile" | "passkey" | "success" = $state("username");

    const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    let username: string = $state("");
    let email: string = $state("");
    let emailVerificationStatus: EmailVerificationStatus = $state("idle");
    let emailVerified = $state(false);
    let password: string = $state("");
    let confirmPassword: string = $state("");
    let displayName: string = $state("");
    let teamNumber: number = $state(0);
    let verificationCodeUuid: string | null = $state(null);

    let checkingUsername: boolean = $state(false);
    let creatingAccount: boolean = $state(false);
    let message: string = $state("");

    let successUser: UserResponse | null = $state(null);
    let createPasskeyStatus: CreatePasskeyStatus = $state("idle");

    /**
     * Check the user's username and email on the server to ensure they're unique
     */
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

    /**
     * Create the user account on the server, and log them in
     * 
     * Get the user's information from the server, and pass it into the `SignInConfirmation` component
     */
    async function createAccount() {
        creatingAccount = true;
        const data: SignupRequest = {
            username: username,
            email: email,
            password: password,
            confirm_password: confirmPassword,
            team_number: teamNumber,
            display_name: displayName,
            verification_code_uuid: verificationCodeUuid
        }
        
        await signupAuthSignupPost(data).then(async (response) => {
            if (response.status == 200) {

                await meAuthMeGet().then((response) => {
                    if (response.status == 200) {
                        successUser = response.data.user;
                    }
                });
                page = "passkey";
            } else {
                message = response.data.message;
            }
        })
        creatingAccount = false;
    }

    /**
     * Handle the enter key on this page
     * 
     * @param e
     */
    function handleKeyDown(e: KeyboardEvent) {
        if (e.key == "Enter") {
            if (page == "username" && username.trim() != "" && !EMAIL_REGEX.test(username) && !checkingUsername) {
                checkUsername();
            } else if (page == "password" && password.trim() != "" && confirmPassword.trim() != "" && password == confirmPassword) {
                page = "profile";
            } else if (page == "profile" && displayName.trim() != "" && teamNumber != 0 && !creatingAccount) {
                createAccount();
            } else if (page == "success") {
                goto(ref);
            }
        }
    }

    /**
     * Listen to the `verified` prop of the `EmailVerification` component. If it is true, the user can proceed
     */
    $effect(() => {
        if (emailVerificationStatus == "success") {
            page = "password";
            emailVerified = true;
        } else if (emailVerificationStatus == "skipped") {
            page = "password";
            emailVerified = false;
        } else if (emailVerificationStatus == "cancel") {
            page = "username";
            emailVerified = false;
        }

        if (createPasskeyStatus == "success" || createPasskeyStatus == "cancel") {
            page = "success";
        }
    })
</script>

<svelte:window on:keydown={handleKeyDown} />

<AuthenticationMessage {message} />

{#if page == "username"}
    <AuthenticationPage title="Choose a username and enter your email">
        {#snippet icon()}
            <EnvelopeIcon weight="bold" />
        {/snippet}

        {#snippet content()}
            <Input placeholder="Username" type="text" bind:value={username} autofocus />
            <p class="text-sm text-muted-foreground">You will use your username to sign in. <br>It must be unique on this server. You can choose a display name later.</p>

            <Input placeholder="Email" type="email" bind:value={email} />
            <p class="text-sm text-muted-foreground">You can also use your email to sign in. <br>We will use this email to send you verification emails (if supported).</p>

            <Button onclick={() => {checkUsername()}} disabled={username.trim() == "" || !EMAIL_REGEX.test(email) || checkingUsername}>
                {#if checkingUsername}
                    <CircleNotchIcon class="animate-spin" size={16} /> Checking...
                {:else}
                    <ArrowRightIcon weight="bold" /> Next <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
                {/if}
            </Button>
        {/snippet}
    </AuthenticationPage>

{:else if page == "verify"}
    <EmailVerification email={email} bind:status={emailVerificationStatus} bind:verificationCodeUuid={verificationCodeUuid} />

{:else if page == "password"}
    <AuthenticationPage title="Choose a password" onBackButtonClick={() => {page = "username"}}>
        {#snippet icon()}
            <KeyIcon weight="bold" />
        {/snippet}

        {#snippet content()}
            <PasswordInput bind:password bind:confirmPassword />

            <Button onclick={() => {page = "profile"}} disabled={password.trim() == "" || confirmPassword.trim() == "" || password != confirmPassword}>
                <ArrowRightIcon weight="bold" /> Next <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
            </Button>
        {/snippet}
    </AuthenticationPage>

{:else if page == "profile"}
    <AuthenticationPage title="Profile Details" onBackButtonClick={() => {page = "password"}}>
        {#snippet icon()}
            <UserCircleIcon weight="bold" />
        {/snippet}

        {#snippet content()}
            <Input placeholder="Display name" type="text" bind:value={displayName} defaultValue={username} />
            <p class="text-sm text-muted-foreground">This is the name that will be displayed in place of your username.</p>

            <Input placeholder="Team Number" type="text" bind:value={teamNumber} />
            <p class="text-sm text-muted-foreground">The team number for the team you are a part of.</p>

            <Button onclick={() => {createAccount()}} disabled={displayName.trim() == "" || teamNumber == 0 || creatingAccount}>
                {#if creatingAccount}
                    <CircleNotchIcon class="animate-spin" size={16} /> Creating Account...
                {:else}
                    <ArrowRightIcon weight="bold" /> Create Account <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
                {/if}
            </Button>
        {/snippet}
    </AuthenticationPage>

{:else if page == "passkey"}
    <CreatePasskey email={email} bind:status={createPasskeyStatus} requireUserVerification={false} />

{:else if page == "success"}
    <SignInConfirmation user={successUser} redirect={5} ref={ref} />

{/if}