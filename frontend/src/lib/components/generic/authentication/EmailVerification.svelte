<!-- 
@component
Universal email verification component

Props:
    - `email` (`string`) - The email to verify
    - `verified` (`boolean`) - If the email has been verified
-->
<script lang="ts">
	import { slide } from "svelte/transition";
	import { PUBLIC_EMAIL_ENABLED } from "$env/static/public";
	import { ArrowRightIcon, EnvelopeIcon, QuestionIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
    import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";


    interface Props {
        email: string
        verified?: boolean
    }
    let { email, verified = $bindable(false) }: Props = $props();

    let page: "confirm_email" | "enter_code" | "success" = $state("confirm_email");
</script>

<div class="flex flex-col gap-2 text-left lg:max-w-[50vw]" transition:slide>
    {#if PUBLIC_EMAIL_ENABLED}
        {#if page == "confirm_email"}

        {:else if page == "enter_code"}

        {:else if page == "success"}

        {/if}

        <div class="flex flex-col gap-2 items-center">
            <p>Email verification is coming soon</p>
            <p>{email}</p>
            <Button class="flex-2" onclick={() => {verified = true}}><ArrowRightIcon weight="bold" /> Continue</Button>
        </div>
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
            <Button class="flex-2" onclick={() => {verified = true}}><ArrowRightIcon weight="bold" /> Continue</Button>
        </div>
    {/if}
</div>