<script lang="ts">
	import { env } from "$env/dynamic/public";
    import Logo from "$lib/components/generic/Logo.svelte";
    import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Alert from "$lib/components/ui/alert/index.js";
    import Input from "$lib/components/ui/input/input.svelte";
    import Label from "$lib/components/ui/label/label.svelte";
    import Separator from "$lib/components/ui/separator/separator.svelte";
    import { ArrowRight, Info, Lock, Plus } from "phosphor-svelte";
	import { onMount } from "svelte";
	import { validateTokenOnline } from "$lib/user";
	import { toast } from "svelte-sonner";

    let page: "signin" | "signup" = "signin";
    let message: string | null = null;

    const API_URL = env.PUBLIC_FAST_API_URL;

    async function handleSubmit(e: Event) {
        e.preventDefault();
        const form = e.currentTarget as HTMLFormElement;
        const formData = new FormData(form);

        const endpoint = page === "signin" ? "/token" : "/auth/signup";
        const res = await fetch(API_URL + endpoint, {
            method: "POST",
            body: `username=${formData.get("username")}&password=${formData.get("password")}`,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });

        const data = await res.json();
        message = data.message ?? data.detail;

        if (res.ok) {
            if (data.access_token) {
                localStorage.setItem("access_token", data.access_token);
                window.location.href = "/";
            }
        }
    }

    onMount(async () => {
        if (await validateTokenOnline()) {
            toast.success("You are already signed in, redirecting...");
            window.location.href = "/";
        }
    })
</script>

<div class="flex flex-col gap-4 w-screen h-screen items-center justify-center">
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
            <form class="flex flex-col gap-4 w-full" on:submit={handleSubmit}>
                <Card.Root class="w-full">
                    <Card.Header>
                        <Card.Title>Sign In</Card.Title>
                        <Card.Description>Sign in to your Open Scouting account</Card.Description>
                    </Card.Header>

                    <Card.Content class="flex flex-col gap-2">
                        <Label for="username">Username</Label>
                        <Input name="username" id="username" type="text" placeholder="Username" required />

                        <Label for="password">Password</Label>
                        <Input name="password" id="password" type="password" placeholder="Password" required />
                    </Card.Content>

                    <Card.Footer class="gap-2">
                        <Button type="submit"><ArrowRight weight="bold" /> Sign In</Button>
                        <Button variant="ghost" type="button" onclick={() => page = "signup"}>
                            <Plus weight="bold" /> Create Account
                        </Button>
                    </Card.Footer>
                </Card.Root>
            </form>

        {:else if page === "signup"}
            <form class="flex flex-col gap-4 w-full" on:submit={handleSubmit}>
                <Card.Root class="w-full">
                    <Card.Header>
                        <Card.Title>Create Account</Card.Title>
                        <Card.Description>Create a new Open Scouting account</Card.Description>
                    </Card.Header>

                    <Card.Content class="flex flex-col gap-2">
                        <Label for="username">Username</Label>
                        <Input name="username" id="username" type="text" placeholder="Username" required />

                        <Label for="email">Email</Label>
                        <Input name="email" id="email" type="email" placeholder="Email" required />

                        <Label for="password">Password</Label>
                        <Input name="password" id="password" type="password" placeholder="Password" required />

                        <Label for="confirm_password">Confirm Password</Label>
                        <Input name="confirm_password" id="confirm_password" type="password" placeholder="Confirm Password" required />

                        <Separator class="my-4" />

                        <Label for="team_number">Team Number</Label>
                        <Input name="team_number" id="team_number" type="text" placeholder="Team Number" />

                        <Label for="display_name">Display Name</Label>
                        <Input name="display_name" id="display_name" type="text" placeholder="Display Name" />
                    </Card.Content>

                    <Card.Footer class="gap-2">
                        <Button type="submit"><ArrowRight weight="bold" /> Create Account</Button>
                        <Button variant="ghost" type="button" onclick={() => page = "signin"}>
                            <Lock weight="bold" /> Sign In
                        </Button>
                    </Card.Footer>
                </Card.Root>
            </form>
        {/if}
    </div>
</div>
