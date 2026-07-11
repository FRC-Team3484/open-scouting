<!-- 
@component
Part of the universal authentication component, for deleting accounts

Props:
    - `status` (`DeleteAccountStatus`) - The state of the component. 
        Other components can bind to this status to know when this component can be hidden again
-->
<script lang="ts" module>
    export type DeleteAccountStatus = "idle" | "success" | "cancel";
</script>
<script lang="ts">
	import { goto } from "$app/navigation";
	import { slide } from "svelte/transition";
	import { ArrowRightIcon, CheckCircleIcon, CircleNotchIcon, InfoIcon, KeyReturnIcon, TrashIcon, WarningIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card";
    import * as Avatar from "$lib/components/ui/avatar";
	import Input from "$lib/components/ui/input/input.svelte";
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Alert from "$lib/components/ui/alert";
	import Switch from "$lib/components/ui/switch/switch.svelte";
	import Label from "$lib/components/ui/label/label.svelte";
    import * as Kbd from "$lib/components/ui/kbd/index";

	import type { UserResponse } from "$lib/api/model";
	import { getUser, signOut } from "$lib/utils/user";
	import { deleteAccountAuthMeDeleteAccountDelete } from "$lib/api/auth/auth";
	import AuthenticationMessage from "./AuthenticationMessage.svelte";
	import AuthenticationPage from "./AuthenticationPage.svelte";
	import VerifyUser, { type VerifyUserStatus } from "./VerifyUser.svelte";


    interface Props {
        status?: DeleteAccountStatus
    }
    let { status = $bindable("idle") }: Props = $props();

    let page: "confirm" | "verify" | "delete" | "success" = $state("confirm");
    let message: string = $state("");
    let user: UserResponse | null = getUser();

    let username: string = $state("");
    let email: string = $state("");
    let deleteData: boolean = $state(false);

    let verifyUserStatus: VerifyUserStatus = $state("idle");
    let verifyEmailVerficationCodeUuid: string | null = $state(null);
    let verifyPasskeyUuid: string | null = $state(null);

    let deletingAccount: boolean = $state(false);
    
    /**
     * Delete the account
     */
    async function deleteAccount() {
        deletingAccount = true;

        await deleteAccountAuthMeDeleteAccountDelete({
            delete_data: deleteData,
            verification_code_uuid: verifyEmailVerficationCodeUuid,
            passkey_uuid: verifyPasskeyUuid
        }).then((response) => {
            if (response.status == 200) {
                page = "success";
            } else {
                message = "Failed to delete account.";
            }
        })

        deletingAccount = false;
    }

    /**
     * Log the user out, and return to the home page
     */
    async function logOut() {
        await signOut();
        await goto("/");
        status = "success";
    }

    /**
     * Handle enter key presses on this component
     * @param e
     */
    function handleKeyDown(e: KeyboardEvent) {
        if (e.key == "Enter") {
            if (page == "confirm" && username == user.username && email == user.email) {
                page = "verify"
            } else if (page == "success") {
                logOut();
            }
        }
    }

    $effect(() => {
        if (verifyUserStatus == "success") {
            page = "delete"
        } else if (verifyUserStatus == "cancel") {
            page = "confirm"
        }
    })
</script>

<svelte:window on:keydown={handleKeyDown} />

<AuthenticationMessage {message} />

{#if user}
    {#if page == "confirm" }
        <AuthenticationPage title="Delete Account" onCancelButtonClick={() => {status = "cancel"}}>
            {#snippet icon()}
                <TrashIcon weight="bold" />
            {/snippet}

            {#snippet content()}
                <Card.Root>
                    <Card.Content>
                        <div class="flex flex-row gap-2 items-center">
                            <Avatar.Root class="size-16">
                                <Avatar.Image src={user.profile_picture_url} alt={user.username} />
                                <Avatar.Fallback>{user.username.substring(0, 1)}</Avatar.Fallback>
                            </Avatar.Root>
                            <div class="flex flex-col gap-1 items-start">
                                <p>{user.display_name}</p>
                                {#if user.username != user.display_name}
                                    <p class="text-muted-foreground">({user.username})</p>
                                {/if}
                                <p class="text-muted-foreground">{user.email}</p>
                            </div>
                        </div>
                    </Card.Content>
                </Card.Root>

                <p class="font-bold">Are you sure you want to delete your account?</p>
                <p>This action cannot be undone.</p>
                <p class="text-muted-foreground">The following data will be permanently deleted:</p>

                <ul class="list-disc list-inside ml-4 text-muted-foreground">
                    <li>Your user account</li>
                    <li>Your profile information and settings</li>
                    <li>Passkeys for your account</li>
                </ul>

                <p class="text-muted-foreground">You can also choose to delete the following data you may have submitted:</p>

                <ul class="list-disc list-inside ml-4 text-muted-foreground mb-4">
                    <li>Match scouting submissions and answers</li>
                    <li>Pit scouting answers</li>
                </ul>

                <p class="text-muted-foreground">Some data will not be deleted:</p>

                <ul class="list-disc list-inside ml-4 text-muted-foreground mb-4">
                    <li>Pit scouting pits</li>
                    <li>Custom events</li>
                </ul>

                <p>Type profile details:</p>
                {#if username != user.username || email != user.email}
                    <div transition:slide>
                        <Alert.Root variant="destructive">
                            <WarningIcon weight="bold" />
                            <Alert.Title>Type your username and email</Alert.Title>
                            <Alert.Description>
                                Type your username ({user.username}) and email ({user.email}) to confirm that you want to delete your account.
                            </Alert.Description>
                        </Alert.Root>
                    </div>
                {/if}
                {#if deleteData}
                    <div transition:slide>
                        <Alert.Root>
                            <InfoIcon weight="bold" />
                            <Alert.Title>Delete Data</Alert.Title>
                            <Alert.Description>
                                You have chosen to delete optional data related to your account, like match and pit scouting data.
                            </Alert.Description>
                        </Alert.Root>

                        <Alert.Root>
                            <WarningIcon weight="bold" />
                            <Alert.Title>Some data may not be deleted</Alert.Title>
                            <Alert.Description>
                                <p>Data submitted prior to <span class="font-mono">v2.2.0</span> did not track who submitted it. This data will not be deleted.</p>
                            </Alert.Description>
                        </Alert.Root>
                    </div>
                {/if}

                <Input placeholder={user.username} bind:value={username} />
                <p class="text-muted-foreground">Type your username ({user.username})</p>

                <Input placeholder={user.email} bind:value={email} />
                <p class="text-muted-foreground">Type your email ({user.email})</p>

                <div class="flex flex-row gap-2 mb-4">
                    <Switch id="show-password" bind:checked={deleteData} />
                    <Label for="show-password">Delete Optional Data</Label>
                </div>

                <Button disabled={username != user.username || email != user.email} onclick={() => {page = "verify"}}><ArrowRightIcon weight="bold" /> Verify Identity <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root></Button>
            {/snippet}
        </AuthenticationPage>

    {:else if page == "verify"}
        <VerifyUser email={user.email} bind:status={verifyUserStatus} bind:emailVerificationCodeUuid={verifyEmailVerficationCodeUuid} bind:passkeyUuid={verifyPasskeyUuid}/>

    {:else if page == "delete"}
        <AuthenticationPage title="Are you really sure?" onBackButtonClick={() => {page = "confirm"}}>
            {#snippet icon()}
                <TrashIcon weight="bold" />
            {/snippet}

            {#snippet content()}
                <p class="font-bold">Are you sure you want to delete your account?</p>
                <p>By pressing the button below, you will permanently delete your account. This action cannot be undone.</p>
                {#if deleteData}
                    <p>You have also specfied to delete optional data related to your account, like match and pit scouting data you have submitted. These will also be immediately deleted.</p>
                {/if}

                <Button variant="destructive" onclick={() => {deleteAccount()}} disabled={deletingAccount}>
                    {#if deletingAccount}
                        <CircleNotchIcon class="animate-spin" weight="bold" />
                    {:else}
                        <TrashIcon weight="bold" /> Delete Account
                    {/if}
                </Button>
            {/snippet}
        </AuthenticationPage>
    {:else if page == "success"}
        <AuthenticationPage title="Account Deleted">
            {#snippet icon()}
                <CheckCircleIcon weight="bold" />
            {/snippet}

            {#snippet content()}
                <p class="text-muted-foreground">You have successfully deleted your account.</p>
                <Button onclick={() => {logOut()}}><CheckCircleIcon weight="bold" /> Home <Kbd.Root class="hidden pointer-fine:flex"><KeyReturnIcon weight="bold" /></Kbd.Root></Button>
            {/snippet}
        </AuthenticationPage>
    {/if}
{:else}
    <p class="text-muted-foreground">Failed to load user data.</p>
{/if}