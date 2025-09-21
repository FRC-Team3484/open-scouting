<script lang="ts">
    import {
        AlertDialog,
        AlertDialogContent,
        AlertDialogTitle,
        AlertDialogDescription,
        AlertDialogCancel,
        AlertDialogAction,
        AlertDialogFooter
    } from "$lib/components/ui/alert-dialog";
	import type { Snippet } from "svelte";

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

<AlertDialog bind:open>
    <AlertDialogContent>
        <AlertDialogTitle>{title}</AlertDialogTitle>
        <AlertDialogDescription>{description}</AlertDialogDescription>

        {#if contents}
            {@render contents()}
        {/if}

        {#if buttons}
            <AlertDialogFooter>
                {#each buttons as button}
                    {#if button.variant === "cancel"}
                        <AlertDialogCancel on:click={button.onClick}>
                            {button.label}
                        </AlertDialogCancel>
                    {:else}
                        <AlertDialogAction on:click={button.onClick}>
                            {button.label}
                        </AlertDialogAction>
                    {/if}
                {/each}
            </AlertDialogFooter>
        {/if}
    </AlertDialogContent>
</AlertDialog>