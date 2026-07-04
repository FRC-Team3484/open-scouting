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

TODO: Support passkeys
-->
<script lang="ts">
	import { slide } from "svelte/transition";
	import { ArrowLeftIcon, ArrowRightIcon, CircleNotchIcon, EnvelopeIcon, KeyIcon, KeyReturnIcon, UserCircleIcon, WarningIcon } from "phosphor-svelte";

    import * as Alert from "$lib/components/ui/alert/index";
	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
	import Switch from "$lib/components/ui/switch/switch.svelte";
	import Label from "$lib/components/ui/label/label.svelte";
    import * as Kbd from "$lib/components/ui/kbd/index";

	import EmailVerification, { type EmailVerificationStatus } from "./EmailVerification.svelte";
	import SignInConfirmation from "./SignInConfirmation.svelte";
	import { checkUniqueUsernameAuthCheckUniqueUsernameGet, meAuthMeGet, signupAuthSignupPost } from "$lib/api/auth/auth";
	import type { SignupRequest, UserResponse } from "$lib/api/model";
	import CreatePasskey, { type CreatePasskeyStatus } from "./CreatePasskey.svelte";


    let page: "username" | "verify" | "password" | "profile" | "passkey" | "success" = $state("username");

    const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    let username: string = $state("");
    let email: string = $state("");
    let emailVerificationStatus: EmailVerificationStatus = $state("idle");
    let emailVerified = $state(false);
    let password: string = $state("");
    let confirmPassword: string = $state("");
    let showPassword: boolean = $state(false);
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
                <ArrowRightIcon weight="bold" /> Next <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
            {/if}
        </Button>
    </div>
{:else if page == "verify"}
    <EmailVerification email={email} bind:status={emailVerificationStatus} bind:verificationCodeUuid={verificationCodeUuid} />

{:else if page == "password"}
    <div class="flex flex-col gap-2 text-left" transition:slide>
        <Button variant="outline" size="sm" onclick={() => {page = "username"}} class="w-fit"><ArrowLeftIcon weight="bold" /> Back</Button>
        <div class="flex flex-row gap-2 items-center">
            <KeyIcon weight="bold" />
            <p class="font-bold">Choose a password</p>
        </div>

        <p class="text-sm text-muted-foreground mb-2">
            Strong passwords are 16+ characters long, and have a mix <br>
            of uppercase and lowercase letters, numbers, and special <br>
            characters. Consider using a passphrase, and don't use the <br>
            same password for multiple websites.
        </p>

        <Input placeholder="Password" type={showPassword ? "text" : "password"} bind:value={password} autofocus />
        <p class="text-sm text-muted-foreground">The password to use when logging into your account</p>

        <Input placeholder="Confirm password" type={showPassword ? "text" : "password"} bind:value={confirmPassword} />
        <p class="text-sm text-muted-foreground">Confirm your password</p>

        <div class="flex flex-row gap-2 mb-4">
            <Switch id="show-password" bind:checked={showPassword} />
            <Label for="show-password">Show Password</Label>
        </div>

        {#if confirmPassword != password}
            <div transition:slide>
                <Alert.Root variant="destructive" class="mb-2 text-left">
                    <WarningIcon weight="bold" />
                    <Alert.Title>Passwords do not match</Alert.Title>
                </Alert.Root>
            </div>
        {/if}

        <Button onclick={() => {page = "profile"}} disabled={password.trim() == "" || confirmPassword.trim() == "" || password != confirmPassword}>
            <ArrowRightIcon weight="bold" /> Next <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
        </Button>
    </div>

{:else if page == "profile"}
    <div class="flex flex-col gap-2 text-left" transition:slide>
        <Button variant="outline" size="sm" onclick={() => {page = "password"}} class="w-fit"><ArrowLeftIcon weight="bold" /> Back</Button>
        <div class="flex flex-row gap-2 items-center">
            <UserCircleIcon weight="bold" />
            <p class="font-bold">Profile Details</p>
        </div>

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
    </div>

{:else if page == "passkey"}
    <CreatePasskey bind:status={createPasskeyStatus} />
{:else if page == "success"}
    <SignInConfirmation user={successUser} redirect={5} />
{/if}