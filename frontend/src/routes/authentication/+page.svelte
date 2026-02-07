<script lang="ts">
	import { env } from "$env/dynamic/public";
    import Logo from "$lib/components/generic/Logo.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Alert from "$lib/components/ui/alert/index.js";
    import { Info } from "phosphor-svelte";
	import { onMount } from "svelte";
	import { validateTokenOnline } from "$lib/utils/user";
	import { toast } from "svelte-sonner";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";

	import SignUpForm from "$lib/components/auth/SignUpForm.svelte";
	import SignInForm from "$lib/components/auth/SignInForm.svelte";

    let page: "signin" | "signup" = "signin";
    let message: string | null = null;

    const API_URL = env.PUBLIC_FAST_API_URL;

    onMount(async () => {
        if (await validateTokenOnline()) {
            toast.success("You are already signed in, redirecting...");
            window.location.href = "/";
        }
    })
</script>

<PageContainer>
    <div class="flex flex-col w-full md:w-1/2 items-center gap-4">
        <Logo text={false} />
        <p class="text-2xl font-bold">Authentication</p>

        {#if message}
            <Alert.Root variant="destructive">
                <Info weight="bold" />
                <Alert.Title>{message}</Alert.Title>
            </Alert.Root>
        {/if}

        {#if page === "signin"}
            <Card.Root class="w-full">
                <Card.Header>
                    <Card.Title>Sign In</Card.Title>
                    <Card.Description>Sign in to your Open Scouting account</Card.Description>
                </Card.Header>

                <SignInForm bind:page={page} />
            </Card.Root>

        {:else if page === "signup"}
            <Card.Root class="w-full">
                <Card.Header>
                    <Card.Title>Create Account</Card.Title>
                    <Card.Description>Create a new Open Scouting account</Card.Description>
                </Card.Header>

                <SignUpForm bind:page={page} />
            </Card.Root>
        {/if}
    </div>
</PageContainer>
