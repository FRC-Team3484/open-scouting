<script lang="ts">
	import * as Dialog from "$lib/components/ui/dialog/index.js";

    let { title, description, open = $bindable(), children } = $props();
</script>

<Dialog.Root bind:open={open}>
    <Dialog.Content>
        <Dialog.Header>
            <Dialog.Title>{title}</Dialog.Title>
            <Dialog.Description>{description}</Dialog.Description>
        </Dialog.Header>

        {@render children()}

    </Dialog.Content>
</Dialog.Root>