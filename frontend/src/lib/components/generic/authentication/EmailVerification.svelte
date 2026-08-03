<!-- 
@component
Universal email verification component

Props:
    - `email` (`string`) - The email to verify
    - `status` (`EmailVerificationStatus`) - The state of the component. 
        Other components can bind to this status to know when this component can be hidden again
    - `verificationCodeUuid` (`string | null`) - The uuid of the verified verification code
    - `skippable` (`boolean`) - Whether to show the skip button
-->
<script lang="ts" module>
    export type EmailVerificationStatus = "idle" | "success" | "cancel" | "skipped";
</script>

<script lang="ts">
	import { onMount } from "svelte";
	import { slide } from "svelte/transition";
	import { PUBLIC_EMAIL_ENABLED } from "$env/static/public";
	import { ArrowRightIcon, CheckCircleIcon, CircleNotchIcon, ClockIcon, EnvelopeIcon, FastForwardCircleIcon, FastForwardIcon, KeyReturnIcon, QuestionIcon, TrashIcon, WarningIcon, XCircleIcon } from "phosphor-svelte";
	import { toast } from "svelte-sonner";

	import Button from "$lib/components/ui/button/button.svelte";
    import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
    import * as Alert from "$lib/components/ui/alert/index.js";
    import * as InputOTP from "$lib/components/ui/input-otp/index.js";
    import * as Kbd from "$lib/components/ui/kbd/index.js";
	import { REGEXP_ONLY_DIGITS } from "bits-ui";

	import { createVerificationCodeAuthCreateVerificationCodePost, verifyVerificationCodeAuthVerifyVerificationCodePost } from "$lib/api/auth/auth";
	import WhyAreEmailsDisabledDialog from "./WhyAreEmailsDisabledDialog.svelte";
	import AuthenticationMessage from "./AuthenticationMessage.svelte";
	import AuthenticationPage from "./AuthenticationPage.svelte";


    interface Props {
        email: string
        status?: EmailVerificationStatus
        verificationCodeUuid?: string | null
        skippable? : boolean
    }
    let { email, status = $bindable("idle"), verificationCodeUuid = $bindable(null), skippable = true }: Props = $props();

    let page: "confirm_email" | "enter_code" | "success" = $state("confirm_email");
    let resendCountdown: number = $state(30);
    let resendInterval: any = null;
    let message: string = $state("");

    let sendingCode: boolean = $state(false);
    let code: string = $state("");
    let checkingCode: boolean = $state(false);

    /**
     * Send a verification code to the user
     * 
     * Creates a resend interval, for when the user can send another code
     * 
     * @param resend If true, show a message that the code has been resent
     */
    async function sendVerificationCode(resend = false) {
        sendingCode = true;
        await createVerificationCodeAuthCreateVerificationCodePost({email}).then((response) => {
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
        sendingCode = false;
    }

    /**
     * Check if the verification code is correct on the server
     */
    async function checkVerificationCode() {
        checkingCode = true;
        await verifyVerificationCodeAuthVerifyVerificationCodePost({email, code}).then((response) => {
            if (response.status == 200) {
                page = "success";
                message = "";
                verificationCodeUuid = response.data.verification_code_uuid ?? null;
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
     * Handle the enter key on this component
     * 
     * @param e
     */
    function handleKeydown(e: KeyboardEvent) {
        if (e.key == "Enter") {
            if (page == "confirm_email" && !sendingCode) {
                sendVerificationCode();
            } else if (page == "enter_code" && code.length == 6 && !checkingCode) {
                checkVerificationCode();
            } else if (page == "success") {
                status = "success";
            }
        }
    }

    onMount(() => {
        status = "idle";

        return () => {
            clearInterval(resendInterval);
        }
    });
</script>

<svelte:window on:keydown={handleKeydown} />

<div class="flex flex-col gap-2 text-left lg:max-w-[50vw]" transition:slide>
    <AuthenticationMessage {message} />

    {#if PUBLIC_EMAIL_ENABLED}
        {#if page == "confirm_email"}
            <AuthenticationPage title="Verify your email" onCancelButtonClick={() => {status = "cancel"}}>
                {#snippet icon()}
                    <EnvelopeIcon weight="bold" />
                {/snippet}

                {#snippet content()}
                    <p class="text-muted-foreground">We will send a verification code to</p>

                    <p class="font-bold">{email}</p>
                    <p class="text-muted-foreground">Enter the code in the next step to verify your email</p>
                    <Button onclick={() => sendVerificationCode()} disabled={sendingCode}>
                        {#if sendingCode}
                            <CircleNotchIcon class="animate-spin" size={16} /> Sending...
                        {:else}
                            <ArrowRightIcon weight="bold" /> Send Code <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
                        {/if}
                    </Button>
                    {#if skippable}
                        <AlertDialog.Root>
                            <AlertDialog.Trigger>
                                <Button onclick={() => {}} variant="outline" disabled={sendingCode} class="w-full"><FastForwardCircleIcon weight="bold" /> Skip</Button>
                            </AlertDialog.Trigger>
                            <AlertDialog.Content>
                                <AlertDialog.Title>Skip Email Verification</AlertDialog.Title>
                                <AlertDialog.Description>
                                    <p>Are you sure you want to skip email verification?</p>
                                    <p>Without a verified email, you will not be able to use the "Forgot Password" feature to recover your account.</p>
                                    <p>You will still be able to change your password by accessing your account using a passkey.</p>
                                </AlertDialog.Description>
                                <AlertDialog.Footer>
                                    <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                    <AlertDialog.Action type="button" onclick={() => {status = "skipped"}}>Skip</AlertDialog.Action>
                                </AlertDialog.Footer>
                            </AlertDialog.Content>
                        </AlertDialog.Root>
                    {/if}
                {/snippet}
            </AuthenticationPage>

        {:else if page == "enter_code"}
            <AuthenticationPage title="Verification code sent" onCancelButtonClick={() => {status = "cancel"}}>
                {#snippet icon()}
                    <EnvelopeIcon weight="bold" />
                {/snippet}

                {#snippet content()}
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
                            <ArrowRightIcon weight="bold" /> Verify <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
                        {/if}
                    </Button>
                    <Button onclick={() => {sendVerificationCode(true)}} variant="outline" disabled={checkingCode || resendCountdown > 0}>
                        {#if sendingCode}
                            <CircleNotchIcon class="animate-spin" size={16} /> Sending...
                        {:else}
                            {#if resendCountdown > 0}
                                <ClockIcon weight="bold" /> Resend Code ({resendCountdown}s)
                            {:else}
                                <EnvelopeIcon weight="bold" /> Resend Code <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root>
                            {/if}
                        {/if}
                    </Button>
                {/snippet}
            </AuthenticationPage>

        {:else if page == "success"}
            <AuthenticationPage title="Email Verified">
                {#snippet icon()}
                    <CheckCircleIcon weight="bold" />
                {/snippet}

                {#snippet content()}
                    <p class="text-muted-foreground">You have successfully verified your email: <span class="font-bold">{email}</span></p>
                    <Button onclick={() => {status = "success"}}><CheckCircleIcon weight="bold" /> Continue <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root></Button>
                {/snippet}
            </AuthenticationPage>
        {/if}
    {:else}
        <AuthenticationPage title="Emails are not enabled on this server">
            {#snippet icon()}
                <EnvelopeIcon weight="bold" />
            {/snippet}

            {#snippet content()}
                <p class="text-muted-foreground">We are not able to verify your email at this time. If emails are enabled on this server later, you will be able to verify your email on your profile page.</p>
                <p class="text-muted-foreground">With an unverified email, you will not be able to use the "Forgot Password" feature. You will still be able to change your password by accessing your account using a passkey.</p>
                <p class="text-muted-foreground font-bold">Consider creating a passkey in the next steps.</p>

                <div class="flex flex-row gap-2 w-full">
                    <WhyAreEmailsDisabledDialog />
                    <Button class="flex-2" onclick={() => {status = "skipped"}}><ArrowRightIcon weight="bold" /> Continue</Button>
                </div>
            {/snippet}
        </AuthenticationPage>
    {/if}
</div>