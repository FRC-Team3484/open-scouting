<!-- 
@component
Universal email verification component

TODO: Skip button
TODO: back buttons

Props:
    - `email` (`string`) - The email to verify
    - `status` (`EmailVerificationStatus`) - The state of the component. 
        Other components can bind to this status to know when this component can be hidden again
-->
<script lang="ts" module>
    export type EmailVerificationStatus = "idle" | "success" | "cancel" | "skipped";
</script>

<script lang="ts">
	import { slide } from "svelte/transition";
	import { PUBLIC_EMAIL_ENABLED } from "$env/static/public";
	import { ArrowRightIcon, CheckCircleIcon, CircleNotchIcon, EnvelopeIcon, FastForwardCircleIcon, FastForwardIcon, QuestionIcon, TrashIcon, WarningIcon, XCircleIcon } from "phosphor-svelte";
	import { toast } from "svelte-sonner";

	import Button from "$lib/components/ui/button/button.svelte";
    import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
    import * as Alert from "$lib/components/ui/alert/index.js";
    import * as InputOTP from "$lib/components/ui/input-otp/index.js";
	import { REGEXP_ONLY_DIGITS } from "bits-ui";

	import { createVerificationCodeAuthCreateVerificationCodePost, verifyVerificationCodeAuthVerifyVerificationCodePost } from "$lib/api/auth/auth";


    interface Props {
        email: string
        status?: EmailVerificationStatus
    }
    let { email, status = $bindable("idle") }: Props = $props();

    let page: "confirm_email" | "enter_code" | "success" = $state("confirm_email");
    let message: string = $state("");

    let sendingCode: boolean = $state(false);
    let code: string = $state("");
    let checkingCode: boolean = $state(false);

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

    async function checkVerificationCode() {
        checkingCode = true;
        await verifyVerificationCodeAuthVerifyVerificationCodePost({email, code}).then((response) => {
            if (response.status == 200) {
                page = "success";
                message = "";
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
        {#if page == "confirm_email"}
            <div class="flex flex-col gap-2 text-left" transition:slide>

                <div class="flex flex-row gap-2 items-center">
                    <EnvelopeIcon weight="bold" />
                    <p class="font-bold">Verify your email</p>
                </div>
                <p class="text-muted-foreground">We will send a verification code to</p>

                <p class="font-bold">{email}</p>
                <p class="text-muted-foreground">Enter the code in the next step to verify your email</p>
                <Button onclick={() => sendVerificationCode()} disabled={sendingCode}>
                    {#if sendingCode}
                        <CircleNotchIcon class="animate-spin" size={16} /> Sending...
                    {:else}
                        <ArrowRightIcon weight="bold" /> Send Code
                    {/if}
                </Button>
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
                <Button variant="ghost" onclick={() => {status = "cancel"}} disabled={sendingCode}><XCircleIcon weight="bold" /> Cancel</Button>
            </div>

        {:else if page == "enter_code"}
            <div class="flex flex-col gap-2 text-left" transition:slide>
                <div class="flex flex-row gap-2 items-center">
                    <EnvelopeIcon weight="bold" />
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
                <Button onclick={() => {sendVerificationCode(true)}} variant="outline" disabled={checkingCode}>
                    {#if sendingCode}
                        <CircleNotchIcon class="animate-spin" size={16} /> Sending...
                    {:else}
                        <EnvelopeIcon weight="bold" /> Resend Code
                    {/if}
                </Button>
                <Button variant="ghost" onclick={() => {status = "cancel"}} disabled={sendingCode}><XCircleIcon weight="bold" /> Cancel</Button>
            </div>

        {:else if page == "success"}
            <div class="flex flex-col gap-2 text-left" transition:slide>
                <div class="flex flex-row gap-2 items-center">
                    <CheckCircleIcon weight="bold" />
                    <p class="font-bold">Verify your email</p>
                </div>
                <p class="text-muted-foreground">You have successfully verified your email!</p>
                <Button onclick={() => {status = "success"}}>Continue</Button>
            </div>
        {/if}
    {:else}
        <div class="flex flex-row gap-2 items-center">
            <EnvelopeIcon weight="bold" size={32} />
            <p class="font-bold text-lg">Emails are not enabled on this server</p>
        </div>
        <p>We are not able to verify your email at this time. If emails are enabled on this server later, you will be able to verify your email on your profile page.</p>
        <p>With an unverified email, you will not be able to use the "Forgot Password" feature. You will still be able to change your password by accessing your account using a passkey.</p>
        <p class="font-bold">Consider creating a passkey in the next steps.</p>

        <div class="flex flex-row gap-2 w-full">
            <AlertDialog.Root>
                <AlertDialog.Trigger>
                    <Button variant="outline"><QuestionIcon weight="bold" /> Why am I seeing this?</Button>
                </AlertDialog.Trigger>
                <AlertDialog.Content>
                    <AlertDialog.Title>Why am I seeing this?</AlertDialog.Title>
            
                    <AlertDialog.Description>
                        <p>Having a reliable way to send emails to users, and getting them to deliver without being marked as spam costs money.</p>
                        <p>There are some free tier options, but they are not always reliable, and will stop working after enough emails are sent in a month.</p>
                        <p>Due to budget constraints, we are keeping Open Scouting's hosting costs as low as possible.</p>
                        <p>You may also be seeing this in the offseason, when we are not paying for emails due to low usage.</p>
                    </AlertDialog.Description>
                    <AlertDialog.Footer>
                        <AlertDialog.Cancel type="button">Close</AlertDialog.Cancel>
                    </AlertDialog.Footer>
                </AlertDialog.Content>
            </AlertDialog.Root>
            <Button class="flex-2" onclick={() => {status = "skipped"}}><ArrowRightIcon weight="bold" /> Continue</Button>
        </div>
    {/if}
</div>