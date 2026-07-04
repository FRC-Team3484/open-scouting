<!-- 
@component
Uses the VerifyUser component to verify user authentication, then changes the user's email

Props:
    - `email` (`string`) - The email to verify
    - `status` (`ChangeEmailStatus`) - The state of the component. 
        Other components can bind to this status to know when this component can be hidden again
-->
<script lang="ts" module>
    export type ChangeEmailStatus = "idle" | "success" | "cancel";
</script>
<script lang="ts">
	import { slide } from "svelte/transition";
	import { ArrowRightIcon, CheckCircleIcon, CircleNotchIcon, EnvelopeIcon, KeyReturnIcon, WarningIcon } from "phosphor-svelte";

    import * as Alert from "$lib/components/ui/alert/index";
	import Input from "$lib/components/ui/input/input.svelte";
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Kbd from "$lib/components/ui/kbd/index";

	import type { VerifyUserStatus } from "./VerifyUser.svelte";
	import VerifyUser from "./VerifyUser.svelte";
	import { changeEmailAuthChangeEmailPost, checkUniqueUsernameAuthCheckUniqueUsernameGet } from "$lib/api/auth/auth";
	import EmailVerification, { type EmailVerificationStatus } from "./EmailVerification.svelte";
	import { PUBLIC_EMAIL_ENABLED } from "$env/static/public";


    interface Props {
        email: string
        status?: ChangeEmailStatus
    }
    let { email, status = $bindable("idle") }: Props = $props();

    const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    let page: "verify" | "change" | "verify_new_email" | "success" = $state("verify");
    let message: string = $state("");

    let verifyUserStatus: VerifyUserStatus = $state("idle");
    let verifyEmailVerficationCodeUuid: string | null = $state(null);
    let verifyPasskeyUuid: string | null = $state(null);

    let newEmail: string = $state("");
    let checkingEmail: boolean = $state(false);

    let verifyEmailStatus: EmailVerificationStatus = $state("idle");

    /**
     * Check that the new email is unique
     */
    async function checkUniqueEmail() {
        checkingEmail = true;
        await checkUniqueUsernameAuthCheckUniqueUsernameGet({email: newEmail}).then(async (response) => {
            if (response.status == 200) {
                await changeEmail();

            } else {
                message = "Email already in use";
            }
        })

        checkingEmail = false;
    }

    /**
     * Change the user's email
     */
    async function changeEmail() {
        await changeEmailAuthChangeEmailPost({email: newEmail, verification_code_uuid: verifyEmailVerficationCodeUuid, passkey_uuid: verifyPasskeyUuid}).then((response) => {
            if (response.status == 200) {
                if (PUBLIC_EMAIL_ENABLED) {
                    page = "verify_new_email";
                } else {
                    page = "success";
                }
            } else {
                message = "Failed to change email";
            }
        })
    }
    

    /**
     * Handle the enter key on this component
     * @param e
     */
    function handleKeyDown(e: KeyboardEvent) {
        if (e.key === "Enter") {
            if (page == "change" && EMAIL_REGEX.test(newEmail) && !checkingEmail) {
                checkUniqueEmail();
            } else if (page == "success") {
                status = "success";
            }
        }
    }

    $effect(() => {
        if (verifyUserStatus == "success") {
            page = "change";
        }

        if (verifyEmailStatus == "success") {
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

{#if page == "verify"}
    <VerifyUser email={email} bind:status={verifyUserStatus} bind:emailVerificationCodeUuid={verifyEmailVerficationCodeUuid} bind:passkeyUuid={verifyPasskeyUuid}/>
{:else if page == "change"}
    <div class="flex flex-col gap-2 text-left" transition:slide>
        <div class="flex flex-row gap-2 items-center">
            <EnvelopeIcon weight="bold" />
            <p class="font-bold">Enter your new email</p>
        </div>

        <Input placeholder="Email" type="email" bind:value={newEmail} />
        <p class="text-sm text-muted-foreground">You can also use your email to sign in. <br>We will use this email to send you verification emails (if supported).</p>

        <Button onclick={() => {checkUniqueEmail()}} disabled={!EMAIL_REGEX.test(newEmail) || checkingEmail}>
            {#if checkingEmail}
                <CircleNotchIcon class="animate-spin" size={16} /> Checking...
            {:else}
                <ArrowRightIcon weight="bold" /> Next <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
            {/if}
        </Button>
    </div>
{:else if page == "verify_new_email"}
    <EmailVerification email={newEmail} bind:status={verifyEmailStatus} skippable={false} />

{:else if page == "success"}
    <div class="flex flex-col gap-2 text-left" transition:slide>
        <div class="flex flex-row gap-2 items-center">
            <CheckCircleIcon weight="bold" />
            <p class="font-bold">Email Changed</p>
        </div>
        <p class="text-muted-foreground">You have successfully changed your email.</p>
        <Button onclick={() => {status = "success"}}><CheckCircleIcon weight="bold" /> Continue <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root></Button>
    </div>
{/if}