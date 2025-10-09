<script lang="ts">
    import { Description, Title } from "../ui/alert";
import * as AlertDialog from "../ui/alert-dialog";
	import type { Snippet } from "svelte";
	import Alert from "../ui/alert/alert.svelte";

    export let open: boolean = false;
    export let title: string = "";
    export let description: string = "";

    export let buttons: {
        label: string;
        variant?: "cancel" | "action"; // maps to your shadcn buttons
        onClick?: () => void;
    }[] = [];

    export let contents: Snippet | null = null;
</script>

<AlertDialog.Root bind:open>
    <AlertDialog.Content>
        <AlertDialog.Header>
            <AlertDialog.Title>{title}</AlertDialog.Title>
            <AlertDialog.Description>{description}</AlertDialog.Description>
        </AlertDialog.Header>

        {#if contents}
            {@render contents()}
        {/if}

        {#if buttons}
            <AlertDialog.Footer>
                {#each buttons as button}
                    {#if button.variant === "cancel"}
                        <AlertDialog.Cancel>
                            <button on:click={button.onClick}>{button.label}</button>
                        </AlertDialog.Cancel>
                    {:else}
                        <AlertDialog.Action>
                            <button on:click={button.onClick}>{button.label}</button>
                        </AlertDialog.Action>
                    {/if}
                {/each}
            </AlertDialog.Footer>
        {/if}
    </AlertDialog.Content>
</AlertDialog.Root>