<script lang="ts">
	import { BarChart, defaultChartPadding } from "layerchart";

	let { field, data } = $props();

	const barSeries = $derived.by(() => {
		if (!data || !field) return [];

		const categoriesSet = new Set<string>();
		data.forEach(team => {
			const f = team.fields.find(f => f.field_uuid === field);
			if (f?.percentages) f.percentages.forEach(p => categoriesSet.add(p.value || "na"));
		});
		const categories = Array.from(categoriesSet);

		return data
			.map((team, i) => {
				const f = team.fields.find(f => f.field_uuid === field);
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
	{data[0].fields.find(f => f.field_uuid === field)?.field_name}
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