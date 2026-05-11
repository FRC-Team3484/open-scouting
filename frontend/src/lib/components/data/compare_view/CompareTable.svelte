<!-- 
@component
Renders the table for comparing data between teams in the compare view on the data page
-->
<script lang="ts">
    import * as Table from "$lib/components/ui/table";
    import * as Card from "$lib/components/ui/card";

	import BaseDialog from "../../generic/dialogs/BaseDialog.svelte";
	import type { CompareFilters, Field } from "../../../../routes/data/+page.svelte";


    interface Props {
        data: unknown
        filters: CompareFilters
        fields: Field[]
    }
    let { data, filters, fields }: Props = $props();

    let allValuesOpen: boolean = $state(false);
    let allValuesValues: string[] = $state([]);
    let allValuesType: string = $state("dict");
    let allValuesFieldName: string = $state("");

    /**
     * Given an array of values, find the highest one
     * @param values
     */
    function highestValue(values: string[]) {
        if (!values) return "";

        const [k, v] = Object.entries(values).reduce((a, b) => b[1] > a[1] ? b : a);

        const label = k === "" ? "N/A" : k;
        return `${label}: ${v}%`;
    }

    /**
     * Show all values 
     * 
     * Used when the user clicks on a cell that's only showing the average
     * 
     * @param values The values to show
     * @param fieldName The name of the field to show values for
     * @param type The type of the field
     */
    function showAllValues(values: any, fieldName: string, type: "array" | "dict" = "dict") {
        allValuesOpen = true;
        allValuesValues = values;
        allValuesType = type;
        allValuesFieldName = fieldName;
    }
</script>

<Card.Root class="p-2 lg:max-w-[70vw] lg:min-w-[50vw] mt-2 max-w-screen">
    <Card.Content class="overflow-x-auto p-2">
        {#if data.length == 0}
            <p class="text-muted-foreground">No data found</p>
        {:else if filters.fields.length == 0}
            <p class="text-muted-foreground">No fields selected</p>
            <p class="text-sm text-muted-foreground">Please select at least one field to view the table</p>
        {:else}
            <Table.Root>
                <Table.Caption class="text-left">
                    Click a cell to see all values
                </Table.Caption>
            
                <Table.Header>
                    <Table.Row>
                        <Table.Head class="font-bold border text-left sticky left-0 bg-card/50 backdrop-blur-xs z-20">
                            Team
                        </Table.Head>
        
                        {#each filters.fields as field}
                            <Table.Head class="font-bold border text-left">{fields.find(f => f.value === field)?.name}</Table.Head>
                        {/each}
                    </Table.Row>
        
                </Table.Header>
            
                <Table.Body>
                    {#each data as team}
                        <Table.Row>
                            <Table.Cell class="font-bold border text-left sticky left-0 bg-card/50 backdrop-blur-xs z-10">
                                {team.team_number}
                            </Table.Cell>
        
                            {#each filters.fields as field}
                                {#if team["summary"].find(f => f.field_uuid === field)?.stat_type == "capability"}
                                    <Table.Cell 
                                        class="border text-left" 
                                        onclick={() => showAllValues(
                                            team["summary"].find(f => f.field_uuid === field)?.values, 
                                            team["summary"].find(f => f.field_uuid === field)?.field_name, 
                                            "dict"
                                        )}
                                    >
                                        {highestValue(team["summary"].find(f => f.field_uuid === field)?.values)}
                                    </Table.Cell>
                                {:else}
                                    <Table.Cell 
                                        class="border text-left" 
                                        onclick={() => showAllValues(
                                            team["summary"].find(f => f.field_uuid === field)?.values, 
                                            team["summary"].find(f => f.field_uuid === field)?.field_name, 
                                            "array"
                                        )}
                                    >
                                        {team["summary"].find(f => f.field_uuid === field)?.avg.toFixed(2)}
                                    </Table.Cell>
                                {/if}
                            {/each}
                        </Table.Row>
        
                    {/each}
                </Table.Body>
            </Table.Root>
        {/if}
    </Card.Content>
</Card.Root>

<BaseDialog title="All Values" description={`All values for ${allValuesFieldName}`} bind:open={allValuesOpen}>
    {#if allValuesType == "dict"}
        {#each Object.entries(allValuesValues) as [key, value]}
            <p>{key || "N/A"}: {value}%</p>
        {/each}
    {:else}
        {#each allValuesValues as value}
            <p>{value}</p>
        {/each}
    {/if}
</BaseDialog>