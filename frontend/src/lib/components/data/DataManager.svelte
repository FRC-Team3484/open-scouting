<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { apiFetch } from "$lib/utils/api";
	import { ArrowClockwise, CircleNotch } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import TeamData from "./TeamData.svelte";
	import { toast } from "svelte-sonner";
	import Separator from "../ui/separator/separator.svelte";

    let { filters } = $props();

    let data = $state(null);
    let loadConfirmed = $state(false);

    async function loadData() {
        if (filters.year > 0) {
            const params = new URLSearchParams();
            params.set("year", String(filters.year));

            if (filters.event_codes.length) {
                params.set("event_codes", filters.event_codes.join(","));
            }

            if (filters.team_numbers.length) {
                params.set("team_numbers", filters.team_numbers.join(","));
            }

            const dataRequest = await apiFetch(
                `/data/get?${params.toString()}`
            ).then((response) => {
                data = response;
            }).catch((e) => {
                console.error(e);
                data = "error";
                toast.error("Error loading data", { duration: 5000 });
            });

            console.log(data);
        }
    }

    $effect(() => {
        // Don't load data unless a filter has been selected, because unfiltered data may take a long time to render
        if (filters.year != 0 && filters.event_codes.length > 0 || filters.team_numbers.length > 0) {
            loadConfirmed = true;
            loadData();
        } else {
            loadConfirmed = false;
        }
    });
</script>

{#if !loadConfirmed && filters.year != 0}
    <Card.Root class="my-4 items-center">
        <Card.Content class="max-w-64">
            <div class="flex flex-col gap-2">
                <p class="font-bold">Load data?</p>
                <p class="text-sm text-muted-foreground">All data (with no filters) may take a long time to load, so it's not loaded by default.</p>
                <Button onclick={() => {loadData(); loadConfirmed = true}}>Load Anyway</Button>
            </div>
        </Card.Content>
    </Card.Root>
{:else if filters.year != 0}
    {#if data == null}
        <CircleNotch weight="bold" class="animate-spin my-4" size={24} />
    {:else if data.length == 0}
        <div class="flex flex-col gap-1 my-4 flex-wrap max-w-64">
            <p class="text-muted-foreground">No data found</p>
            <p class="text-muted-foreground text-sm">Please check your filters and try again</p>
        </div>
    {:else if data == "error"}
        <div class="flex flex-col gap-1 my-4 flex-wrap max-w-64">
            <p class="text-muted-foreground">Error loading data</p>
            <p class="text-muted-foreground text-sm">Recieved an invalid response from the backend. Please check your filters and try again</p>
        </div>
    {:else}
        <div class="flex flex-col gap-4 my-4">
            <Card.Root>
                <Card.Content>
                    <div class="flex flex-row gap-2 items-center">
                        <p class="text-sm text-muted-foreground">Loaded {data.length} {data.length == 1 ? "team" : "teams"} with data</p>
                        <Button size="sm" variant="outline" onclick={() => loadData()}><ArrowClockwise weight="bold" /> Refresh</Button>
                    </div>
                </Card.Content>
            </Card.Root>

            <Separator orientation="horizontal" />

            {#each data as team}
                <TeamData team={team} />
            {/each}
        </div>
    {/if}
{/if}