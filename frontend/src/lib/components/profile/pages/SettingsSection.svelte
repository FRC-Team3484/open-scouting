<!-- 
@component
The settings section on the profile page, for editing user settings

Props:
    - `settings` (`{[key: string]: UserSetting[]}`) - The user
    - `getNewSettings` (`() => void`) - A function to get the new settings
-->
<script lang="ts">
	import type { UserSetting } from "$lib/api/model";
	import Section from "./BaseSection.svelte";
	import SettingSectionHeader from "../settings/SettingSectionHeader.svelte";
	import StringSetting from "../settings/StringSetting.svelte";
	import NumberSetting from "../settings/NumberSetting.svelte";
	import BooleanSetting from "../settings/BooleanSetting.svelte";
	import JSONSetting from "../settings/JSONSetting.svelte";


    interface Props {
        settings: {[key: string]: UserSetting[]}
        getNewSettings: () => void
    }
    let { settings, getNewSettings }: Props = $props();
</script>
<Section title="Settings" description="Your settings">
    <div class="flex flex-col gap-2">
        {#each Object.entries(settings) as [section, settingsList]}
            <SettingSectionHeader name={section} />

            {#each settingsList as setting}
                {#if setting.type == "string"}
                    <StringSetting {setting} {getNewSettings} />
                {:else if setting.type == "number"}
                    <NumberSetting {setting} {getNewSettings} />
                {:else if setting.type == "boolean"}
                    <BooleanSetting {setting} {getNewSettings} />
                {:else if setting.type == "json"}
                    <JSONSetting {setting} {getNewSettings} />
                {:else}
                    <JSONSetting {setting} {getNewSettings} />
                {/if}
            {/each}
        {/each}
    </div>
</Section>