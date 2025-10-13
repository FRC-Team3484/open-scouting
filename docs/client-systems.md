# Client Systems

This document lists the various client side systems that are available to aid in development.

- [Dialog](#dialog)
- [Toast](#toasts)
- [Database](#database)
- [UI](#ui)
- [User Management](#user-managment)
- [API Requests](#api-requests)

## Dialog
A simple alert dialog that is presented to the user

```html
<script lang="ts">
    import Dialog from "$lib/components/generic/Dialog.svelte";
    
    let show_warning_dialog = true;

    function closeWarningDialog(): void {
        show_warning_dialog = false;
    }
</script>

<Dialog 
    open={show_warning_dialog} 
    title="Open Scouting Administration" 
    description="By continuing, understand that changes made here are irreversible, and may cause unintended consequences. Know what you're doing and proceed with caution." 
    cancel_text=""
    submit_text="Continue"
    onSubmit={closeWarningDialog}
/>
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
  import { db } from '$lib/utils/db';

  // Use dexie.js from this, like db.open(), ect.
</script>
```

See the full Dexie.js docs [here](https://dexie.org/)

## UI
You can add new components using the `shadcn-svelte` cli

```
cd frontend
npx shadcn-svelte@latest add
```

## User Managment
The client can manage the currently authenticated user using `$lib/utils/user.ts`

- `validateTokenOnline()` - If the user is authenticated and has a valid token, returns the user's data
- `signOut()` - Signs the user out by deleting the access token from the client
- `getUserSettings()` - Returns all the settings for the user
- `setUserSettings(settings)` - Updates all the settings for the user
    - `settings` - The dictionary of settings, hopefully edited based off of the result of `getUserSettings()`
- `getUserSetting(key)` - Returns the value of a specific setting for the user
    - `key` - The key of the specific setting
- `setUserSetting(key, value)` - Sets a specific setting to a certain value
    - `key` - The key of the specific setting
    - `value` - The value to set the setting to


## API Requests
Requests can be made to the backend using `api.ts`