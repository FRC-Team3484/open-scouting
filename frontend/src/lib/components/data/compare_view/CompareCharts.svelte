<!-- 
@component
Renders the charts for the compare chart view mode on the data page

Props:
    - `data` (`DataTeamResponse[]`) The data for the chart
    - `filters` (`CompareFilters`) The current filters
    - `fields` (`Field[]`) The avaliable field filters
-->
<script lang="ts" module>
    type FlatField =
        | (DataNumericStatEntry & {
            stat_type: "score";
        })
        | (DataCapabilityStatEntry & {
            stat_type: "capability";
        });

    export interface FlatData {
        team_number: number;
        nickname: string | null;
        fields: FlatField[];
    }
</script>

<script lang="ts">
	import type { DataCapabilityStatEntry, DataNumericStatEntry, DataTeamResponse } from "$lib/api/model";

	import * as Card from "$lib/components/ui/card";
	import type { CompareFilters, Field } from "../../../../routes/data/+page.svelte";
	import CompareCapability from "./charts/CompareCapability.svelte";
	import CompareScore from "./charts/CompareScore.svelte";


    interface Props {
        data: DataTeamResponse[]
        filters: CompareFilters
        fields: Field[]
    }
    let { data, filters, fields }: Props = $props();

    
    const flattenedData: FlatData[] = $derived.by(() => {
        return data.map(team => {
            const fields: FlatField[] = [
                ...Object.values(team.auton ?? {})
                    .flat()
                    .map(field => ({
                        ...field,
                        stat_type: "score" as const
                    })),

                ...Object.values(team.teleop ?? {})
                    .flat()
                    .map(field => ({
                        ...field,
                        stat_type: "score" as const
                    })),

                ...(team.capability ?? []).map(field => ({
                    ...field,
                    stat_type: "capability" as const
                }))
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
                        {#if fieldData.stat_type === "auton_score" || fieldData.stat_type === "teleop_score" || fieldData.stat_type === "auton_miss" || fieldData.stat_type === "teleop_miss"}
                            <CompareScore fieldUuid={field} data={flattenedData} />
                        {:else if fieldData.stat_type === "capability"}
                            <CompareCapability fieldUuid={field} data={flattenedData} />
                        {/if}
                    {:else}
                        <p class="text-sm text-muted-foreground">Failed to load field data</p>
                    {/if}
                {/each}
            </div>
        {/if}
    </Card.Content>
</Card.Root>