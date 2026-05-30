<!-- 
@component
The scatter chart for showing a score or miss stat

Props:
    - `fieldUuid` (`string`) - This field's UUID
    - `data` (`FlatData[]`) - Data from the parent
-->
<script lang="ts">
	import { defaultChartPadding, ScatterChart } from "layerchart";

	import type { FlatData } from "../CompareCharts.svelte";
    

    interface Props {
        fieldUuid: string
        data: FlatData[]
    }
    let { fieldUuid, data }: Props = $props();

    const chartData = $derived.by(() => {
        if (!data || !fieldUuid) return [];

        return data
            .map((team, i) => {
                const newField = team.fields.find(f => f.field_uuid === fieldUuid);
                if (!newField || !newField.values) return null;

                console.log("newField", newField);

                const data = newField.values
                    .filter(v => v.match_number != null && v.value != null)
                    .map(v => ({
                        match_number: Number(v.match_number),
                        value: Number(v.value)
                    }));

                if (!data.length) return null;

                const color = `var(--chart-${(i % 6) + 1})`;

                return {
                    key: `${team.team_number}`,
                    data,
                    color,
                    props: {
                        stroke: color,
                        fillOpacity: 0.4
                    }
                };
            })
            .filter(Boolean);
    });
</script>

<p class="text-left font-bold">
    {#if data[0]}
		{data[0].fields.find(f => f.field_uuid === fieldUuid)?.field_name}
	{/if}
</p>

<ScatterChart
    x="match_number"
    y="value"
    series={chartData}
    xNice
    yDomain={[0, null]}
    padding={defaultChartPadding({ top: 20, bottom: 48, left: 20, right: 20 })}
    height={400}
    legend
/>