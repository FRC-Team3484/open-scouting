document.addEventListener("alpine:init", () => {
	Alpine.data("advanced_data", () => ({
		data: {},
		offline: false,
		year: JSON.parse(YEARS).reverse()[0],

		/**
		 * Creates a line chart using Chart.js
		 *
		 * @param {HTMLCanvasElement} canvas - The canvas element to render the chart on
		 * @param {number[]} data - The data to be displayed on the chart
		 * @param {string} label - The label to be displayed on the chart
		 * @param {string} type - The type of chart to be created
		 */
		create_line_chart(canvas, data, label, type) {
			const labels = data.map((_, i) => (i + 1).toString());

			const average = data.reduce((acc, val) => acc + val, 0) / data.length;

			const color =
				type === "auton_score" || type === "score" ? "#51ff4e" : "#ff4e51";

			new Chart(canvas, {
				type: "line",
				data: {
					labels: labels,
					datasets: [
						{
							label: `${label} Values`,
							data: data,
							borderWidth: 2,
							borderColor: color,
							fill: false,
						},
						{
							label: "Average Values",
							data: Array(data.length).fill(average),
							borderWidth: 1,
							borderColor: color,
							borderDash: [5, 5],
							fill: false,
							pointRadius: 0,
							pointBackgroundColor: `rgba(${color === "#51ff4e" ? 81 : 255}, ${color === "#51ff4e" ? 255 : 78}, 0.5)`,
						},
					],
				},
				options: {
					scales: {
						x: {
							display: true,
							title: {
								display: true,
								text: "Reports",
							},
						},
						y: {
							display: true,
							title: {
								display: true,
								text: "Values",
							},
						},
					},
				},
			});
		},

		/**
		 * Creates a donut chart using Chart.js
		 *
		 * @param {HTMLCanvasElement} element - The canvas element to render the chart on
		 * @param {number[]} data - The data to be displayed on the chart
		 * @param {string[]} labels - The labels to be displayed on the chart
		 * @param {string} title - The title of the chart
		 */
		create_donut_chart(element, data, labels, title) {
			const backgroundColors = labels.map((label) => {
				if (label === "true") {
					return "#4FBD4D";
				} else if (label === "false") {
					return "#ff4e51";
				}

				let default_colors = [
					"#36a2eb",
					"#ff6384",
					"#4bc0c0",
					"#ff9f40",
					"#9966ff",
					"#ffcd56",
					"#c9cbcf",
				];

				return default_colors[labels.indexOf(label) % default_colors.length];
			});

			new Chart(element, {
				type: "doughnut",
				data: {
					labels: labels,
					datasets: [
						{
							data: data,
							backgroundColor: backgroundColors,
						},
					],
				},
				options: {
					aspectRatio: 1,
					plugins: {
						title: {
							display: true,
							text:
								title.charAt(0).toUpperCase() +
								title.slice(1).replace(/_/g, " "),
						},
						legend: {
							position: "bottom",
							labels: {
								boxWidth: 10,
							},
						},
					},
				},
			});
		},

		init() {
			window.addEventListener("data", (event) => {
				event.stopImmediatePropagation();
				const { data } = event.detail;

				this.data = data;
			});

			setTimeout(() => {
				if (globalThis.offline) {
					this.offline = true;
				} else {
					this.offline = false;
				}
			}, 100);
		},
	}));
});
