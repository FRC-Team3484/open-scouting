<script lang="ts">
    import * as Chart from "$lib/components/ui/chart";
    import { AreaChart, LineChart } from "layerchart";
    import * as Card from "$lib/components/ui/card";
	import { FieldDescription } from "../ui/field";

    let { field } = $props();

    let data = $state(null);

    const chartData = field.values
        .map(v => ({
            match_number: Number(v.match_number),
            value: Number(v.data),
        }))
        
    // const chartData = $derived(
    //     field.values
    //         .map(v => ({
    //             match_number: Number(v.match_number),
    //             value: Number(v.data),
    //         }))
    //         .toSorted((a, b) => a.match_number - b.match_number)
    // )

    // const chartData = [
    //     { match_number: 1, value: 1 },
    //     { match_number: 2, value: 2 },
    //     { match_number: 3, value: 3 },
    //     { match_number: 4, value: 4 },
    //     { match_number: 5, value: 5 },
    // ];

    // console.log(chartData)

    const chartConfig = {
        value: {
            label: field.field_name,
            color: "var(--chart-1)",
        }
    } satisfies Chart.ChartConfig;
</script>


<Card.Root>
    <Card.Content>
        <div class="flex flex-col gap-2">
            <p class="font-bold">{field.field_name}</p>

            <p class="text-sm">Average: {field.avg.toFixed(2)}</p>
            <p class="text-sm">Minimum: {field.min}</p>
            <p class="text-sm">Maximum: {field.max}</p>

            <Chart.Container config={chartConfig} class="min-w-64">
                <LineChart
                    data={field.values}
                    x="match_number"
                    axis="x"
                    legend={true}
                    points={{ r: 4 }}
                    series={[
                        {
                            key: "value",
                            label: chartConfig.value.label,
                            color: chartConfig.value.color
                        }
                    ]}
                />

            </Chart.Container>
        </div>
    </Card.Content>
</Card.Root>
