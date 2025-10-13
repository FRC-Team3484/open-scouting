<script lang="ts">
    import { Description, Title } from "../ui/alert";
    import * as AlertDialog from "../ui/alert-dialog";
	import type { Snippet } from "svelte";
	import Alert from "../ui/alert/alert.svelte";

    export let open: boolean = false;
    export let title: string = "";
    export let description: string = "";
    export let cancel_text: string = "Cancel";
    export let submit_text: string = "Submit";
    export let onSubmit: () => void = () => {};

    export let contents: Snippet | null = null;

    function handleSubmit(e: Event) {
        e.preventDefault();
        onSubmit(e);
        open = false;
    }
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

    <AlertDialog.Footer>
        <form method="post" on:submit={handleSubmit}>
            {#if cancel_text}
                <AlertDialog.Cancel type="button">
                    {cancel_text}
                </AlertDialog.Cancel>
            {/if}
            {#if submit_text}
                <AlertDialog.Action type="submit">
                    {submit_text}
                </AlertDialog.Action>
            {/if}
        </form>
    </AlertDialog.Footer>
    </AlertDialog.Content>
</AlertDialog.Root>