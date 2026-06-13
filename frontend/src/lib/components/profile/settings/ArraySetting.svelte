<!-- 
@component
A component for rendering an array user setting on the profile page

Props:
    - `setting` (`UserSetting`) - The user setting to render
    - `getNewSettings` (`() => void`) - A function to get the new settings
-->
<script lang="ts">
	import type { UserSetting } from "$lib/api/model";
	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
	import { PlusCircleIcon, TrashIcon } from "phosphor-svelte";
	import BaseSetting from "./BaseSetting.svelte";


    interface Props {
        setting: UserSetting
        getNewSettings: () => void
    }
    let { setting, getNewSettings }: Props = $props();
    
    let newValue = $state<string[]>(
        Array.isArray(setting.value) ? [...setting.value] : []
    );
    $inspect(newValue)
</script>

<BaseSetting {setting} {newValue} {getNewSettings}>
    {#each newValue as _, index}
        <div class="flex flex-row gap-2">
            <Input type="text" bind:value={newValue[index]} />

            <Button
                variant="destructive"
                onclick={() => {
                    newValue = newValue.filter((_, i) => i !== index);
                }}
            >
                <TrashIcon weight="bold" />
            </Button>
        </div>
    {/each}

    <Button variant="outline" onclick={() => {newValue = [...newValue, ""];}}><PlusCircleIcon weight="bold" /> Add Item</Button>
</BaseSetting>