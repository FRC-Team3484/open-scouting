<script lang="ts">
    import { superForm } from "sveltekit-superforms";

    import * as Form from "$lib/components/ui/form/index";
    import Input from "../ui/input/input.svelte";
	import { zod4Client } from "sveltekit-superforms/adapters";
	import Label from "../ui/label/label.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import { loginForAccessTokenTokenPost } from "$lib/api/auth/auth";
	import { ArrowRight } from "phosphor-svelte";

    let { page = $bindable() } = $props();

    const form = superForm(
        {
            username: "",
            password: "",
        }
    )
    const { form: formData, enhance } = form

    async function signIn() {
        if (!$formData.username && !$formData.password) {
            return;
        }
        
        const res = await loginForAccessTokenTokenPost($formData);

        if (res.status === 200) {
            localStorage.setItem("access_token", res.data.access_token);
            window.location.href = "/";
        }
    }
</script>

<form method="POST" use:enhance class="flex flex-col gap-2 m-8 text-left" on:submit|preventDefault={signIn}>        
    <Form.Field {form} name="username">
        <Form.Control>
            {#snippet children({ props })}
                <Label>Username</Label>
                <Input {...props} bind:value={$formData.username} />
            {/snippet}
        </Form.Control>
        <Form.Description>The username of the user account.</Form.Description>
        <Form.FieldErrors />
    </Form.Field>

    <Form.Field {form} name="password">
        <Form.Control>
            {#snippet children({ props })}
                <Label>Password</Label>
                <Input {...props} type="password" bind:value={$formData.password} />
            {/snippet}
        </Form.Control>
        <Form.Description>The password of the user account.</Form.Description>
        <Form.FieldErrors />
    </Form.Field>

    <Form.Button>Sign In</Form.Button>
    <Form.Button type="button" onclick={() => page = "signup"} variant="outline"><ArrowRight weight="bold" /> Create Account</Form.Button>
</form>