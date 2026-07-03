<!-- 
@component
Part of the universal authentication component, for resetting your password from the authentication page if forgotten

Users are asked to enter their email before being sent a verification code to that email, if their account exists. 
If emails are disabled on the server, instead prompt them to log in with a passkey. 

TODO: Support keyboard navigation
TODO: Can this use the EmailVerification component instead?

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
	import { ArrowLeftIcon, ArrowRightIcon, CheckCircleIcon, CircleNotchIcon, ClockIcon, EnvelopeIcon, EnvelopeOpenIcon, PasswordIcon, TrashIcon, WarningIcon, XCircleIcon } from "phosphor-svelte";

    import * as Alert from "$lib/components/ui/alert";
	import Button from "$lib/components/ui/button/button.svelte";
	import WhyAreEmailsDisabledDialog from "./WhyAreEmailsDisabledDialog.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
    import * as InputOTP from "$lib/components/ui/input-otp/index.js";
	import { REGEXP_ONLY_DIGITS } from "bits-ui";
	import Switch from "$lib/components/ui/switch/switch.svelte";
	import Label from "$lib/components/ui/label/label.svelte";
	import { createVerificationCodeAuthCreateVerificationCodePost, forgotPasswordAuthForgotPasswordPost, verifyVerificationCodeAuthVerifyVerificationCodePost } from "$lib/api/auth/auth";
	import { toast } from "svelte-sonner";
    

    const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    interface Props {
        status?: ForgotPasswordStatus;
    }
    let { status = $bindable("idle") }: Props = $props();

    let page: "enter_email" | "enter_code" | "enter_new_password" | "success" = $state("enter_email");
    let resendCountdown: number = $state(30);
    let resendInterval: any = null;
    let message: string = $state("");

    let email = $state("");
    let sendingVerificationCode = $state(false);
    let code = $state("");
    let checkingCode = $state(false);
    let password = $state("");
    let confirmPassword = $state("");
    let showPassword = $state(false);
    let changingPassword = $state(false);
    let verificationCodeUuid = $state(null);

    /**
     * Send a verification code to the user
     * 
     * Creates a resend interval, for when the user can send another code
     * 
     * @param resend If true, show a message that the code has been resent
     */
    async function sendVerificationCode(resend = false) {
        sendingVerificationCode = true;
        await createVerificationCodeAuthCreateVerificationCodePost({email, style: "forgot_password"}).then((response) => {
            if (response.status == 200) {
                if (resend) {
                    toast.success("Code resent");
                    message = "";
                } else {
                    page = "enter_code";
                    message = "";
                }

                if (resendInterval) {
                    clearInterval(resendInterval);
                    resendCountdown = 30;
                }
                resendInterval = setInterval(() => {
                    resendCountdown = resendCountdown - 1;
                    if (resendCountdown == 0) {
                        clearInterval(resendInterval);
                    }
                }, 1000);
            } else {
                message = response.data.message
                console.error(response.data.message);
            }
        }).catch((error) => {
            message = error.message
            console.error(error);
        });
        sendingVerificationCode = false;
    }

    /**
     * Check if the verification code is correct on the server
     */
    async function checkVerificationCode() {
        checkingCode = true;
        await verifyVerificationCodeAuthVerifyVerificationCodePost({email, code}).then((response) => {
            if (response.status == 200) {
                page = "enter_new_password";
                message = "";
                verificationCodeUuid = response.data.verification_code_uuid;
            } else {
                message = response.data.message
                console.error(response.data.message);
            }
        }).catch((error) => {
            message = error.message
            console.error(error);
        });
        checkingCode = false;
    }

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

    onMount(() => {
        status = "idle";

        return () => {
            clearInterval(resendInterval);
        }
    })
</script>

