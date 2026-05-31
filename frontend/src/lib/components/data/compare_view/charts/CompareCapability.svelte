<!-- 
@component
The bar chart for showing a capability stat

Props:
    - `fieldUuid` (`string`) - This field's UUID
    - `data` (`FlatData[]`) - Data from the parent
-->
<script lang="ts">
	import { BarChart, defaultChartPadding } from "layerchart";

	import type { FlatData } from "../CompareCharts.svelte";

	
	interface Props {
		fieldUuid: string,
		data: FlatData[]
	}
	let { fieldUuid, data }: Props = $props();

	const barSeries = $derived.by(() => {
		if (!data || !fieldUuid) return [];

		const categoriesSet = new Set<string>();
		data.forEach(team => {
			const f = team.fields.find(f => f.field_uuid === fieldUuid);
			if (f?.stat_type !== "capability") return;
			if (f?.percentages) f.percentages.forEach(p => categoriesSet.add(p.value || "na"));
		});
		const categories = Array.from(categoriesSet);

		return data
			.map((team, i) => {
				const f = team.fields.find(f => f.field_uuid === fieldUuid);
				if (f?.stat_type !== "capability") return;
				if (!f?.percentages) return null;

				const seriesData = categories.map(cat => {
					const p = f.percentages.find(p => (p.value || "na") === cat);
					return {
						category: cat,
						value: p ? p.percentage : 0
					};
				});

                const color = `var(--chart-${(i % 6) + 1})`;

				return {
					key: team.team_number,
					data: seriesData,
					color: color
				};
			})
			.filter(Boolean);
	});
</script>

<p class="font-bold text-left">
	{#if data[0]}
		{data[0].fields.find(f => f.field_uuid === fieldUuid)?.field_name}
	{/if}
</p>

<BarChart
	series={barSeries}
	x="category"
	y="value"
	color="color"
	padding={defaultChartPadding({ top: 20, bottom: 48, left: 20, right: 20 })}
	height={400}
	legend
/>