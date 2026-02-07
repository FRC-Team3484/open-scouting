<script lang="ts">
    import { superForm } from "sveltekit-superforms";

    import * as Form from "$lib/components/ui/form/index";
    import Input from "../ui/input/input.svelte";
    import { SignupAuthSignupPostBody } from "$lib/zod/auth/auth";
	import { zod4Client } from "sveltekit-superforms/adapters";
	import Label from "../ui/label/label.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import { signupAuthSignupPost } from "$lib/api/auth/auth";
	import { ArrowRight } from "phosphor-svelte";

    let { page = $bindable() } = $props();

    const form = superForm(
        {
            username: "",
            email: "",
            password: "",
            confirm_password: "",
            team_number: 0,
            display_name: "",
        },
        {
            validators: zod4Client(SignupAuthSignupPostBody)
        }
    )
    const { form: formData, enhance } = form

    async function createAccount(e: Event) {
        const result = await form.validateForm();

        if (!result.valid) {
            return;
        }
        
        const res = await signupAuthSignupPost($formData);

        if (res.status === 200) {
            localStorage.setItem("access_token", res.data.access_token);
            window.location.href = "/";
        }
    }
</script>

<form method="post" use:enhance class="flex flex-col gap-2 m-8 text-left" on:submit|preventDefault={createAccount}>        
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

    <Form.Field {form} name="email">
        <Form.Control>
            {#snippet children({ props })}
                <Label>Email</Label>
                <Input {...props} bind:value={$formData.email} />
            {/snippet}
        </Form.Control>
        <Form.Description>The email of the user account.</Form.Description>
        <Form.FieldErrors />
    </Form.Field>

    <Form.Field {form} name="password">
        <Form.Control>
            {#snippet children({ props })}
                <Label>Password</Label>
                <Input {...props} bind:value={$formData.password} />
            {/snippet}
        </Form.Control>
        <Form.Description>The password of the user account.</Form.Description>
        <Form.FieldErrors />
    </Form.Field>

    <Form.Field {form} name="confirm_password">
        <Form.Control>
            {#snippet children({ props })}
                <Label>Confirm Password</Label>
                <Input {...props} bind:value={$formData.confirm_password} />
            {/snippet}
        </Form.Control>
        <Form.Description>Confirm the password of the user account.</Form.Description>
        <Form.FieldErrors />
    </Form.Field>

    <Separator />

    <Form.Field {form} name="team_number">
        <Form.Control>
            {#snippet children({ props })}
                <Label>Team Number</Label>
                <Input {...props} type="number" bind:value={$formData.team_number} />
            {/snippet}
        </Form.Control>
        <Form.Description>The team number of the user account.</Form.Description>
        <Form.FieldErrors />
    </Form.Field>

    <Form.Field {form} name="display_name">
        <Form.Control>
            {#snippet children({ props })}
                <Label>Display Name</Label>
                <Input {...props} bind:value={$formData.display_name} />
            {/snippet}
        </Form.Control>
        <Form.Description>The display name of the user account.</Form.Description>
        <Form.FieldErrors />
    </Form.Field>

    <Form.Button>Create Account</Form.Button>
    <Form.Button type="button" onclick={() => page = "signin"} variant="outline"><ArrowRight weight="bold" /> Sign In</Form.Button>
</form>