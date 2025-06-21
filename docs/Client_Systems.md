# Client Systems

This page documents how to use several of the systems and utilities that are built into Open Scouting's client to aid in development

- [Sending notifications](#sending-notifications)
- [Using common styles](#using-common-styles)
- [Showing dialogs](#showing-dialogs)
- [Client logging](#client-logging)
- [Accessing the client database](#accessing-the-client-database)
- [Client user management](#client-user-management)

## Sending notifications
Notifications are shown next to the menu and can be used to provide the user with some information if an action succeeds or fails

Send a notification using a JavaScript event, on any page that uses the menu

Parameters for the event details:
- `title` - The title of the notification
- `body` - The body text of the notification
- `icon` - The icon to display on the notification, as a Phosphor Icon, minus the `ph-` part

```js
window.dispatchEvent(
    new CustomEvent("scouting_notification", {
        detail: {
            title: "Event autofilled",
            body: "Autofilled the event and year from the provided link data",
            icon: "lightning",
        },
    }),
);
```

## Using common styles
There's several common UI styles located in [`styles.css`](/scouting/static/main/src/styles.css)

- `ui_button` - A large button
- `ui_button_icon` - A button the same height, but only wide enough to fit an icon
- `ui_button_small` - A much smaller button, useful for groups of more buttons or chips
- `ui_input` - Styles for a text input, drop down, or multiple choice box
- `ui_checkbox` - Styles for checkboxes

Using these styles is as simple as using them as a tailwind utility class

```html
<!-- Note the 'ui_button' -->
<button class="ui_button w-full" @click="sign_in()">
    <i class="ph-bold ph-user-circle"></i> Sign In
</button>
```

## Showing dialogs
Dialogs cover the entire page's content and are used to ask the user a question or display urgent information

Create a dialog using a JavaScript event, on any page that has the dialog component available

Parameters for the event details:
- `event_name` - Used later to receive events from buttons clicked for a specific dialog
- `title` - The title text of the dialog
- `body` - The body text of the dialog
- `buttons` - An array of the buttons to display on the dialog
    - Buttons take several parameters:
        - `type` - Can be `confirm`, `cancel`, or `close`. Returns different events based on the type
        - `icon` - The CSS class to apply to show an icon
        - `text` - The text to show on the button

```js
// Showing a dialog
window.dispatchEvent(
    new CustomEvent("dialog_show", {
        detail: {
            event_name: "sign_out",
            title: "Signing out will clear page cache",
            body: "You're currently offline. Signing out will reset any cached pages to make sure your user is actually signed in. Those pages will not be able to be cached again until you're online, so the site may not work properly if you proceed. Are you sure you want to sign out?",
            buttons: [
                { type: "confirm", icon: "ph-bold ph-check", text: "Sign out" },
                { type: "cancel", icon: "ph-bold ph-x", text: "Not now" },
            ],
        },
    }),
);
```

Later, to react on a button in the dialog getting pressed, you'll need to capture one of three events based on the button type you chose. The event will either be `dialog_confirm`, `dialog_cancel` or `dialog_close`.

These events returns an `event_name` in the details, which can be used to check for what dialog that button was pressed on

> ![NOTE]
> Ensure you don't call `event.stopImmediatePropagation();` until you're sure you wish to react on that event. If multiple components use dialogs, only one component might get the `dialog_confirm` event.

```js
// Reacting to the dialog_confirm event, and checking that it's of type sign_out before doing anything with that event
window.addEventListener("dialog_confirm", (event) => {
    const { event_name } = event.detail;

    if (event_name === "sign_out") {
        event.stopImmediatePropagation();

        localStorage.setItem("offline_manual", false);
        window.dispatchEvent(new CustomEvent("sw_update_offline_manual"));

        this.sign_out();
    }
});
```

## Client logging
Open Scouting comes with a way to handle client side logging. Log messages sent using this function allows users to view those messages in a user interface, and submit a log file when opening bug reports if needed

Messages will be logged to the console with the file and line number (in most cases). Users can view logged messages in the menu, and export a file of those messages. Only a maximum of 100 log messages are stored in the client between page loads.

The function definition for the log function in [`log.js`](/scouting/static/main/scripts/log.js):

```js
/**
 * Logs a message to the console with colors and location information
 *
 * The location information is colored as needed in different environments
 *
 * Also stores the logs in the global array
 *
 * @param {string} [level="INFO"] - The level of the log message.
 * @param {...*} messages - The messages to be logged.
 */
function log(level = "INFO", ...messages)
```

And basic usage:
```js
log("INFO", "Example info message")
log("WARNING", "Example warning message")
log("ERROR" , "Example error message")
log("DEBUG", "Example debug message")
```
Permitted log levels are `INFO`, `WARNING`, `ERROR` and `DEBUG`

## Accessing the client database
The client database is defined in a global [`db.js`](/scouting/static/main/scripts/db.js) file and uses [Dexie.js](https://dexie.org/)

If any database migrations (new object store, add new fields to store) are needed, they should be specified in this file. 

You can access the client database for saving or querying data using `db`:
```js
db.open()
    .then(() => {
        const data = "";

        db.backups
            .add(data)
            .then(() => {
                // Do something when the operation completes
            })
            .catch((error) => {
                // Do something if the operation fails
            });
    })
    .catch((error) => {
        // Do something if unable to open the database
    });
```

Check the [Dexie.js documentation](https://dexie.org/docs/API-Reference#quick-reference) for more information on usage

## Client user management
Open Scouting has a [`user.js`](/scouting/static/main/scripts/user.js) file that handles the current authenticated user

To use utilities from this file on a page, include the following in the `body` block, below the environment variable settings
```html
<script>
    const user = new User();
    window.user = user;

    user.check_authentication_status().then(() => {
        window.dispatchEvent(new CustomEvent("user_ready", { detail: user }));
    });
</script>
```

Now the user utility functions can be used with `user.*`, and things on the page relying on the user utility functions should be called when the `user_ready` event is called

### `check_authentication_status`
This function checks the authentication status with the server and stores it locally for offline use. If the user is offline, this is retrieved locally. If it's not stored locally, the user is marked as not authenticated

```js
user.check_authentication_status()
```

### `sign_out`
Signs the user out and reloads the page. This will also clear the service worker cache, and should only be called from the index and profile pages where there's a confirmation prompt for clearing the cache

```js
user.sign_out()
```

### `load_settings`
Fetches the user's settings from the server and stores it locally. Is called automatically in most cases

```js
user.load_settings()
```

### `save_settings`
Uploads the changed settings to the server. Should be called once editing settings is finished, and doesn't need to be called if multiple settings are being set

```js
user.save_settings()
```

### `get_setting`
Gets a value of a setting

Parameters:
- key - The name of the setting

```js
user.get_setting("favorite_events")
```

### `get_all_settings`
Gets all the user's settings, as a list of objects with `name`, `value`, and `type` attributes
Is the same as `user.settings`

```js
user.get_all_settings()
```

### `set_setting`
Sets a value to a user's setting and stores it locally. Does not save it to the server, `save_settings` is needed to do that

Parameters:
- key - The name of the setting
- value - The value of the setting to set

```js
user.set_setting("favorite_events", ["2025paca"])
```