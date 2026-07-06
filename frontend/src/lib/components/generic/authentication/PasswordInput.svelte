<!-- 
@component
Provides a univeral password input, with confirmation checking

Used by CreateAccount, ForgotPassword, and ChangePassword

TODO: Add a password strength meter?

Props:
    - `password` (`string`) - The password to use when logging into your account
    - `confirmPassword` (`string`) - The password to use when logging into your account
-->
<script lang="ts">
	import { slide } from "svelte/transition";
	import { WarningIcon } from "phosphor-svelte";

    import * as Alert from "$lib/components/ui/alert/index";
	import Input from "$lib/components/ui/input/input.svelte";
	import Label from "$lib/components/ui/label/label.svelte";
	import Switch from "$lib/components/ui/switch/switch.svelte";


    interface Props {
        password: string
        confirmPassword: string
    }
    let { password = $bindable(""), confirmPassword = $bindable("") }: Props = $props();

    let showPassword: boolean = $state(false);
</script>

<p class="text-sm text-muted-foreground mb-2">
    Strong passwords are 16+ characters long, and have a mix <br>
    of uppercase and lowercase letters, numbers, and special <br>
    characters. Consider using a passphrase, and don't use the <br>
    same password for multiple websites.
</p>

<Input placeholder="Password" type={showPassword ? "text" : "password"} bind:value={password} autofocus />
<p class="text-sm text-muted-foreground">The password to use when logging into your account</p>

<Input placeholder="Confirm password" type={showPassword ? "text" : "password"} bind:value={confirmPassword} />
<p class="text-sm text-muted-foreground">Confirm your password</p>

<div class="flex flex-row gap-2 mb-4">
    <Switch id="show-password" bind:checked={showPassword} />
    <Label for="show-password">Show Password</Label>
</div>

{#if confirmPassword != password}
    <div transition:slide>
        <Alert.Root variant="destructive" class="mb-2 text-left">
            <WarningIcon weight="bold" />
            <Alert.Title>Passwords do not match</Alert.Title>
        </Alert.Root>
    </div>
{/if}