<div class="flex flex-col gap-2 text-left lg:max-w-[50vw]" transition:slide>
    {#if message}
        <Alert.Root variant="destructive" class="mb-2">
            <WarningIcon weight="bold" />
            <Alert.Title>There was a problem</Alert.Title>
            <Alert.Description>{message}</Alert.Description>
        </Alert.Root>
    {/if}

    {#if PUBLIC_EMAIL_ENABLED}
        {#if page == "enter_email"}
            <div class="flex flex-col gap-2 text-left" transition:slide>
                <Button variant="outline" size="sm" onclick={() => {status = "cancel"}} class="w-fit" disabled={sendingVerificationCode}><XCircleIcon weight="bold" /> Cancel</Button>
                <div class="flex flex-row gap-2 items-center">
                    <EnvelopeIcon weight="bold" />
                    <p class="font-bold">Enter your email</p>
                </div>
                <p class="text-muted-foreground">Enter the email associated with the account you're trying to reset the password for</p>

                <Input type="email" placeholder="Email" bind:value={email} autofocus />
                <p class="text-sm text-muted-foreground">A verification code will be sent to this email</p>

                <Button onclick={() => sendVerificationCode()} disabled={sendingVerificationCode || email.trim() == "" || !EMAIL_REGEX.test(email)}>
                    {#if sendingVerificationCode}
                        <CircleNotchIcon class="animate-spin" size={16} /> Sending...
                    {:else}
                        <ArrowRightIcon weight="bold" /> Send Verification Code
                    {/if}
                </Button>

            </div>
        {:else if page == "enter_code"}
            <div class="flex flex-col gap-2 text-left" transition:slide>
                <Button variant="outline" size="sm" onclick={() => {page = "enter_email"}} class="w-fit"><ArrowLeftIcon weight="bold" /> Back</Button>
                <div class="flex flex-row gap-2 items-center">
                    <EnvelopeOpenIcon weight="bold" />
                    <p class="font-bold">Verification code sent</p>
                </div>
                <p class="text-muted-foreground">A verification code has been sent to <span class="font-bold">{email}</span></p>
                <p class="text-muted-foreground">Enter the code below to verify your email</p>

                <div class="flex flex-row items-center w-full justify-center gap-2">
                    <InputOTP.Root maxlength={6} pattern={REGEXP_ONLY_DIGITS} class="my-4" bind:value={code}>
                        {#snippet children({ cells })}
                            <InputOTP.Group>
                            {#each cells as cell (cell)}
                                <InputOTP.Slot {cell} />
                            {/each}
                            </InputOTP.Group>
                        {/snippet}
                    </InputOTP.Root>
                    <Button variant="outline" size="icon" onclick={() => code = ""} disabled={!code.length}><TrashIcon weight="bold" /></Button>
                </div>
                <Button onclick={() => {checkVerificationCode()}} disabled={code.length != 6 || checkingCode}>
                    {#if checkingCode}
                        <CircleNotchIcon class="animate-spin" size={16} /> Checking...
                    {:else}
                        <ArrowRightIcon weight="bold" /> Verify
                    {/if}
                </Button>
                <Button onclick={() => {sendVerificationCode(true)}} variant="outline" disabled={checkingCode || resendCountdown > 0}>
                    {#if sendingVerificationCode}
                        <CircleNotchIcon class="animate-spin" size={16} /> Sending...
                    {:else}
                        {#if resendCountdown > 0}
                            <ClockIcon weight="bold" /> Resend Code ({resendCountdown}s)
                        {:else}
                            <EnvelopeIcon weight="bold" /> Resend Code
                        {/if}
                    {/if}
                </Button>
            </div>
        {:else if page == "enter_new_password"}
            <div class="flex flex-col gap-2 text-left" transition:slide>
                <Button variant="outline" size="sm" onclick={() => {page = "enter_email"}} class="w-fit"><ArrowLeftIcon weight="bold" /> Back</Button>
                <div class="flex flex-row gap-2 items-center">
                    <PasswordIcon weight="bold" />
                    <p class="font-bold">Enter new password</p>
                </div>
                <p class="text-muted-foreground">Enter your new password</p>

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
                        <ArrowRightIcon weight="bold" /> Change Password
                    {/if}
                </Button>

            </div>
        {:else if page == "success"}
            <div class="flex flex-col gap-2 text-left" transition:slide>
                <div class="flex flex-row gap-2 items-center">
                    <CheckCircleIcon weight="bold" />
                    <p class="font-bold">Password Changed</p>
                </div>
                <p class="text-muted-foreground">Your password has been changed. Continue to the sign in page to log in with your new password.</p>

                <Button onclick={() => {status = "success"}}><ArrowRightIcon weight="bold" /> Continue</Button>
            </div>
        {/if}
    {:else}
        <div class="flex flex-row gap-2 items-center">
            <EnvelopeIcon weight="bold" />
            <p class="font-bold">Unable to change password here</p>
        </div>
        <p class="text-muted-foreground font-bold">Emails are disabled on this server.</p>
        <p class="text-muted-foreground">We cannot send you a code to verify your identity before changing your password.</p>
        <p class="text-muted-foreground">If you have a passkey for Open Scouting, use that to log in, then change your password on your profile page.</p>

        <div class="flex flex-row gap-2 w-full">
            <WhyAreEmailsDisabledDialog />
            <Button class="flex-2" onclick={() => {status = "cancel"}}><ArrowLeftIcon weight="bold" /> Back</Button>
        </div>
    {/if}
</div>