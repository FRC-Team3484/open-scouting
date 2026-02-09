<script lang="ts">
    import { superForm } from "sveltekit-superforms";

    import * as Form from "$lib/components/ui/form/index";
    import * as Alert from "$lib/components/ui/alert/index";
    import Input from "../ui/input/input.svelte";
	import Label from "../ui/label/label.svelte";
	import { loginForAccessTokenTokenPost } from "$lib/api/auth/auth";
	import { ArrowRight, Warning } from "phosphor-svelte";

    let { page = $bindable() } = $props();

    let message = $state("");

    const defaultValues = {
        username: "",
        password: "",
    }

    const form = superForm(defaultValues, {
            SPA: true,
            async onUpdate({ form }) {
                if (!form.data.username && !form.data.password) {
                    return;
                }
                
                const res = await loginForAccessTokenTokenPost($formData);

                if (res.status === 200) {
                    localStorage.setItem("access_token", res.data.access_token);
                    window.location.href = "/";
                } else {
                    message = res.data.detail || "Something went wrong";
                }
            }
        }
    )
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

<form class="flex flex-col gap-2 mx-4 text-left" use:enhance>        
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