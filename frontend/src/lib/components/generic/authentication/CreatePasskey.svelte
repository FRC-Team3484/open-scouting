<!-- 
@component
Component used to create a user passkey, used by the universal authentication component

TODO: Improve request typing

Props:
    - `status` (`CreatePasskeyStatus`) - The state of the component. 
        Other components can bind to this status to know when this component can be hidden again
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
	import { ArrowRightIcon, CheckCircleIcon, CircleNotchIcon, KeyIcon, KeyReturnIcon, WarningIcon, XCircleIcon } from "phosphor-svelte";
	import { PUBLIC_EMAIL_ENABLED } from "$env/static/public";
	import Input from "$lib/components/ui/input/input.svelte";
	import AuthenticationMessage from "./AuthenticationMessage.svelte";
	import AuthenticationPage from "./AuthenticationPage.svelte";


    interface Props {
        status?: CreatePasskeyStatus
    }
    let { status = $bindable("idle") }: Props = $props();

    let page: "create" | "success" = $state("create");

    let message: string = $state("");
    let creatingPasskey: boolean = $state(false);
    let label: string = $state("");

    /**
     * Create a passkey
     */
    async function createPasskey() {
        creatingPasskey = true;
        try {
            const options = await createPasskeyAuthPasskeysRegisterCreatePost();

            const registrationResponse = await startRegistration({
                optionsJSON: options.data,
            });
            
            registrationResponse.challenge_uuid = options.data.challenge_uuid;
            
            await verifyPasskeyAuthPasskeysRegisterVerifyPost(registrationResponse, {challenge_uuid: registrationResponse.challenge_uuid, label}).then((response) => {
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
            createPasskey();
        } else if (event.key === "Enter" && page == "success") {
            status = "success";
        }
    }
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

            <Input bind:value={label} placeholder="Label" />
            <p class="text-sm text-muted-foreground">The label of this passkey, to help identify it later</p>

            {#if !PUBLIC_EMAIL_ENABLED}
                <Alert.Root variant="destructive" class="mb-2 text-left">
                    <WarningIcon weight="bold" />
                    <Alert.Title>Emails are disabled</Alert.Title>
                    <Alert.Description>If you loose your password, a passkey will be the only way to recover your account. We recommend creating a passkey now.</Alert.Description>
                </Alert.Root>
            {/if}

            <Button onclick={() => {createPasskey()}} disabled={creatingPasskey || label.trim() == ""}>
                {#if creatingPasskey}
                    <CircleNotchIcon class="animate-spin" size={16} /> Creating Passkey...
                {:else}
                    <ArrowRightIcon weight="bold" /> Create <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
                {/if}
            </Button>
            <Button variant="outline" size="sm" onclick={() => {status = "cancel"}}><XCircleIcon weight="bold" /> Cancel</Button>
        {/snippet}
    </AuthenticationPage>

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