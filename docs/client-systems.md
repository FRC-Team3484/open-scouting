# Client Systems

This document lists the various client side systems that are avaliable to aid in development.

- [Dialog](#dialog)


## Dialog
A simple alert dialog that is presented to the user

```html
<script lang="ts">
    import Dialog from "$lib/components/generic/Dialog.svelte";
    
    let showDialog = true;

     function handleCancel() {
        showDialog = false;
        // Additional cancel logic...
    }

    function handleAction() {
        showDialog = false;
        // Additional action logic...
    }
</script>

<Dialog
    bind:open={showDialog}
    title="Dialog"
    description="This is an example dialog."
    buttons={[
        { label: "Cancel", variant: "cancel", onClick: handleCancel },
        { label: "Action", variant: "action", onClick: handleAction },
    ]}
>
    {#snippet contents()}
        <p>This is the dialog's contents.</p>
    {/snippet}
</Dialog>
```