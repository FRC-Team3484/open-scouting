# Client Systems

This document lists the various client side systems that are avaliable to aid in development.

- [Dialog](#dialog)
- [Toast](#toasts)
- [Database](#database)


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

## Toasts
Toasts can be shown to the user

```js
toast("Example toast", { description: "This is a description" })
```

See the full Svelte Sonner docs [here](https://svelte-sonner.vercel.app/) for more options

## Database
You can access the client database using a global db instance

```html
<script lang="ts">
  import { db } from '$lib/db';

  // Use dexie.js from this, like db.open(), ect.
</script>
```

See the full Dexie.js docs [here](https://dexie.org/)