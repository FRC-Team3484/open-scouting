<!-- 
@component
The scatter chart for showing a score or miss stat

Props:
    - `field` (`Field`) - This field's info
    - `data` (`FlatData`) - Data from the parent
-->
<script lang="ts">
	import { defaultChartPadding, ScatterChart } from "layerchart";

	import type { Field } from "../../../../../routes/data/+page.svelte";
	import type { FlatData } from "../CompareCharts.svelte";
    

    interface Props {
        field: Field
        data: FlatData
    }
    let { field, data }: Props = $props();

    const chartData = $derived.by(() => {
        if (!data || !field) return [];

        return data
            .map((team, i) => {
                const newField = team.fields.find(f => f.field_uuid === field);
                if (!newField || !newField.values) return null;

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
    {data[0].fields.find(f => f.field_uuid === field).field_name}
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