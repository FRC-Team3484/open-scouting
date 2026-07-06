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
	import { slide } from "svelte/transition";
	import { ArrowRightIcon, CheckCircleIcon, CircleNotchIcon, KeyReturnIcon, PasswordIcon, WarningIcon } from "phosphor-svelte";

	import Input from "$lib/components/ui/input/input.svelte";
	import Switch from "$lib/components/ui/switch/switch.svelte";
	import Label from "$lib/components/ui/label/label.svelte";
    import * as Alert from "$lib/components/ui/alert/index";
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Kbd from "$lib/components/ui/kbd/index";

	import VerifyUser, { type VerifyUserStatus } from "./VerifyUser.svelte";
	import { changePasswordAuthChangePasswordPost } from "$lib/api/auth/auth";
	import AuthenticationMessage from "./AuthenticationMessage.svelte";
	import AuthenticationPage from "./AuthenticationPage.svelte";


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
    let showPassword: boolean = $state(false);
    let changingPassword: boolean = $state(false);

    /**
     * Change the user's password
     */
    async function changePassword() {
        changingPassword = true;

        console.log(verifyEmailVerficationCodeUuid, verifyPasskeyUuid);

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
    <div class="flex flex-col gap-2 text-left" transition:slide>
        <div class="flex flex-row gap-2 items-center">
            <PasswordIcon weight="bold" />
            <p class="font-bold">Enter your new password</p>
        </div>
        
        
    </div>

    <AuthenticationPage title="Enter your new password">
        {#snippet icon()}
            <PasswordIcon weight="bold" />
        {/snippet}

        {#snippet content()}
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