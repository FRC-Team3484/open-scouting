<!-- 
@component
A component for rendering a number user setting on the profile page

Props:
    - `setting` (`UserSetting`) - The user setting to render
    - `getNewSettings` (`() => void`) - A function to get the new settings
-->
<script lang="ts">
	import type { UserSetting } from "$lib/api/model";
	import Input from "$lib/components/ui/input/input.svelte";
	import BaseSetting from "./BaseSetting.svelte";


    interface Props {
        setting: UserSetting
        getNewSettings: () => void
    }
    let { setting, getNewSettings }: Props = $props();
    
    let newValue = $derived(setting.value);
</script>

<BaseSetting {setting} newValue={newValue} getNewSettings={getNewSettings}>
    <Input type="number" name={setting.key} bind:value={newValue} />
</BaseSetting>