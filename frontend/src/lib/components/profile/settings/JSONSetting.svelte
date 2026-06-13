<!-- 
@component
A component for rendering a JSON user setting on the profile page

Props:
    - `setting` (`UserSetting`) - The user setting to render
    - `getNewSettings` (`() => void`) - A function to get the new settings
-->
<script lang="ts">
	import type { UserSetting } from "$lib/api/model";
	import { Textarea } from "$lib/components/ui/textarea";
	import BaseSetting from "./BaseSetting.svelte";


    interface Props {
        setting: UserSetting
        getNewSettings: () => void
    }
    let { setting, getNewSettings }: Props = $props();
    
    let newValue = $derived(setting.value ?? {});
</script>

<BaseSetting {setting} newValue={JSON.stringify(newValue)} getNewSettings={getNewSettings}>
    <Textarea name={setting.key} bind:value={newValue} />
</BaseSetting>