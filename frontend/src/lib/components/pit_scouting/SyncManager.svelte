<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { ArrowClockwise, CheckCircle, CircleNotch, Warning, WifiSlash } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import Badge from "../ui/badge/badge.svelte";
	import { db } from "$lib/utils/db";
	import { onMount } from "svelte";
	import { online } from "svelte/reactivity/window";
	import { fetchPitScoutingData, pushPitScoutingData } from "$lib/utils/sync";
	import { slide } from "svelte/transition";
	import { liveQuery } from "dexie";
	import { toast } from "svelte-sonner";

    let { eventData, seasonUuid } = $props();

    type Status = "ready" | "fetching" | "pushing" | "warning" | "offline";
    let status: Status = $state("ready");

    let unsyncedQuery = liveQuery(() => db.pit_scouting.filter(p => p.synced === false && p.event_code === eventData.event_code && p.year === eventData.year).count());

    async function sync() {
        status = "pushing";
        await pushPitScoutingData(eventData, seasonUuid).then(async () => {
            status = "fetching";
            await fetchPitScoutingData(eventData, seasonUuid).then(() => {
                status = "ready";
            }).catch(() => {
                console.warn("Failed to fetch pit scouting data");
                toast.error("Failed to fetch pit scouting data");
            });
        }).catch(() => {
            console.warn("Failed to push pit scouting data");
            toast.error("Failed to push pit scouting data");
        });
    }

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
    <Card.Root class={`p-4 transition-colors ${status == "warning" ? "bg-destructive/30 !border-destructive/40 backdrop-blur-lg" : ""}`}>
        <div class="flex flex-row gap-2 items-center">
            {#if status != "offline"}
                <Button variant="outline" size="icon" onclick={sync}><ArrowClockwise weight="bold" /></Button>
            {/if}

            <div class="flex flex-col gap-2 items-start">
                <div class="flex flex-row gap-2 items-center">
                    {#if status === "ready"}
                        <CheckCircle weight="bold" />
                        <p class="text-sm">Up to Date</p>
                    {:else if status === "fetching"}
                        <CircleNotch weight="bold" class="animate-spin" />
                        <p class="text-sm">Fetching data...</p>
                    {:else if status === "pushing"}
                        <CircleNotch weight="bold" class="animate-spin" />
                        <p class="text-sm">Pushing data...</p>
                    {:else if status === "warning"}
                        <Warning weight="bold" class="animate-pulse" />
                        <p class="text-sm">Error syncing</p>
                    {:else if status === "offline"}
                        <WifiSlash weight="bold" class="animate-pulse" />
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
