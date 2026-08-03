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
    - `mode` (`create_account | sign_in | change_password | forgot_password | verify_email | change_email | create_passkey | delete_account`) - The current authentication mode
    - `email` (`string`) - The email to verify (if `mode` is `verify_email`, `change_password`, `change_email`, or `create_passkey`)
    - `emailVerificationStatus` (`EmailVerificationStatus`) - The state of the `EmailVerification` component (if `mode` is `verify_email`)
    - `forgotPasswordStatus` (`ForgotPasswordStatus`) - The state of the `ForgotPassword` component (if `mode` is `forgot_password`)
    - `changePasswordStatus` (`ChangePasswordStatus`) - The state of the `ChangePassword` component (if `mode` is `change_password`)
    - `changeEmailStatus` (`ChangeEmailStatus`) - The state of the `ChangeEmail` component (if `mode` is `change_email`)
    - `createPasskeyStatus` (`CreatePasskeyStatus`) - The state of the `CreatePasskey` component (if `mode` is `create_passkey`)
    - `createPasskeyRequireUserVerification` (`boolean`) - Whether to require user verification (if `mode` is `create_passkey`)
    - `deleteAccountStatus` (`DeleteAccountStatus`) - The state of the `DeleteAccount` component (if `mode` is `delete_account`)
