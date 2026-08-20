<!-- 
@component
Displays some basic server stats on the index page
-->
<script lang="ts">
	import { CircleNotchIcon, WarningIcon } from "phosphor-svelte";
        
    import * as Card from "$lib/components/ui/card/index.js";

	import type { ServerStatsResponse } from "$lib/api/model";
	import { getServerStatsStatusStatsGet } from "$lib/api/generic/generic";


    let stats: ServerStatsResponse = $state({
        seasons: 0,
        events_scouted: 0,
        match_scouting_submissions: 0,
        pits_scouted: 0
    });
    let loadingState: "loading" | "error" | "success" = $state("loading");

    /**
     * Get stats from the server
     */
    async function getStats() {
        loadingState = "loading";
        await getServerStatsStatusStatsGet().then((res) => {
            if (res.status !== 200) {
                console.error(res);
                loadingState = "error";
                return
            } else {
                stats = res.data
                loadingState = "success"
            }
        }).catch(() => {
            loadingState = "error";
        })
    }

    /**
     * Svelte action to run a function when an element is in view
     * @param node
     * @param callback
     */
    function runOnInView(node, callback) {
        const observer = new IntersectionObserver(([entry]) => {
        if (entry.isIntersecting) {
            callback();
            observer.unobserve(node); 
        }
        }, {
            threshold: 0.1
        });

        observer.observe(node);

        return {
            destroy() {
                observer.disconnect();
            }
        };
    }
</script>

<div class="flex flex-row gap-2 items-center mt-16 mb-4">
    <p class="text-2xl font-bold">Server Stats</p>

    {#if loadingState == "loading"}
        <CircleNotchIcon weight="bold" class="animate-spin" size={20} />
    {:else if loadingState == "error"}
        <WarningIcon weight="bold" size={20} />
    {/if}
</div>

<div class={`flex flex-row gap-2 items-center flex-wrap justify-center` + (loadingState == "loading" ? " animate-pulse" : "") + (loadingState == "error" ? " opacity-75" : "")} use:runOnInView={getStats}>
    <Card.Root>
        <Card.Content>
            <div class="flex flex-col text-left w-[80vw] sm:w-auto">
                <p class="text-xl font-mono">{stats?.seasons}</p>
                <p class="text-muted-foreground">{stats?.seasons == 1 ? "Season" : "Seasons"}</p>
            </div>
        </Card.Content>
    </Card.Root>
    
    <Card.Root>
        <Card.Content>
            <div class="flex flex-col text-left w-[80vw] sm:w-auto">
                <p class="text-xl font-mono">{stats?.events_scouted}</p>
                <p class="text-muted-foreground">{stats?.events_scouted == 1 ? "Event Scouted" : "Events Scouted"}</p>
            </div>
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Content>
            <div class="flex flex-col text-left w-[80vw] sm:w-auto">
                <p class="text-xl font-mono">{stats?.match_scouting_submissions}</p>
                <p class="text-muted-foreground">{stats?.match_scouting_submissions == 1 ? "Match Scouted" : "Matches Scouted"}</p>
            </div>
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Content>
            <div class="flex flex-col text-left w-[80vw] sm:w-auto">
                <p class="text-xl font-mono">{stats?.pits_scouted}</p>
                <p class="text-muted-foreground">{stats?.pits_scouted == 1 ? "Pit Scouted" : "Pits Scouted"}</p>
            </div>
        </Card.Content>
    </Card.Root>
</div>