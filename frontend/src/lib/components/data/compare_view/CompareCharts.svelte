<!-- 
@component
Renders the charts for the compare chart view mode on the data page

Props:
    - `data` (`unknown`) The data for the chart
    - `filters` (`CompareFilters`) The current filters
    - `fields` (`Field[]`) The avaliable field filters
-->
<script lang="ts" module>
    export interface FlatData {
        team_number: number
        nickname: string
        fields: any
    }
</script>

<script lang="ts">
	import * as Card from "$lib/components/ui/card";
	import type { CompareFilters, Field } from "../../../../routes/data/+page.svelte";
	import CompareCapability from "./charts/CompareCapability.svelte";
	import CompareScore from "./charts/CompareScore.svelte";


    interface Props {
        data: unknown
        filters: CompareFilters
        fields: Field[]
    }
    let { data, filters, fields }: Props = $props();

    
    const flattenedData: FlatData[] = $derived.by(() => {
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

<Card.Root class="p-2 lg:max-w-[70vw] lg:min-w-[50vw] mt-2">
    <Card.Content class="overflow-x-auto p-2">
        {#if data.length == 0}
            <p class="text-muted-foreground">No data found</p>
        {:else if filters.fields.length == 0}
            <p class="text-muted-foreground">No fields selected</p>
            <p class="text-sm text-muted-foreground">Please select at least one field to view charts</p>
        {:else}
            <div class="flex flex-col gap-2">
                {#each filters.fields as field}
                    {@const fieldData = fields.find(f => f.value === field)}
                    {#if fieldData}
                        {#if fieldData.stat_type === "autom_score" || fieldData.stat_type === "teleop_score" || fieldData.stat_type === "auton_miss" || fieldData.stat_type === "teleop_miss"}
                            <CompareScore field={field} data={flattenedData} />
                        {:else if fieldData.stat_type === "capability"}
                            <CompareCapability field={field} data={flattenedData} />
                        {/if}
                    {:else}
                        <p class="text-sm text-muted-foreground">Failed to load field data</p>
                    {/if}
                {/each}
            </div>
        {/if}
    </Card.Content>
</Card.Root>