-->
<script lang="ts">
	import { EnvelopeIcon, FingerprintIcon, KeyIcon, TrashIcon, UserCircleIcon, UserCirclePlusIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";

	import AuthenticationModeHeader from "./AuthenticationModeHeader.svelte";
	import SignIn from "./SignIn.svelte";
	import CreateAccount from "./CreateAccount.svelte";
	import EmailVerification, { type EmailVerificationStatus } from "./EmailVerification.svelte";
	import ForgotPassword, { type ForgotPasswordStatus } from "./ForgotPassword.svelte";
	import CreatePasskey, { type CreatePasskeyStatus } from "./CreatePasskey.svelte";
	import type { ChangePasswordStatus } from "./ChangePassword.svelte";
	import ChangePassword from "./ChangePassword.svelte";
	import type { ChangeEmailStatus } from "./ChangeEmail.svelte";
	import ChangeEmail from "./ChangeEmail.svelte";
	import type { DeleteAccountStatus } from "./DeleteAccount.svelte";
	import DeleteAccount from "./DeleteAccount.svelte";


    interface BaseProps {
        mode: "create_account" | "sign_in" | "change_password" | "forgot_password" | "verify_email" | "change_email" | "create_passkey" | "delete_account"
        email?: never
        ref?: never
        emailVerificationStatus?: never
        forgotPasswordStatus?: never
        changePasswordStatus?: never
        changeEmailStatus?: never
        createPasskeyStatus?: never
        createPasskeyRequireUserVerification?: never
        deleteAccountStatus?: never
    }
    interface CreateAccountProps {
        mode: "create_account"
        email?: never
        ref?: string
        emailVerificationStatus?: never
        forgotPasswordStatus?: never
        changePasswordStatus?: never
        changeEmailStatus?: never
        createPasskeyStatus?: never
        createPasskeyRequireUserVerification?: never
        deleteAccountStatus?: never
    }
    interface SignInProps {
        mode: "sign_in"
        email?: never
        ref?: string
        emailVerificationStatus?: never
        forgotPasswordStatus?: never
        changePasswordStatus?: never
        changeEmailStatus?: never
        createPasskeyStatus?: never
        createPasskeyRequireUserVerification?: never
        deleteAccountStatus?: never
    }
    interface VerifyEmailProps {
        mode: "verify_email"
        email: string
        ref?: never
        emailVerificationStatus?: EmailVerificationStatus
        forgotPasswordStatus?: never
        changePasswordStatus?: never
        changeEmailStatus?: never
        createPasskeyStatus?: never
        createPasskeyRequireUserVerification?: never
        deleteAccountStatus?: never
    }
    interface ForgotPasswordProps {
        mode: "forgot_password"
        email?: never
        ref?: never
        emailVerificationStatus?: never
        forgotPasswordStatus?: ForgotPasswordStatus
        changePasswordStatus?: never
        changeEmailStatus?: never
        createPasskeyStatus?: never
        createPasskeyRequireUserVerification?: never
        deleteAccountStatus?: never
    }
    interface ChangePasswordProps {
        mode: "change_password"
        email: string
        ref?: never
        emailVerificationStatus?: never
        forgotPasswordStatus?: never
        changePasswordStatus?: ChangePasswordStatus
        changeEmailStatus?: never
        createPasskeyStatus?: never
        createPasskeyRequireUserVerification?: never
        deleteAccountStatus?: never
    }
    interface ChangeEmailProps {
        mode: "change_email"
        email: string
        ref?: never
        emailVerificationStatus?: never
        forgotPasswordStatus?: never
        changePasswordStatus?: never
        changeEmailStatus?: ChangeEmailStatus
        createPasskeyStatus?: never
        createPasskeyRequireUserVerification?: never
        deleteAccountStatus?: never
    }
    interface CreatePasskeyProps {
        mode: "create_passkey"
        email: string
        ref?: never
        emailVerificationStatus?: never
        forgotPasswordStatus?: never
        changePasswordStatus?: never
        changeEmailStatus?: never
        createPasskeyStatus?: CreatePasskeyStatus
        createPasskeyRequireUserVerification?: boolean
        deleteAccountStatus?: never
    }
    interface DeleteAccountProps {
        mode: "delete_account"
        email?: never
        ref?: never
        emailVerificationStatus?: never
        forgotPasswordStatus?: never
        changePasswordStatus?: never
        changeEmailStatus?: never
        createPasskeyStatus?: never
        createPasskeyRequireUserVerification?: never
        deleteAccountStatus?: DeleteAccountStatus
    }
    let { mode, email, ref, emailVerificationStatus = $bindable(), forgotPasswordStatus = $bindable(), changePasswordStatus = $bindable(), changeEmailStatus = $bindable(), createPasskeyStatus = $bindable(), createPasskeyRequireUserVerification, deleteAccountStatus = $bindable() }: BaseProps | CreateAccountProps | SignInProps | VerifyEmailProps | ForgotPasswordProps | ChangePasswordProps | ChangeEmailProps | CreatePasskeyProps | DeleteAccountProps = $props();
</script>

<Card.Root>
    <Card.Content>
        {#if mode === "create_account"}
            <AuthenticationModeHeader title="Create Account" description="Create a new Open Scouting account">
                <UserCirclePlusIcon weight="bold" size={32} />
            </AuthenticationModeHeader>

            <CreateAccount ref={ref} />

        {:else if mode === "sign_in"}
            <AuthenticationModeHeader title="Sign In" description="Sign in to your Open Scouting account">
                <UserCircleIcon weight="bold" size={32} />
            </AuthenticationModeHeader>

            <SignIn ref={ref} />

        {:else if mode === "change_password"}
            <AuthenticationModeHeader title="Change Password" description="Change your password">
                <KeyIcon weight="bold" size={32} />
            </AuthenticationModeHeader>

            {#if email}
                <ChangePassword email={email} bind:status={changePasswordStatus} />
            {/if}

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

            {#if email}
                <ChangeEmail email={email} bind:status={changeEmailStatus} />
            {/if}

        {:else if mode === "create_passkey"}
            <AuthenticationModeHeader title="Create Passkey" description="Create a new passkey">
                <FingerprintIcon weight="bold" size={32} />
            </AuthenticationModeHeader>

            {#if email}
                <CreatePasskey email={email} bind:status={createPasskeyStatus} requireUserVerification={createPasskeyRequireUserVerification} />
            {/if}

        {:else if mode === "delete_account"}
            <AuthenticationModeHeader title="Delete Account" description="Delete your account">
                <TrashIcon weight="bold" size={32} />
            </AuthenticationModeHeader>

            <DeleteAccount bind:status={deleteAccountStatus} />
        {/if}
    </Card.Content>
</Card.Root>