<!-- 
@component
The profile section on the profile page, for editing user details

Props:
    - `user` (`UserResponse`) - The user
    - `getNewUserData` (`() => void`) - A function to get the new user
-->
<script lang="ts">
	import { PUBLIC_EMAIL_ENABLED, PUBLIC_PASSKEY_NO_VERIFICATION_MINUTES } from "$env/static/public";
    import { onMount } from "svelte";
	import { toast } from "svelte-sonner";
	import { ArrowRightIcon, CheckCircleIcon, CircleNotchIcon, EnvelopeIcon, InfoIcon, KeyIcon, PasswordIcon, PencilIcon, TrashIcon, UploadSimpleIcon, WarningIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";
	import { Badge } from "$lib/components/ui/badge";
    import * as Alert from "$lib/components/ui/alert";
	import Separator from "$lib/components/ui/separator/separator.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Avatar from "$lib/components/ui/avatar/index.js";
    import * as AlertDialog from "$lib/components/ui/alert-dialog";

	import Section from "./BaseSection.svelte";
	import type { PasskeyResponse, UserResponse } from "$lib/api/model";
	import { deletePasskeyAuthPasskeysDeleteUuidDelete, getPasskeysAuthPasskeysGetGet, setDisplayNameUsersMeSetDisplayNamePost, setTeamNumberUsersMeSetTeamNumberPost } from "$lib/api/auth/auth";
	import BaseDialog from "$lib/components/generic/dialogs/BaseDialog.svelte";
	import { uploadProfilePictureUploadProfilePictureMePost } from "$lib/api/uploads/uploads";
	import Authentication from "$lib/components/generic/authentication/Authentication.svelte";
	import type { EmailVerificationStatus } from "$lib/components/generic/authentication/EmailVerification.svelte";
	import type { ChangePasswordStatus } from "$lib/components/generic/authentication/ChangePassword.svelte";
	import type { ChangeEmailStatus } from "$lib/components/generic/authentication/ChangeEmail.svelte";
	import type { CreatePasskeyStatus } from "$lib/components/generic/authentication/CreatePasskey.svelte";
	import DeleteAccount, { type DeleteAccountStatus } from "$lib/components/generic/authentication/DeleteAccount.svelte";


    interface Props {
        user: UserResponse
        getNewUserData: () => void
    }
    let { user, getNewUserData }: Props = $props();
    let displayName = $state(user?.display_name);
    let teamNumber = $state(user?.team_number);
    let passkeys: PasskeyResponse[] = $state([]);

    let uploadProfilePictureOpen = $state(false);
    let files: FileList | undefined = $state(undefined);
    let uploadProfilePictureState: "idle" | "uploading" = $state("idle");

    let verifyEmailOpen = $state(false);
    let emailVerificationStatus: EmailVerificationStatus = $state("idle");

    let changePasswordOpen = $state(false);
    let changePasswordStatus: ChangePasswordStatus = $state("idle");

    let changeEmailOpen = $state(false);
    let changeEmailStatus: ChangeEmailStatus = $state("idle");

    let createPasskeyOpen = $state(false);
    let createPasskeyStatus: CreatePasskeyStatus = $state("idle");
    const passkeyNoVerificationHasElapsed = (new Date() - new Date(user.created_at)) >= (+PUBLIC_PASSKEY_NO_VERIFICATION_MINUTES * 60 * 1000);

    let deleteAccountOpen = $state(false);
    let deleteAccountStatus: DeleteAccountStatus = $state("idle");


    /**
     * Set the user's display name on the server
     */
    async function setDisplayName() {
        await setDisplayNameUsersMeSetDisplayNamePost({ display_name: displayName }).then((response) => {
            if (response.status === 200) {
                getNewUserData();
                toast.success("Display name updated");
            } else {
                toast.error("Failed to updated display name");
            }
        });
    }

    /**
     * Set the user's team number on the server
     */
    async function setTeamNumber() {
        await setTeamNumberUsersMeSetTeamNumberPost({ team_number: teamNumber }).then((response) => {
            if (response.status === 200) {
                getNewUserData();
                toast.success("Team number updated");
            } else {
                toast.error("Failed to updated team number");
            }
        });
    }

    /**
     * Upload the user's profile picture to the server
     */
    async function uploadProfilePicture() {
        if (!files || files.length === 0) return;
        if (!files[0]) return;

        uploadProfilePictureState = "uploading";

        await uploadProfilePictureUploadProfilePictureMePost({ file: files[0]}).then((response) => {
            if (response.status === 200) {
                toast.success("Profile picture updated");
                uploadProfilePictureOpen = false;
                getNewUserData();
            } else {
                toast.error("Failed to update profile picture");
                uploadProfilePictureOpen = false;
                uploadProfilePictureState = "idle";
            }
        }).catch((error) => {
            console.error(error);
            toast.error("Failed to update profile picture");
            uploadProfilePictureOpen = false;
            uploadProfilePictureState = "idle";
        });

        uploadProfilePictureState = "idle";
    }

    /**
     * Get the user's passkeys
     */
    async function getPasskeys() {
        await getPasskeysAuthPasskeysGetGet().then((response) => {
            if (response.status === 200) {
                passkeys = response.data;
            }
        })
    }

    /**
     * Delete a passkey
     * @param uuid The uuid of the passkey to delete
     */
    async function deletePasskey(uuid: string) {
        await deletePasskeyAuthPasskeysDeleteUuidDelete(uuid).then((response) => {
            if (response.status === 200) {
                getPasskeys();
                toast.success("Passkey deleted");
            } else {
                toast.error("Failed to delete passkey");
            }
        })
    }

    $effect(() => {
        if (emailVerificationStatus == "success") {
            verifyEmailOpen = false;
            getNewUserData();
            emailVerificationStatus = "idle";
        } else if (emailVerificationStatus == "cancel") {
            verifyEmailOpen = false;
            emailVerificationStatus = "idle";
        } else if (emailVerificationStatus == "skipped") {
            verifyEmailOpen = false;
            emailVerificationStatus = "idle";
        }

        if (changePasswordStatus == "success") {
            changePasswordOpen = false;
            getNewUserData();
            changePasswordStatus = "idle";
        } else if (changePasswordStatus == "cancel") {
            changePasswordOpen = false;
            changePasswordStatus = "idle";
        }

        if (changeEmailStatus == "success") {
            changeEmailOpen = false;
            getNewUserData();
            changeEmailStatus = "idle";
        } else if (changeEmailStatus == "cancel") {
            changeEmailOpen = false;
            changeEmailStatus = "idle";
        }

        if (createPasskeyStatus == "success") {
            createPasskeyOpen = false;
            getPasskeys();
            createPasskeyStatus = "idle";
        } else if (createPasskeyStatus == "cancel") {
            createPasskeyOpen = false;
            createPasskeyStatus = "idle";
        }

        if (deleteAccountStatus == "success") {
            deleteAccountOpen = false;
            deleteAccountStatus = "idle";
        } else if (deleteAccountStatus == "cancel") {
            deleteAccountOpen = false;
            deleteAccountStatus = "idle";
        }
    });

    onMount(() => {
        getPasskeys();
    })
</script>

<Section title="Profile" description="Your profile details">
    <div class="flex flex-col gap-2">
        <Card.Root>
            <Card.Content>
                <div class="flex flex-col md:flex-row gap-2">
                    <Avatar.Root class="group w-16 h-16 bg-muted rounded-full flex items-center justify-center relative overflow-hidden active:scale-90 transition-transform" onclick={() => {uploadProfilePictureOpen = true}}>
                        <Avatar.Image src={user?.profile_picture_url} alt={user?.username} />
                        <Avatar.Fallback class="text-2xl text-white select-none">{user?.username.charAt(0)}</Avatar.Fallback>
                        <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity z-10"></div>
                        <PencilIcon weight="bold" class="absolute inset-0 m-auto text-white opacity-0 group-hover:opacity-100 transition-opacity z-20 text-3xl" />
                    </Avatar.Root>

                    <div class="flex flex-col gap-1 items-start">
                        <div class="flex flex-row gap-2 flex-wrap">
                            <p class="font-bold text-lg">{user?.display_name}</p>

                            {#if user?.display_name != user?.username}
                                <p class="font-bold text-lg text-muted-foreground">{user?.username}</p>
                            {/if}

                            {#if user?.is_superuser}
                                <Badge class="bg-green-400/50">Superuser</Badge>
                            {/if}
                        </div>
                        
                        <p class="text-md text-muted-foreground">{user?.email}</p>
                        <p class="text-md text-muted-foreground">Team: {user?.team_number}</p>

                        <p class="hidden pointer-coarse:block text-xs text-muted-foreground mt-2 wrap-break-word">Tap the profile picture to edit</p>
                    </div>
                </div>
            </Card.Content>
        </Card.Root>

        <Separator class="my-2" />

        <Card.Root>
            <Card.Content class="flex flex-col gap-2">
                <p class="font-bold">Display Name</p>

                <div class="flex flex-col md:flex-row gap-2">
                    <Input placeholder="Display Name" bind:value={displayName} />
                    <Button class="w-fit" disabled={displayName == user?.display_name} onclick={setDisplayName}><CheckCircleIcon weight="bold" /> Save</Button>
                </div>
            </Card.Content>
        </Card.Root>

        <Card.Root>
            <Card.Content class="flex flex-col gap-2">
                <p class="font-bold">Team Number</p>

                <div class="flex flex-col md:flex-row gap-2">
                    <Input placeholder="Team Number" bind:value={teamNumber} />
                    <Button class="w-fit" disabled={teamNumber == user?.team_number} onclick={setTeamNumber}><CheckCircleIcon weight="bold" /> Save</Button>
                </div>
            </Card.Content>
        </Card.Root>

        <Card.Root>
            <Card.Content class="flex flex-col gap-2">
                <div class="flex flex-row gap-2 items-center">
                    <p class="font-bold">Email</p>

                    {#if user.email_verified}
                        <Badge class="bg-green-300/70">Verified</Badge>
                    {:else}
                        <Badge class="bg-red-400/70">Not Verified</Badge>
                    {/if}
                </div>

                {#if !user.email_verified && PUBLIC_EMAIL_ENABLED}
                    <Alert.Root>
                        <InfoIcon weight="bold" />
                        <Alert.Title>Verify your email</Alert.Title>
                        <Alert.Description>
                            You have not verified your email. Please do so, otherwise you will not be able to change your password.
                            <Button onclick={() => {verifyEmailOpen = true}}><ArrowRightIcon weight="bold" /> Verify Email</Button>
                        </Alert.Description>
                    </Alert.Root>
                {/if}

                {#if PUBLIC_EMAIL_ENABLED}
                    <Alert.Root>
                        <InfoIcon weight="bold" />
                        <Alert.Title>Changing your email</Alert.Title>
                        <Alert.Description>
                            If you change your email, you will need to verify it. This email will be used for recovering your account, or creating passkeys.
                        </Alert.Description>
                    </Alert.Root>
                {:else}
                    <Alert.Root variant="destructive">
                        <WarningIcon weight="bold" />
                        <Alert.Title>Emails are disabled on this server</Alert.Title>
                        <Alert.Description>
                            This server does not support sending emails. You will not be able to verify your email, or use it for changing your password. If you loose your password, a passkey will be the only way to recover your account.
                        </Alert.Description>
                    </Alert.Root>
                {/if}

                <Button onclick={() => changeEmailOpen = true}><EnvelopeIcon weight="bold" /> Change Email</Button>
            </Card.Content>
        </Card.Root>

        <Card.Root>
            <Card.Content class="flex flex-col gap-2">
                <p class="font-bold">Password</p>
                <Alert.Root>
                    <InfoIcon weight="bold" />
                    <Alert.Title>Changing your password</Alert.Title>
                    <Alert.Description>
                        If you change your password, you will need to first verify your identity. This requires emails to be enabled on this server, or for you to have created a passkey for this account.
                    </Alert.Description>
                </Alert.Root>
                <Button onclick={() => changePasswordOpen = true}><PasswordIcon weight="bold" /> Change Password</Button>
            </Card.Content>
        </Card.Root>

        <Card.Root>
            <Card.Content class="flex flex-col gap-2">
                <p class="font-bold">Passkeys</p>

                <p>You have created {passkeys.length} passkey{passkeys.length == 1 ? "" : "s"}</p>

                {#each passkeys as passkey}
                    <Card.Root>
                        <Card.Content>
                            <div class="flex flex-row gap-2 items-center justify-between">
                                <div class="flex flex-row gap-2 items-center flex-wrap">
                                    <KeyIcon weight="bold" />
                                    <p class="font-bold">{passkey.label || "No Label"}</p>
                                    <p>{new Intl.DateTimeFormat("en-US", {dateStyle: "medium", timeStyle: "short"}).format(new Date(passkey.created_at))}</p>
                                </div>
                                <AlertDialog.Root>
                                    <AlertDialog.Trigger>
                                        <Button variant="destructive" size="icon-sm"><TrashIcon weight="bold" /></Button>
                                    </AlertDialog.Trigger>

                                    <AlertDialog.Content>
                                        <AlertDialog.Title>Delete Passkey?</AlertDialog.Title>
                                        <AlertDialog.Description>Are you sure you want to delete this passkey? This action cannot be undone, and you will no longer be able to sign in with it.</AlertDialog.Description>
                                        
                                        <AlertDialog.Footer>
                                            <AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
                                            <AlertDialog.Action onclick={() => deletePasskey(passkey.uuid)}>Delete</AlertDialog.Action>
                                        </AlertDialog.Footer>
                                    </AlertDialog.Content>
                                </AlertDialog.Root>
                            </div>
                        </Card.Content>
                    </Card.Root>
                {/each}
                
                <Button onclick={() => createPasskeyOpen = true}><KeyIcon weight="bold" /> Create Passkey</Button>
            </Card.Content>
        </Card.Root>

        <Card.Root>
            <Card.Content class="flex flex-col gap-2">
                <p class="font-bold">Delete Account</p>
                <Button onclick={() => deleteAccountOpen = true} variant="destructive"><TrashIcon weight="bold" /> Delete Account</Button>
            </Card.Content>
        </Card.Root>
    </div>
</Section>

<BaseDialog title="Upload Profile Picture" description="Add or change your profile picture." bind:open={uploadProfilePictureOpen}>
    <div class="flex flex-row gap-2 items-center mt-4">
        <Input type="file" accept="image/*" bind:files />
        <Button onclick={uploadProfilePicture} disabled={files == null || uploadProfilePictureState == "uploading"}>
            {#if uploadProfilePictureState == "idle"}
                <UploadSimpleIcon weight="bold" />
                Upload
            {:else if uploadProfilePictureState == "uploading"}
                <CircleNotchIcon class="animate-spin" weight="bold" />
                Uploading...
            {/if}
        </Button>
    </div>

    <p class="text-sm mt-4">It may take a moment for the image to appear across the site after uploading</p>
    <p class="text-sm text-muted-foreground">10MB max, will be downsized to 256x256. Square image recommended.</p>
    <p class="text-sm text-muted-foreground mb-4">JPEG, PNG, WEBP, HEIC, or HEIF are supported</p>
</BaseDialog>

<BaseDialog title="" description="" bind:open={verifyEmailOpen}>
    <Authentication mode="verify_email" email={user?.email} bind:emailVerificationStatus />
</BaseDialog>

<BaseDialog title="" description="" bind:open={changePasswordOpen}>
    <Authentication mode="change_password" email={user?.email} bind:changePasswordStatus />
</BaseDialog>

<BaseDialog title="" description="" bind:open={changeEmailOpen}>
    <Authentication mode="change_email" email={user?.email} bind:changeEmailStatus />
</BaseDialog>

<BaseDialog title="" description="" bind:open={createPasskeyOpen}>
    <Authentication mode="create_passkey" email={user?.email} bind:createPasskeyStatus createPasskeyRequireUserVerification={passkeyNoVerificationHasElapsed}/>
</BaseDialog>

<BaseDialog title="" description="" bind:open={deleteAccountOpen}>
    <Authentication mode="delete_account" bind:deleteAccountStatus />
</BaseDialog>