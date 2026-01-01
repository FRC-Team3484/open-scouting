<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Chart from "$lib/components/ui/chart/index.js";
	import { PieChart } from "layerchart";

    let { capability } = $props();

    const chartConfig = {
        percentage: {
            label: "Percentage",
            color: "var(--chart-1)"
        }
    } satisfies Chart.ChartConfig;
</script>

<Card.Root>
    <Card.Content>
        <p class="font-bold">{capability.field_name}</p>

        {#each capability.percentages as percentages}
            <p class="text-sm"><span class="font-bold">{percentages.value || "N/A"}</span> - {percentages.percentage}%</p>
        {/each}

        <Chart.Container config={chartConfig} class="min-w-64">
            <PieChart
                data={capability.percentages}
                key="value"
                value="percentage"
                legend={true}
            />
        </Chart.Container>
    </Card.Content>
</Card.Root>