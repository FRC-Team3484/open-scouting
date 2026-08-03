<!-- 
@component
Component for showing a warning message in authentication modes

Props:
    - `message` (`string`) - The message to show
-->
<script lang="ts">
	import { slide } from "svelte/transition";
	import { WarningIcon } from "phosphor-svelte";

    import * as Alert from "$lib/components/ui/alert/index";


    interface Props {
        message: string
    }
    let { message }: Props = $props();
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