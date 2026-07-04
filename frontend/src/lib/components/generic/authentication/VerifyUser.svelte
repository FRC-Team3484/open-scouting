<!-- 
@component
Used by other components in the universal authentication component to verify the user's identity, with either email or passkey verification.

Props:
    - `email` (`string`) - The email to verify
    - `status` (`VerifyUserStatus`) - The state of the component. 
        Other components can bind to this status to know when this component can be hidden again
    - `emailVerificationCodeUuid` (`string | null`) - The uuid of the verified verification code
        This can be used to perform backend verification of the information
    - `passkeyUuid` (`string | null`) - The uuid of the verified passkey
        This can be used to perform backend verification of the information
-->
<script lang="ts" module>
    export type VerifyUserStatus = "idle" | "success" | "cancel";
</script>
<script lang="ts">
	import { slide } from "svelte/transition";
	import { startAuthentication } from "@simplewebauthn/browser";
	import { CheckCircleIcon, CircleNotchIcon, EnvelopeIcon, KeyIcon, KeyReturnIcon, UserCircleCheckIcon, UserCircleIcon, WarningIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
    import * as Alert from "$lib/components/ui/alert/index";
    import * as Kbd from "$lib/components/ui/kbd/index";

	import EmailVerification, { type EmailVerificationStatus } from "./EmailVerification.svelte";
	import { createVerificationPasskeyAuthPasskeysVerificationCreatePost, verifyVerificationPasskeyAuthPasskeysVerificationVerifyPost } from "$lib/api/auth/auth";


    interface Props {
        email: string
        status?: VerifyUserStatus
        emailVerificationCodeUuid?: string | null
        passkeyUuid?: string | null
    }
    let { email, status = $bindable("idle"), emailVerificationCodeUuid = $bindable(null), passkeyUuid = $bindable(null) }: Props = $props();

    let page: "start" | "email" | "success" = $state("start");
    let message: string = $state("");

    let emailVerificationStatus: EmailVerificationStatus = $state("idle");

    let verifyingWithPasskey: boolean = $state(false);

    /**
     * Login with a passkey
     */
    async function verifyWithPasskey() {
        message = "";
        verifyingWithPasskey = true;
        try {
            const options = await createVerificationPasskeyAuthPasskeysVerificationCreatePost({ email: email });

            const authenticationResponse = await startAuthentication({
                optionsJSON: options.data,
            });

            await verifyVerificationPasskeyAuthPasskeysVerificationVerifyPost(authenticationResponse, {challenge_uuid: options.data.challenge_uuid, email: email}).then(async (response) => {
                if (response.status == 200) {
                    passkeyUuid = response.data.uuid;
                    page = "success";
                } else {
                    message = "Failed to verify with passkey";
                    page = "start";
                }
            });
        } catch (error) {
            console.error(error);
            message = error.message
        }

        verifyingWithPasskey = false;
    }

    /**
     * Handle keydowns on this component
     * @param e
     */
    function handleKeyDown(e) {
        if (e.key == "Enter") {
            if (page == "start") {
                verifyWithPasskey();
            } else if (page == "success") {
                status = "success";
            }
        }
    }

    $effect(() => {
        if (emailVerificationStatus == "success") {
            page = "success";
        } else if (emailVerificationStatus == "cancel") {
            page = "start";
            message = "Email verification was cancelled.";
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

{#if page == "start"}
    <div class="flex flex-col gap-2 text-left" transition:slide>
        <div class="flex flex-row gap-2 items-center">
            <UserCircleIcon weight="bold" />
            <p class="font-bold">Verify Identity</p>
        </div>

        <p class="text-sm text-muted-foreground">We need to verify your identity.</p>
        <p class="text-sm text-muted-foreground">Please choose a verification method. Email verification may not be supported on this server.</p>

        <Button onclick={() => {verifyWithPasskey()}} disabled={verifyingWithPasskey}>
            {#if verifyingWithPasskey}
                <CircleNotchIcon class="animate-spin" size={16} /> Verifying...
            {:else}
                <KeyIcon weight="bold" /> Verify with Passkey
            {/if}
            <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
        </Button>
        <Button onclick={() => {page = "email"}} disabled={verifyingWithPasskey}><EnvelopeIcon weight="bold" /> Send Verification Email</Button>
    </div>

{:else if page == "email"}
    <EmailVerification email={email} bind:status={emailVerificationStatus} bind:verificationCodeUuid={emailVerificationCodeUuid} skippable={false} />

{:else if page == "success"}
    <div class="flex flex-col gap-2 text-left" transition:slide>
        <div class="flex flex-row gap-2 items-center">
            <UserCircleCheckIcon weight="bold" />
            <p class="font-bold">Identity Verified</p>
        </div>

        <p class="text-sm text-muted-foreground">You have successfully verified your identity.</p>
        <Button onclick={() => {status = "success"}}><CheckCircleIcon weight="bold" /> Continue <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root></Button>
    </div>
{/if}