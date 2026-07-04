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

    import { createLoginPasskeyAuthPasskeysLoginCreatePost, createPasskeyAuthPasskeysRegisterCreatePost, verifyLoginPasskeyAuthPasskeysLoginVerifyPost, verifyPasskeyAuthPasskeysRegisterVerifyPost } from "$lib/api/auth/auth";
	import { slide } from "svelte/transition";
	import { ArrowRightIcon, CheckCircleIcon, CircleNotchIcon, KeyIcon, KeyReturnIcon, WarningIcon, XCircleIcon } from "phosphor-svelte";
	import { PUBLIC_EMAIL_ENABLED } from "$env/static/public";


    interface Props {
        status?: CreatePasskeyStatus
    }
    let { status = $bindable("idle") }: Props = $props();

    let page: "create" | "success" = $state("create");

    let message: string = $state("");
    let creatingPasskey: boolean = $state(false);

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
            
            await verifyPasskeyAuthPasskeysRegisterVerifyPost(registrationResponse, {challenge_uuid: registrationResponse.challenge_uuid}).then((response) => {
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
        if (event.key === "Enter" && page == "create") {
            createPasskey();
        } else if (event.key === "Enter" && page == "success") {
            status = "success";
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

{#if page == "create"}
    <div class="flex flex-col gap-2 text-left" transition:slide>
        <div class="flex flex-row gap-2 items-center">
            <KeyIcon weight="bold" />
            <p class="font-bold">Create a passkey?</p>
        </div>

        <p class="text-sm text-muted-foreground">Creating a passkey makes it quick and easy to log into your account.</p>

        {#if !PUBLIC_EMAIL_ENABLED}
            <Alert.Root variant="destructive" class="mb-2 text-left">
                <WarningIcon weight="bold" />
                <Alert.Title>Emails are disabled</Alert.Title>
                <Alert.Description>If you loose your password, a passkey will be the only way to recover your account. We recommend creating a passkey now.</Alert.Description>
            </Alert.Root>
        {/if}


        <Button onclick={() => {createPasskey()}} disabled={creatingPasskey}>
            {#if creatingPasskey}
                <CircleNotchIcon class="animate-spin" size={16} /> Creating Passkey...
            {:else}
                <ArrowRightIcon weight="bold" /> Create <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
            {/if}
        </Button>
        <Button variant="outline" size="sm" onclick={() => {status = "cancel"}}><XCircleIcon weight="bold" /> Cancel</Button>
    </div>

{:else if page == "success"}
    <div class="flex flex-col gap-2 text-left" transition:slide>
        <div class="flex flex-row gap-2 items-center">
            <CheckCircleIcon weight="bold" />
            <p class="font-bold">Passkey created</p>
        </div>

        <p>You've successfully created a passkey for your account</p>

        <Button onclick={() => {status = "success"}}><ArrowRightIcon weight="bold" /> Continue <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root></Button>
    </div>
{/if}