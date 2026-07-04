<!-- 
@component
Universal authentication component, supporting the following features:
- Creating an account, verifying their email (if enabled), and creating a passkey
- Signing in to an account, with both password and a passkey
- Changing a password, given a passkey
- Changing a password, given a email verification code (if enabled)
- Verifying an unverified email
- Changing an email, and verifying it
- Creating a passkey

This plugin takes a mode prop, which defines it's operation where the component is used
Additional props optionally take data depending on the mode

Props:
    - `mode` (`create_account | sign_in | change_password | forgot_password | verify_email | change_email | create_passkey`) - The current authentication mode
    - `email` (`string`) - The email to verify (if `mode` is `verify_email`)
    - `emailVerificationStatus` (`EmailVerificationStatus`) - The state of the `EmailVerification` component (if `mode` is `verify_email`)
    - `forgotPasswordStatus` (`ForgotPasswordStatus`) - The state of the `ForgotPassword` component (if `mode` is `forgot_password`)
-->
<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";

	import type { UserResponse } from "$lib/api/model";
	import { getUser } from "$lib/utils/user";
	import AuthenticationModeHeader from "./AuthenticationModeHeader.svelte";
	import { EnvelopeIcon, FingerprintIcon, KeyIcon, UserCircleIcon, UserCirclePlusIcon } from "phosphor-svelte";
	import SignIn from "./SignIn.svelte";
	import CreateAccount from "./CreateAccount.svelte";
	import EmailVerification, { type EmailVerificationStatus } from "./EmailVerification.svelte";
	import ForgotPassword, { type ForgotPasswordStatus } from "./ForgotPassword.svelte";
	import CreatePasskey from "./CreatePasskey.svelte";


    interface BaseProps {
        mode: "create_account" | "sign_in" | "change_password" | "forgot_password" | "verify_email" | "change_email" | "create_passkey"
        email?: never
        emailVerificationStatus?: never
        forgotPasswordStatus?: never
    }
    interface VerifyEmailProps {
        mode: "verify_email"
        email: string
        emailVerificationStatus: EmailVerificationStatus
        forgotPasswordStatus?: never
    }
    interface ForgotPasswordProps {
        mode: "forgot_password"
        email?: never
        emailVerificationStatus?: never
        forgotPasswordStatus: ForgotPasswordStatus
    }
    let { mode, email, emailVerificationStatus = $bindable(), forgotPasswordStatus = $bindable() }: BaseProps | VerifyEmailProps | ForgotPasswordProps = $props();

    let user: UserResponse | null = getUser();
</script>

<Card.Root>
    <Card.Content>
        {#if mode === "create_account"}
            <AuthenticationModeHeader title="Create Account" description="Create a new Open Scouting account">
                <UserCirclePlusIcon weight="bold" size={32} />
            </AuthenticationModeHeader>

            <CreateAccount />

        {:else if mode === "sign_in"}
            <AuthenticationModeHeader title="Sign In" description="Sign in to your Open Scouting account">
                <UserCircleIcon weight="bold" size={32} />
            </AuthenticationModeHeader>

            <SignIn />

        {:else if mode === "change_password"}
            <AuthenticationModeHeader title="Change Password" description="Change your password">
                <KeyIcon weight="bold" size={32} />
            </AuthenticationModeHeader>

        {:else if mode === "forgot_password"}
            <AuthenticationModeHeader title="Forgot Password" description="Reset your password">
                <KeyIcon weight="bold" size={32} />
            </AuthenticationModeHeader>

            <ForgotPassword bind:status={forgotPasswordStatus} />

        {:else if mode === "verify_email"}
            <AuthenticationModeHeader title="Verify Email" description="Verify your email">
                <EnvelopeIcon weight="bold" size={32} />
            </AuthenticationModeHeader>

            {#if email}
                <EmailVerification email={email} bind:status={emailVerificationStatus} />
            {/if}

        {:else if mode === "change_email"}
            <AuthenticationModeHeader title="Change Email" description="Change your email">
                <EnvelopeIcon weight="bold" size={32} />
            </AuthenticationModeHeader>

        {:else if mode === "create_passkey"}
            <AuthenticationModeHeader title="Create Passkey" description="Create a new passkey">
                <FingerprintIcon weight="bold" size={32} />
            </AuthenticationModeHeader>

            <CreatePasskey />
        {/if}
    </Card.Content>
</Card.Root>