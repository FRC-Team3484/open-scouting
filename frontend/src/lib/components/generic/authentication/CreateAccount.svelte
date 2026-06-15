<script lang="ts">
	import { checkUniqueUsernameAuthCheckUniqueUsernameGet } from "$lib/api/auth/auth";
    import * as Alert from "$lib/components/ui/alert/index";
	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
	import { ArrowRightIcon, CircleNotchIcon, EnvelopeIcon, WarningIcon } from "phosphor-svelte";
	import { slide } from "svelte/transition";

    let page: "username" | "verify" | "password" | "profile" | "passkey" | "success" = $state("username");

    let username: string = $state("");
    let email: string = $state("");

    let checkingUsername: boolean = $state(false);
    let message: string = $state("");

    async function checkUsername() {
        checkingUsername = true;
        await checkUniqueUsernameAuthCheckUniqueUsernameGet({ username: username, email: email }).then((response) => {
            console.log(response);
            if (response.status == 200) {
                page = "verify";
                message = "";
            } else {
                message = response.data.message;
            }
        })
        checkingUsername = false;
    }
</script>

{#if message}
    <div transition:slide>
        <Alert.Root variant="destructive" class="mb-2 text-left">
            <WarningIcon weight="bold" />
            <Alert.Title>There was a problem</Alert.Title>
            <Alert.Description>{message}</Alert.Description>
        </Alert.Root>
    </div>
{/if}

{#if page == "username"}
    <div class="flex flex-col gap-2 text-left" transition:slide>
        <div class="flex flex-row gap-2 items-center">
            <EnvelopeIcon weight="bold" />
            <p class="font-bold">First, choose a username and enter your email</p>
        </div>

        <Input placeholder="Username" type="text" bind:value={username} autofocus />
        <p class="text-sm text-muted-foreground">You will use your username to sign in. <br>It must be unique on this server. You can choose a display name later.</p>

        <Input placeholder="Email" type="email" bind:value={email} />
        <p class="text-sm text-muted-foreground">You can also use your email to sign in. <br>We will use this email to send you verification emails (if supported).</p>

        <Button onclick={() => {checkUsername()}} disabled={username.trim() == "" || email.trim() == "" || checkingUsername}>
            {#if checkingUsername}
                <CircleNotchIcon class="animate-spin" size={16} /> Checking...
            {:else}
                <ArrowRightIcon weight="bold" /> Next
            {/if}
        </Button>
    </div>
{:else if page == "verify"}

{:else if page == "password"}

{:else if page == "profile"}

{:else if page == "passkey"}

{:else if page == "success"}

{/if}