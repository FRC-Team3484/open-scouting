# Client Systems

This document lists the various client side systems that are available to aid in development.

- [Client Systems](#client-systems)
  - [Dialogs](#dialogs)
  - [Toasts](#toasts)
  - [Database](#database)
  - [UI](#ui)
  - [User Managment](#user-managment)
  - [Authentication Components](#authentication-components)
  - [User Settings](#user-settings)
  - [API Requests](#api-requests)
  - [Form Validation](#form-validation)
  - [Menu Status](#menu-status)

## Dialogs
### BaseDialog
A larger dialog that automatically switches to a drawer on smaller screens
```html
<script lang="ts">
    import BaseDialog from "../dialogs/BaseDialog.svelte";

    let dialogOpen = $state(true)
</script>

<BaseDialog title="Dialog title" description="Dialog description" bind:open={dialogOpen}>
    <!-- Dialog contents -->
</BaseDialog>
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

```bash
cd frontend
npx shadcn-svelte@latest add
```

## User Managment
The client can get the current user data using the `user` store from `$lib/utils/auth.ts`.

The client can manage the currently authenticated user using `$lib/utils/user.ts`:

- `signOut()` - Sign the user out
- `getUserSettings()` - Get all user settings from the server
- `setUserSettings(settings)` - Update the user's settings on the server
- `getUserSetting(key)` - Get a single user setting from the server
- `setUserSetting(key, value)` - Set a single user setting on the server

## Authentication Components
Various universal authentication components are provided in `$lib/components/generic/authentication`.

These components support most user operations. This includes changing emails and passwords, creating and logging into accounts, creating passkeys, deleting accounts, email verification, a forgot password flow, and passkey verification. These components still work when the server has emails disabled. Users are encouraged to always create a passkey so they can recover their account when emails are disabled.

These components should be accessed using the wrapper `Authentication.svelte`. This component requires the mode prop:
- `mode` (`create_account | sign_in | change_password | forgot_password | verify_email | change_email | create_passkey | delete_account`)

Additional props are needed depending on the mode. For example, `email` is required when the `mode` is `verify_email`, `change_password`, `change_email` or `create_passkey`.

Finally, this component exposes bindable status props for most of the avaliable modes. Use these status props to listen to when the authentication action has completed, to know when the dialog can be closed or the next step can proceed.

See the full component for more information.

## User Settings
Settings can be defined for user accounts in `backend/models.py`. These use special tortoise fields which provide some special metadata for each setting.

The following settings are avaliable:
- `StringSetting` (subclass of `CharField`)
- `NumberSetting` (subclass of `IntField`)
- `BooleanSetting` (subclass of `BooleanField`)
- `ArraySetting` (subclass of `JSONField`)
- `JSONSetting` (subclass of `JSONField`)

These settings include metadata which appear on the user's profile page:
- `display_name` - The human readable name for the setting
- `setting_description` - The human readable description for the setting
- `section` - The section to show the setting in. Settings with the same section will be grouped together. Leave this string empty to place the setting in the root section.
- `visible` - If the setting should be shown on the profile page.

Create these fields in the `Settings` model:
```python
favorite_events = ArraySetting(null=True, default=list, display_name="Favorite Events", setting_description="Your favorite events, which appear at the top of the event list", section="General", visible=True)
```

Upon running database migrations with the new setting, the user will be able to view the current value of these settings and change them on their profile page.

## API Requests
Requests can be made to the backend using the typed request functions in `$lib/api`

## Form Validation
Forms can be validated using `sveltekit-superforms` and the typed zod schemas in `$lib/zod`

## Menu Status
You can show the progress of a task in the menu by setting the `menuState` store

- `state` - Either `ready`, `loading` or `warning`. Indicates what icon should be shown on the menu
- `status` - The text description of the task or warning
- `close` - If the text should be hidden three seconds after the data is written (Used to indicate a task was completed)

```js
import { menuState } from "$lib/stores/menu";

menuState.set({
    state: "loading",
    status: "Fetching season data...",
    close: false
});
```