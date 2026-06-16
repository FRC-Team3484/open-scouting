<!-- 
The authentication page

Allows for the user to sign into their account, or create a new account.
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";
	import { goto } from "$app/navigation";
	import { slide } from "svelte/transition";
	import { ArrowRightIcon, CircleNotchIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
    
	import { getAuthenticationStatus } from "$lib/utils/user";
    import Logo from "$lib/components/generic/Logo.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import Authentication from "$lib/components/generic/authentication/Authentication.svelte";


    let page: "signin" | "signup" = $state("signin");
    let authenticated: boolean = getAuthenticationStatus();

    /**
     * If the user is already signed in, redirect them to the index page
     */
    onMount(async () => {
        if (authenticated) {
            await goto("/");
        }
    })
</script>

<PageContainer>
    {#if !authenticated}
        <div class="flex flex-col w-full md:w-1/2 items-center gap-4">
            <Logo text={false} />
            <p class="text-2xl font-bold">Authentication</p>

            {#if page === "signin"}
                <div class="flex flex-col gap-4 items-center" transition:slide>
                    <Authentication mode="sign_in" />
                    <Button variant="outline" onclick={() => {page = "signup"}}><ArrowRightIcon weight="bold" /> Sign Up</Button>
                </div>

            {:else if page === "signup"}
                <div class="flex flex-col gap-4 items-center" transition:slide>
                    <Authentication mode="create_account" />
                    <Button variant="outline" onclick={() => {page = "signin"}}><ArrowRightIcon weight="bold" /> Sign In</Button>
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
