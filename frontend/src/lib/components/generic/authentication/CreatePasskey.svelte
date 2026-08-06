<!-- 
@component
Component used to create a user passkey, used by the universal authentication component

TODO: Improve request typing

Props:
    - `status` (`CreatePasskeyStatus`) - The state of the component. 
        Other components can bind to this status to know when this component can be hidden again
    - `email` (`string`) - The email to verify
    - `requireUserVerification` (`boolean`) - Whether to require user verification
-->
<script lang="ts" module>
    export type CreatePasskeyStatus = "idle" | "success" | "cancel";
</script>
<script lang="ts">
    import { startRegistration } from "@simplewebauthn/browser";

	import Button from "$lib/components/ui/button/button.svelte";
    import * as Alert from "$lib/components/ui/alert/index";
    import * as Kbd from "$lib/components/ui/kbd/index";

    import { createPasskeyAuthPasskeysRegisterCreatePost, verifyPasskeyAuthPasskeysRegisterVerifyPost } from "$lib/api/auth/auth";
	import { ArrowRightIcon, CheckCircleIcon, CircleNotchIcon, InfoIcon, KeyIcon, KeyReturnIcon, WarningIcon, XCircleIcon } from "phosphor-svelte";
	import { env } from "$env/dynamic/public";
	import Input from "$lib/components/ui/input/input.svelte";
	import AuthenticationMessage from "./AuthenticationMessage.svelte";
	import AuthenticationPage from "./AuthenticationPage.svelte";
	import type { VerifyUserStatus } from "./VerifyUser.svelte";
	import VerifyUser from "./VerifyUser.svelte";


    interface Props {
        status?: CreatePasskeyStatus
        email: string
        requireUserVerification?: boolean
    }
    let { status = $bindable("idle"), email, requireUserVerification = true }: Props = $props();

    let page: "create" | "verify" | "success" = $state("create");

    let message: string = $state("");
    let creatingPasskey: boolean = $state(false);
    let label: string = $state("");

    let verifyUserStatus: VerifyUserStatus = $state("idle");
    let verifyEmailVerficationCodeUuid: string | null = $state(null);
    let verifyPasskeyUuid: string | null = $state(null);

    function getRequireUserVerification() {
        if (+env.PUBLIC_PASSKEY_NO_VERIFICATION_MINUTES == -1) {
            return false;
        } else {
            return requireUserVerification;
        }
    }

    /**
     * Create a passkey
     */
    async function createPasskey() {
        creatingPasskey = true;
        try {
            let params;
            if (verifyEmailVerficationCodeUuid) {
                params = {
                    verification_code_uuid: verifyEmailVerficationCodeUuid,
                }
            } else if (verifyPasskeyUuid) {
                params = {
                    passkey_uuid: verifyPasskeyUuid
                }
            } else if (verifyEmailVerficationCodeUuid && verifyPasskeyUuid) {
                params = {
                    verification_code_uuid: verifyEmailVerficationCodeUuid,
                    passkey_uuid: verifyPasskeyUuid
                }
            }

            const options = await createPasskeyAuthPasskeysRegisterCreatePost(params).then((response) => {
                if (response.status != 200) {
                    message = response.data.detail;
                    throw new Error(message);
                } else {
                    return response;
                }
            });

            const registrationResponse = await startRegistration({
                optionsJSON: options.data,
            });
                        
            await verifyPasskeyAuthPasskeysRegisterVerifyPost(registrationResponse, {challenge_uuid: options.data.challenge_uuid, label}).then((response) => {
                if (response.status == 200) {
                    page = "success";
                } else {
                    message = "Failed to create passkey";
                }
            });
        } catch (error) {
            console.error(error);
            message = error.message
        }

        creatingPasskey = false;
    }

    /**
     * Handle keydown events
     */
    function handleKeyDown(event: KeyboardEvent) {
        if (event.key === "Enter" && page == "create" && !creatingPasskey && label.trim() != "") {
            if (getRequireUserVerification()) {
                page = "verify";
            } else if (!getRequireUserVerification()) {
                createPasskey();
            }
        } else if (event.key === "Enter" && page == "success") {
            status = "success";
        }
    }

    $effect(() => {
        if (verifyUserStatus == "success") {
            verifyUserStatus = "idle";
            createPasskey();
        } else if (verifyUserStatus == "cancel") {
            page = "create";
        }
    })
</script>

<svelte:window on:keydown={handleKeyDown} />

<AuthenticationMessage {message} />

{#if page == "create"}
    <AuthenticationPage title="Create a passkey?">
        {#snippet icon()}
            <KeyIcon weight="bold" />
        {/snippet}

        {#snippet content()}
            <p class="text-sm text-muted-foreground">Creating a passkey makes it quick and easy to log into your account.</p>

            {#if !env.PUBLIC_EMAIL_ENABLED}
                <Alert.Root variant="destructive" class="mb-2 text-left">
                    <WarningIcon weight="bold" />
                    <Alert.Title>Emails are disabled</Alert.Title>
                    <Alert.Description>If you loose your password, a passkey will be the only way to recover your account. We recommend creating a passkey now.</Alert.Description>
                </Alert.Root>
            {/if}

            {#if getRequireUserVerification()}
                <Alert.Root class="mb-2 text-left">
                    <InfoIcon weight="bold" />
                    <Alert.Title>Passkeys will need user verification</Alert.Title>
                    <Alert.Description>
                        {env.PUBLIC_PASSKEY_NO_VERIFICATION_MINUTES} minutes after your account creation, you will need user verification to create new passkeys. 
                        {#if !env.PUBLIC_EMAIL_ENABLED}
                            <br><span class="font-bold">Emails are disabled, so this passkey will be the only way to change your password later. Make sure to create one in the next {env.PUBLIC_PASSKEY_NO_VERIFICATION_MINUTES} minutes.</span> 
                        {/if}
                    </Alert.Description>
                </Alert.Root>
            {/if}

            <Input bind:value={label} placeholder="Label" />
            <p class="text-sm text-muted-foreground">The label of this passkey, to help identify it later</p>

            <Button onclick={() => {if (getRequireUserVerification()) {page = "verify"} else if (!getRequireUserVerification()) {createPasskey()}} } disabled={creatingPasskey || label.trim() == ""}>
                {#if creatingPasskey}
                    <CircleNotchIcon class="animate-spin" size={16} /> Creating Passkey...
                {:else}
                    <ArrowRightIcon weight="bold" /> Create <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
                {/if}
            </Button>
            <Button variant="outline" size="sm" onclick={() => {status = "cancel"}}><XCircleIcon weight="bold" /> Cancel</Button>
        {/snippet}
    </AuthenticationPage>

{:else if page == "verify"}
    <VerifyUser email={email} bind:status={verifyUserStatus} bind:emailVerificationCodeUuid={verifyEmailVerficationCodeUuid} bind:passkeyUuid={verifyPasskeyUuid} />

{:else if page == "success"}
    <AuthenticationPage title="Passkey created">
        {#snippet icon()}
            <CheckCircleIcon weight="bold" />
        {/snippet}

        {#snippet content()}
            <p class="text-muted-foreground">You have successfully created a passkey for your account.</p>
            <Button onclick={() => {status = "success"}}><CheckCircleIcon weight="bold" /> Continue <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root></Button>
        {/snippet}
    </AuthenticationPage>
{/if}