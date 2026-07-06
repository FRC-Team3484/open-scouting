<!-- 
@component
Part of the universal authentication component, for resetting your password from the authentication page if forgotten

Users are asked to enter their email before being sent a verification code to that email, if their account exists. 
If emails are disabled on the server, instead prompt them to log in with a passkey. 

Props:
    - `status` (`ForgotPasswordStatus`) - The state of the component. 
        Other components can bind to this status to know when this component can be hidden again
-->
<script lang="ts" module>
    export type ForgotPasswordStatus = "idle" | "success" | "cancel";
</script>

<script lang="ts">
	import { PUBLIC_EMAIL_ENABLED } from "$env/static/public";
	import { onMount } from "svelte";
	import { slide } from "svelte/transition";
	import { toast } from "svelte-sonner";
	import { ArrowLeftIcon, ArrowRightIcon, CheckCircleIcon, CircleNotchIcon, EnvelopeIcon, KeyReturnIcon, PasswordIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
    import * as Kbd from "$lib/components/ui/kbd/index";

	import WhyAreEmailsDisabledDialog from "./WhyAreEmailsDisabledDialog.svelte";
	import { forgotPasswordAuthForgotPasswordPost } from "$lib/api/auth/auth";
	import EmailVerification, { type EmailVerificationStatus } from "./EmailVerification.svelte";
	import AuthenticationMessage from "./AuthenticationMessage.svelte";
	import AuthenticationPage from "./AuthenticationPage.svelte";
	import PasswordInput from "./PasswordInput.svelte";
    

    const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    interface Props {
        status?: ForgotPasswordStatus;
    }
    let { status = $bindable("idle") }: Props = $props();

    let page: "enter_email" | "verify" | "enter_new_password" | "success" = $state("enter_email");

    let message: string = $state("");

    let email = $state("");
    let password = $state("");
    let confirmPassword = $state("");
    let changingPassword = $state(false);

    let emailVerificationStatus: EmailVerificationStatus = $state("idle");
    let verificationCodeUuid = $state(null);

    /**
     * Change the user's password on the server
     */
    async function changePassword() {
        changingPassword = true;

        if (!verificationCodeUuid) {
            toast.error("No verification code uuid");
            changingPassword = false;
            return;
        }

        await forgotPasswordAuthForgotPasswordPost({email, password, verification_code_uuid: verificationCodeUuid}).then((response) => {
            if (response.status == 200) {
                page = "success";
                message = "";
            } else {
                message = response.data.message
                console.error(response.data.message);
            }
        })

        changingPassword = false;
    }

    /**
     * Handle the enter key on this component
     * 
     * @param e
     */
    function handleKeydown(e: KeyboardEvent) {
        if (e.key == "Enter") {
            if (page == "enter_email" && email.trim() != "" && EMAIL_REGEX.test(email)) {
                page = "verify";
            } else if (page == "enter_new_password" && password.trim() != "" && confirmPassword.trim() != "" && password == confirmPassword && !changingPassword) {
                changePassword();
            } else if (page == "success") {
                status = "success";
            }
        }
    }
    
    onMount(() => {
        status = "idle";
    });

    /**
     * Update the page when the email verification status changes
     */
    $effect(() => {
        if (emailVerificationStatus == "success") {
            page = "enter_new_password";
        } else if (emailVerificationStatus == "cancel" || emailVerificationStatus == "skipped") {
            page = "enter_email";
        }
    });
</script>

<svelte:window on:keydown={handleKeydown} />

<div class="flex flex-col gap-2 text-left lg:max-w-[50vw]" transition:slide>
    <AuthenticationMessage {message} />

    {#if PUBLIC_EMAIL_ENABLED}
        {#if page == "enter_email"}
            <AuthenticationPage title="Enter your email" onCancelButtonClick={() => {status = "cancel"}}>
                {#snippet icon()}
                    <EnvelopeIcon weight="bold" />
                {/snippet}

                {#snippet content()}
                    <p class="text-muted-foreground">Enter the email associated with the account you're trying to reset the password for</p>

                    <Input type="email" placeholder="Email" bind:value={email} autofocus />
                    <p class="text-sm text-muted-foreground">A verification code will be sent to this email</p>

                    <Button onclick={() => page = "verify"} disabled={email.trim() == "" || !EMAIL_REGEX.test(email)}>
                        <ArrowRightIcon weight="bold" /> Send Verification Code <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
                    </Button>
                {/snippet}
            </AuthenticationPage>

        {:else if page == "verify"}
            <EmailVerification email={email} bind:status={emailVerificationStatus} bind:verificationCodeUuid={verificationCodeUuid} skippable={false} />

        {:else if page == "enter_new_password"}
            <AuthenticationPage title="Enter new password" onBackButtonClick={() => {page = "enter_email"}}>
                {#snippet icon()}
                    <PasswordIcon weight="bold" />
                {/snippet}

                {#snippet content()}
                    <p class="text-muted-foreground">Enter your new password</p>

                    <PasswordInput bind:password bind:confirmPassword />

                    <Button onclick={() => {changePassword()}} disabled={password.trim() == "" || confirmPassword.trim() == "" || password != confirmPassword}>
                        {#if changingPassword}
                            <CircleNotchIcon class="animate-spin" size={16} /> Changing...
                        {:else}
                            <ArrowRightIcon weight="bold" /> Change Password <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
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
                    <p class="text-muted-foreground">Your password has been changed. Continue to the sign in page to log in with your new password.</p>

                    <Button onclick={() => {status = "success"}}>
                        <ArrowRightIcon weight="bold" /> Continue <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
                    </Button>
                {/snippet}
            </AuthenticationPage>

        {/if}
    {:else}
        <AuthenticationPage title="Unable to change password here">
            {#snippet icon()}
                <EnvelopeIcon weight="bold" />
            {/snippet}

            {#snippet content()}
                <p class="text-muted-foreground font-bold">Emails are disabled on this server.</p>
                <p class="text-muted-foreground">We cannot send you a code to verify your identity before changing your password.</p>
                <p class="text-muted-foreground">If you have a passkey for Open Scouting, use that to log in, then change your password on your profile page.</p>

                <div class="flex flex-row gap-2 w-full">
                    <WhyAreEmailsDisabledDialog />
                    <Button class="flex-2" onclick={() => {status = "cancel"}}><ArrowLeftIcon weight="bold" /> Back</Button>
                </div>
            {/snippet}
        </AuthenticationPage>
    {/if}
</div>