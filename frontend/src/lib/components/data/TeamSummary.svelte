<script lang="ts">
	import Separator from "../ui/separator/separator.svelte";
	import BaseTeamFolder from "./BaseTeamFolder.svelte";

    let { fields } = $props();

    let scoreFields = $derived(fields.filter((f) => f.stat_type === "teleop_score" || f.stat_type === "autom_score" || f.stat_type === "teleop_miss" || f.stat_type === "auton_miss"));
    let capabilityFields = $derived(fields.filter((f) => f.stat_type === "capability"));
</script>

<BaseTeamFolder title="Summary" expanded={true}>
    <div class="flex flex-col gap-1 text-left">
        <p>Score and Miss Averages</p>
        {#each scoreFields as field}
            <div class="flex flex-row gap-2 text-sm ml-4 flex-wrap mb-1">
                <p class="font-bold">{field.field_name}</p>
                <Separator orientation="vertical" class="mx-1" />
                <p>{field.avg}</p>
            </div>
        {/each}
        <p class="mt-2">Capabilities</p>
        {#each capabilityFields as field}
            <div class="flex flex-row gap-1 text-sm ml-4 flex-wrap mb-1">
                <p class="font-bold">{field.field_name}</p>
                <Separator orientation="vertical" class="mx-1" />
                {#each Object.entries(field.values) as [key, value]}
                    <div class="flex flex-row gap-1 text-sm mr-1">
                        {#if key == "na"}
                            <p class="text-muted-foreground">N/A</p>
                        {:else if key == "true"}
                            <p class="text-green-300">True</p>
                        {:else if key == "false"}
                            <p class="text-red-400">False</p>
                        {:else}
                            <p>{key}</p>
                        {/if}
                        <p>{value}%</p>
                    </div>
                {/each}
            </div>
        {/each}
    </div>
</BaseTeamFolder>
