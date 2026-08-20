<!-- 
The authentication page

Allows for the user to sign into their account, or create a new account.
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { slide } from "svelte/transition";
	import { ArrowRightIcon, CircleNotchIcon, QuestionMarkIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
    
    import Logo from "$lib/components/generic/Logo.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import Authentication from "$lib/components/generic/authentication/Authentication.svelte";
	import type { ForgotPasswordStatus } from "$lib/components/generic/authentication/ForgotPassword.svelte";
	import { user } from "$lib/utils/auth";


    let page: "signin" | "signup" | "forgot_password" = $state("signin");
    let forgotPasswordStatus: ForgotPasswordStatus = $state("idle");
    let ref: string = $state("/");

    /**
     * If the user is already signed in, redirect them to the index page
     */
    onMount(async () => {
        const params = new URLSearchParams(window.location.search);
        if (params.has("ref")) {
            ref = params.get("ref") || "/";
        }

        if ($user.authenticated && !$user.loading) {
            await goto(ref);
        }
    });

    $effect(() => {
        if (forgotPasswordStatus === "success" || forgotPasswordStatus === "cancel") {
            page = "signin";
        }
    })
</script>

<PageContainer>
    {#if !$user.authenticated}
        <div class="flex flex-col w-full md:w-1/2 items-center gap-4">
            <Logo text={false} href="/" />
            <p class="text-2xl font-bold">Authentication</p>

            {#if page === "signin"}
                <div class="flex flex-col gap-4 items-center" transition:slide>
                    <Authentication mode="sign_in" ref={ref} />
                    <Button variant="outline" onclick={() => {page = "forgot_password"}}><QuestionMarkIcon weight="bold" /> Forgot Password</Button>
                    <Button variant="outline" onclick={() => {page = "signup"}}><ArrowRightIcon weight="bold" /> Sign Up</Button>
                </div>

            {:else if page === "signup"}
                <div class="flex flex-col gap-4 items-center" transition:slide>
                    <Authentication mode="create_account" ref={ref} />
                    <Button variant="outline" onclick={() => {page = "signin"}}><ArrowRightIcon weight="bold" /> Sign In</Button>
                </div>

            {:else if page === "forgot_password"}
                <div class="flex flex-col gap-4 items-center" transition:slide>
                    <Authentication mode="forgot_password" bind:forgotPasswordStatus={forgotPasswordStatus} />
                </div>
            {/if}
        </div>
    {:else}
        <div class="flex flex-col gap-2 items-center">
            <CircleNotchIcon weight="bold" class="animate-spin" size={32} />
            <p class="text-lg font-bold">You are already signed in</p>
            <p>Redirecting...</p>
        </div>
    {/if}
</PageContainer>
