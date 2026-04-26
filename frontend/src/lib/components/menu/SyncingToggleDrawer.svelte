<script lang="ts">
    import * as Sheet from "$lib/components/ui/sheet";
	import { CircleNotchIcon, CloudCheckIcon, CloudSlashIcon, XCircleIcon } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import { Separator } from "../ui/separator";
	import DrawerHeader from "../generic/drawers/DrawerHeader.svelte";
    import { syncStatus } from "$lib/stores/sync";
	import { fetchEventData, fetchSeasonData, pushMatchScoutingData, pushUnsyncedPitScoutingData } from "$lib/utils/sync";
	import { toast } from "svelte-sonner";

    let open = $state(false);
    let syncing = $state(false);

    async function sync() {
        syncing = true;
        try {
            await fetchSeasonData();
            await fetchEventData();
            await pushMatchScoutingData();
            await pushUnsyncedPitScoutingData();
    
            toast.success("Data has been synced!", { duration: 5000 });
            syncing = false;
            open = false;
        } catch {
            toast.warning("Failed to sync data", { duration: 5000 });
        }
    }
</script>

<Sheet.Root bind:open={open}>
    <Sheet.Trigger>
        {#if $syncStatus}
            <Button variant="outline" class="w-full"><CloudSlashIcon weight="bold" /> Disable Syncing</Button>
        {:else}
            <Button variant="outline" class="w-full"><CloudCheckIcon weight="bold" /> Enable Syncing</Button>
        {/if}
    </Sheet.Trigger>
    <Sheet.Content class="max-h-[80vh] overflow-y-scroll lg:mx-64 2xl:mx-128 border-1 p-4 rounded-t-lg" side="bottom">
        <div class="overflow-y-scroll pr-2">
            {#if $syncStatus && !syncing}
                <DrawerHeader title="Disable Syncing?" description="" />
            {:else if !$syncStatus || syncing}
                <DrawerHeader title="Enable Syncing?" description="" />
            {/if}
            <Separator orientation="horizontal" class="mb-4" />

            {#if $syncStatus && !syncing}
                <div class="flex flex-row gap-2 items-center">
                    <CloudSlashIcon weight="bold" size={32} />
                    <p>This will prevent your data from being synced to the server, and stop new data from being fetched.</p>
                </div>
            {:else if !$syncStatus || syncing}
                <div class="flex flex-row gap-2 items-center">
                    <CloudCheckIcon weight="bold" size={32} />
                    <p>This will resume syncing your data to the server, and allow fetching new data.</p>
                </div>
            {/if}

            {#if $syncStatus && !syncing}
                <ul class="list-disc list-inside ml-8">
                    <li class="mt-2">This may be useful when you have a poor internet connection, to stop your device from constantly trying to make requests to the server.</li>
                    <li>Your scouting reports and pit scouting data will remain stored locally until you manually re-enable syncing.</li>
                    <li>You can always manually sync data using the "Manage Local Data" button in the menu.</li>
                </ul>
            {:else if !$syncStatus || syncing}
                <ul class="list-disc list-inside ml-8">
                    <li class="mt-2">Your scouting reports and pit scouting data will be immediately synced with the server, and new season and event data will be fetched.</li>
                    <li>You can always manually sync data using the "Manage Local Data" button in the menu.</li>
                </ul>
            {/if}
            
            <div class="flex flex-col gap-2 w-full mt-4">
                {#if !$syncStatus || syncing}
                    <Button class="w-full" onclick={() => {syncStatus.set(true); sync();}} disabled={syncing}>
                        {#if syncing}
                            <CircleNotchIcon weight="bold" class="animate-spin" />
                        {:else}
                            <CloudCheckIcon weight="bold" /> 
                        {/if}
                        Enable Syncing
                    </Button>
                {/if}

                <Sheet.Close class="flex flex-col gap-2 w-full">
                    {#if $syncStatus && !syncing}
                        <Button class="w-full" onclick={() => {syncStatus.set(false)}}><CloudSlashIcon weight="bold" /> Disable Syncing</Button>
                    {/if}

                    <Button variant="outline" class="w-full" disabled={syncing}><XCircleIcon /> Close</Button>
                </Sheet.Close>
            </div>
        </div>
    </Sheet.Content>
</Sheet.Root>