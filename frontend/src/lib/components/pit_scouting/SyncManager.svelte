<!-- 
@component
Sync manager component for the pit scouting page

TODO: Respect the user's syncing setting
TODO: Make the 100ms delay to ensure seasonUuid has loaded more reliable
TODO: Make the pit scouting sync frequency configurable
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { online } from "svelte/reactivity/window";
	import { slide } from "svelte/transition";
	import { liveQuery } from "dexie";
	import { toast } from "svelte-sonner";
	import { ArrowClockwiseIcon, CheckCircleIcon, CircleNotchIcon, WarningIcon, WifiSlashIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";
	import Button from "../ui/button/button.svelte";
	import Badge from "../ui/badge/badge.svelte";

	import { db, type Event } from "$lib/utils/db";
	import { fetchPitScoutingData, pushPitScoutingData } from "$lib/utils/sync";


    interface Props {
        eventData: Event
        seasonUuid: string
    }
    let { eventData, seasonUuid }: Props = $props();

    type Status = "ready" | "fetching" | "pushing" | "warning" | "offline";
    let status: Status = $state("ready");

    let unsyncedQuery = liveQuery(() => db.pit_scouting.filter(p => p.synced === false && p.event_code === eventData.event_code && p.year === eventData.year).count());

    /**
     * Sync the pit scouting data
     */
    async function sync() {
        status = "pushing";
        await pushPitScoutingData(eventData, seasonUuid).then(async () => {
            status = "fetching";
            await fetchPitScoutingData(eventData, seasonUuid).then(() => {
                status = "ready";
            }).catch((error) => {
                console.warn("Failed to fetch pit scouting data", error);
                toast.error("Failed to fetch pit scouting data");
            });
        }).catch((error) => {
            console.warn("Failed to push pit scouting data", error);
            toast.error("Failed to push pit scouting data");
        });
    }

    /**
     * Sync the pit scouting data when the page is mounted
     * 
     * Then, create the interval for syncing the page every 10 seconds
     */
    onMount(() => {
        // Delay by 100ms to ensure season_uuid has been fetched
        // TODO: Make this more reliable later
        setTimeout(() => {        
            if (online.current) {
                sync();
            }
        }, 100);

        const interval = setInterval(async () => {
            if (online.current) {
                sync();
            }
        }, 10000);

        return () => {
            clearInterval(interval);
        }
    });
</script>

<div class="fixed bottom-0 left-0 ml-2 mb-2">
    <Card.Root class={`p-4 transition-colors ${status == "warning" ? "bg-destructive/30 border-destructive/40! backdrop-blur-lg" : ""}`}>
        <div class="flex flex-row gap-2 items-center">
            {#if status != "offline"}
                <Button variant="outline" size="icon" onclick={sync}><ArrowClockwiseIcon weight="bold" /></Button>
            {/if}

            <div class="flex flex-col gap-2 items-start">
                <div class="flex flex-row gap-2 items-center">
                    {#if status === "ready"}
                        <CheckCircleIcon weight="bold" />
                        <p class="text-sm">Up to Date</p>
                    {:else if status === "fetching"}
                        <CircleNotchIcon weight="bold" class="animate-spin" />
                        <p class="text-sm">Fetching data...</p>
                    {:else if status === "pushing"}
                        <CircleNotchIcon weight="bold" class="animate-spin" />
                        <p class="text-sm">Pushing data...</p>
                    {:else if status === "warning"}
                        <WarningIcon weight="bold" class="animate-pulse" />
                        <p class="text-sm">Error syncing</p>
                    {:else if status === "offline"}
                        <WifiSlashIcon weight="bold" class="animate-pulse" />
                        <p class="text-sm">Offline</p>
                    {/if}
                </div>

                {#if $unsyncedQuery > 0}
                    <div transition:slide>
                        <Badge variant="destructive">{$unsyncedQuery} Unsynced Pit</Badge>
                    </div>
                {/if}
            </div>
        </div>
    </Card.Root>
</div>
