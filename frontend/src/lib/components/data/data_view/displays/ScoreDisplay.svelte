<script lang="ts">
    import { ScatterChart } from "layerchart";
    import * as Card from "$lib/components/ui/card";

    let { field } = $props();
</script>


<Card.Root>
    <Card.Content>
        <div class="flex flex-col gap-2">
            <p class="font-bold">{field.field_name}</p>

            <p class="text-sm">Average: {field.avg.toFixed(2)}</p>
            <p class="text-sm">Minimum: {field.min}</p>
            <p class="text-sm">Maximum: {field.max}</p>

            <ScatterChart 
                data={field.values} 
                x="match_number" 
                y="value" 
                height={400} 
                cRange={["var(--chart-1)"]} 
                annotations={[
                {
                    type: 'line',
                    label: 'Average',
                    labelXOffset: 4,
                    labelYOffset: 2,
                    y: field.avg,
                    props: {
                        label: { class: 'text-chart-1' },
                        line: { class: '[stroke-dasharray:2,2] stroke-chart-1' }
                    }
                }
            ]}
            />
        </div>
    </Card.Content>
</Card.Root>
