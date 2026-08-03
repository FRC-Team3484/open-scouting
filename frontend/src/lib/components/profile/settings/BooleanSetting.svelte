<!-- 
@component
A component for rendering a boolean user setting on the profile page

Props:
    - `setting` (`UserSetting`) - The user setting to render
-->
<script lang="ts">
	import type { UserSetting } from "$lib/api/model";
	import Input from "$lib/components/ui/input/input.svelte";
	import Switch from "$lib/components/ui/switch/switch.svelte";
	import BaseSetting from "./BaseSetting.svelte";


    interface Props {
        setting: UserSetting
        getNewSettings: () => void
    }
    let { setting, getNewSettings }: Props = $props();

    $inspect(setting.value)
    
    let newValue = $derived(setting.value == true);
</script>

<BaseSetting {setting} newValue={newValue} getNewSettings={getNewSettings}>
    {#if newValue !== undefined && newValue !== null}
        <div class="flex flex-row gap-2 items-center">
            <input
                type="hidden"
                value="false"
                disabled={newValue}
            />

            <input
                type="checkbox"
                class="sr-only"
                value="true"
                bind:checked={newValue}
            />

            <Switch
                checked={newValue}
                onCheckedChange={() => (newValue = !newValue)}
                class="touch-manipulation"
            />

            <p>{newValue ? "True" : "False"}</p>
        </div>
    {/if}
</BaseSetting>