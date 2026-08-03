<!-- 
@component
Uses the VerifyUser component to verify user authentication, then changes the user's password

Props:
    - `email` (`string`) - The email to verify
    - `status` (`ChangePasswordStatus`) - The state of the component. 
        Other components can bind to this status to know when this component can be hidden again
-->
<script lang="ts" module>
    export type ChangePasswordStatus = "idle" | "success" | "cancel";
</script>
<script lang="ts">
	import { ArrowRightIcon, CheckCircleIcon, CircleNotchIcon, KeyReturnIcon, PasswordIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
    import * as Kbd from "$lib/components/ui/kbd/index";

	import VerifyUser, { type VerifyUserStatus } from "./VerifyUser.svelte";
	import { changePasswordAuthChangePasswordPost } from "$lib/api/auth/auth";
	import AuthenticationMessage from "./AuthenticationMessage.svelte";
	import AuthenticationPage from "./AuthenticationPage.svelte";
	import PasswordInput from "./PasswordInput.svelte";


    interface Props {
        email: string
        status?: ChangePasswordStatus
    }
    let { email, status = $bindable("idle") }: Props = $props();

    let page: "verify" | "change" | "success" = $state("verify");
    let message: string = $state("");

    let verifyUserStatus: VerifyUserStatus = $state("idle");
    let verifyEmailVerficationCodeUuid: string | null = $state(null);
    let verifyPasskeyUuid: string | null = $state(null);

    let password: string = $state("");
    let confirmPassword: string = $state("");
    let changingPassword: boolean = $state(false);

    /**
     * Change the user's password
     */
    async function changePassword() {
        changingPassword = true;

        await changePasswordAuthChangePasswordPost({
            password: password,
            verification_code_uuid: verifyEmailVerficationCodeUuid,
            passkey_uuid: verifyPasskeyUuid
        }).then((response) => {
            if (response.status == 200) {
                page = "success";
            }
        })

        changingPassword = false;
    }

    /**
     * Handle the enter key on this component
     * @param e
     */
    function handleKeyDown(e: KeyboardEvent) {
        if (e.key == "Enter") {
            if (page == "change" && password.trim() != "" && confirmPassword.trim() != "" && password == confirmPassword) {
                changePassword();
            } else if (page == "success") {
                status = "success";
            }
        }
    }

    $effect(() => {
        if (verifyUserStatus == "success") {
            page = "change";
        } else if (verifyUserStatus == "cancel") {
            status = "cancel";
        }
    })
</script>

<svelte:window on:keydown={handleKeyDown}/>

<AuthenticationMessage {message} />

{#if page == "verify"}
    <VerifyUser email={email} bind:status={verifyUserStatus} bind:emailVerificationCodeUuid={verifyEmailVerficationCodeUuid} bind:passkeyUuid={verifyPasskeyUuid}/>
{:else if page == "change"}
    <AuthenticationPage title="Enter your new password">
        {#snippet icon()}
            <PasswordIcon weight="bold" />
        {/snippet}

        {#snippet content()}
            <PasswordInput bind:password bind:confirmPassword />

            <Button onclick={() => {changePassword()}} disabled={password.trim() == "" || confirmPassword.trim() == "" || password != confirmPassword}>
                {#if changingPassword}
                    <CircleNotchIcon class="animate-spin" size={16} /> Changing...
                {:else}
                    <ArrowRightIcon weight="bold" /> Change <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
                {/if}
            </Button>
        {/snippet}
    </AuthenticationPage>

{:else if page == "success"}
    <AuthenticationPage title="Password Changed">
        {#snippet icon()}
            <CheckCircleIcon weight="bold" />
        {/snippet}

        {#snippet content()}
            <p class="text-muted-foreground">You have successfully changed your password.</p>
            <Button onclick={() => {status = "success"}}><CheckCircleIcon weight="bold" /> Continue <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root></Button>
        {/snippet}
    </AuthenticationPage>
{/if}