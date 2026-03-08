<script lang="ts">
    import { superForm } from "sveltekit-superforms";
	import { zod, zod4Client } from "sveltekit-superforms/adapters";
	import { ArrowRight, Warning } from "phosphor-svelte";

    import Input from "../ui/input/input.svelte";
    import * as Alert from "$lib/components/ui/alert/index";
	import Label from "../ui/label/label.svelte";
	import Separator from "../ui/separator/separator.svelte";
    import * as Form from "$lib/components/ui/form/index";
    import { SignupAuthSignupPostBody } from "$lib/zod/auth/auth";
	import { signupAuthSignupPost } from "$lib/api/auth/auth";
    import {} from "$lib/zod/auth/auth"

    let { page = $bindable() } = $props();

    let message = $state("");

    const defaultValues = {
        username: "",
        email: "",
        password: "",
        confirm_password: "",
        team_number: 0,
        display_name: ""
    }

    const form = superForm(defaultValues, {
        SPA: true,
        validators: zod4Client(SignupAuthSignupPostBody),
        async onUpdate({ form }) {
            if (form.valid) {
                const res = await signupAuthSignupPost(form.data);

                if (res.status === 200) {
                    localStorage.setItem("access_token", res.data.access_token);
                    window.location.href = "/";
                } else {
                    console.error(res);
                    message = res.data.detail[0].msg || "Something went wrong";
                }
            }
        }
    });

    const { form: formData, enhance } = form
</script>

{#if message}
    <Alert.Root variant="destructive" class="text-left">
        <Warning weight="bold" />
        <Alert.Title>
            There was a problem
        </Alert.Title>
        <Alert.Description>
            {message}
        </Alert.Description>
    </Alert.Root>
{/if}

<form use:enhance method="POST" class="flex flex-col gap-2 mx-4 text-left">        
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