<!-- 
@component
The base for a user setting, rendered on the profile page

Props:
    - `setting` (`UserSetting`) - The user setting to render
    - `newValue` (`any`) - The new value of the setting, from the parent
    - `getNewSettings` (`() => void`) - A function to get the new settings
    - `children` (`Snippet`) - The child components of the setting
-->
<script lang="ts">
	import type { Snippet } from "svelte";

    import * as Card from "$lib/components/ui/card/index.js";
	import type { UserSetting } from "$lib/api/model";
	import Button from "$lib/components/ui/button/button.svelte";
	import { CheckIcon } from "phosphor-svelte";
	import { toast } from "svelte-sonner";
	import { updateUserSettingsUsersMeUpdateSettingsPost } from "$lib/api/auth/auth";


    interface Props {
        setting: UserSetting
        newValue?: any
        getNewSettings: () => void
        children: Snippet
    }
    let { setting, newValue, getNewSettings, children }: Props = $props();

    async function save() {
        await updateUserSettingsUsersMeUpdateSettingsPost({ [setting.key]: newValue }).then((response) => {
            if (response.status === 200) {
                getNewSettings();
                toast.success("Saved " + setting.name, { duration: 5000 });
            } else {
                toast.error("Failed to save " + setting.name, { duration: 5000, description: response.data.detail });
            }
        });
    }
</script>

<Card.Root>
    <Card.Content>
        <div class="flex flex-col gap-2">
            <div class="flex flex-row gap-2 items-center">
                <p class="font-bold">{setting.name}</p>
                <p class="text-sm text-muted-foreground">{setting.key}</p>
                <p class="text-sm text-muted-foreground">{setting.type}</p>
            </div>

            <p class="text-muted-foreground">{setting.description}</p>

            {@render children()}

            <Button class="w-fit" onclick={() => save()} disabled={newValue == setting.value}><CheckIcon weight="bold" /> Save</Button>
        </div>
    </Card.Content>
</Card.Root>