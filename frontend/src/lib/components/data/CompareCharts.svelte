<script lang="ts">
	import * as Card from "$lib/components/ui/card";
	import CompareCapability from "./CompareCapability.svelte";
	import CompareScore from "./CompareScore.svelte";

    let { data, filters, fields } = $props();

    const flattenedData = $derived.by(() => {
        return data.map(team => {
            const fields = [
                ...Object.values(team.auton ?? {})
                    .flat()
                    .map(field => ({ ...field, stat_type: "score" })),

                ...Object.values(team.teleop ?? {})
                    .flat()
                    .map(field => ({ ...field, stat_type: "score" })),

                ...(team.capability ?? [])
                    .map(field => ({ ...field, stat_type: "capability" }))
            ];

            return {
                team_number: team.team_number,
                nickname: team.nickname,
                fields
            };
        });
    });
</script>

<Card.Root class="mt-2 lg:w-[50vh]">
    <Card.Content>
        <div class="flex flex-col gap-2">
            {#each filters.fields as field}
                {@const fieldData = fields.find(f => f.value === field)}
                {#if fieldData.stat_type === "autom_score" || fieldData.stat_type === "teleop_score" || fieldData.stat_type === "auton_miss" || fieldData.stat_type === "teleop_miss"}
                    <CompareScore field={field} data={flattenedData} />
                {:else if fieldData.stat_type === "capability"}
                    <CompareCapability field={field} data={flattenedData} />
                {/if}
            {/each}
        </div>
    </Card.Content>
</Card.Root>