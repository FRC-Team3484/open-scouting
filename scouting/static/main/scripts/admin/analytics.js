document.addEventListener("alpine:init", () => {
	Alpine.data("analytics", () => ({
		open: false,
		one_hour: 0,
		twelve_hours: 0,
		twenty_four_hours: 0,
		three_days: 0,
		seven_days: 0,
		one_month: 0,
		three_months: 0,
		six_months: 0,
		one_year: 0,
		all_time: 0,

		async get_analytics() {
			fetch(`${SERVER_IP}/analytics/get_analytics`, {
				method: "POST",
				headers: {
					"X-CSRFToken": CSRF_TOKEN,
				},
			})
				.then((response) => response.json())
				.then((data) => {
					data = JSON.parse(data);
					this.one_hour = data["1_hour"];
					this.twelve_hours = data["12_hours"];
					this.twenty_four_hours = data["24_hours"];
					this.three_days = data["3_days"];
					this.seven_days = data["7_days"];
					this.one_month = data["1_month"];
					this.three_months = data["3_months"];
					this.six_months = data["6_months"];
					this.one_year = data["1_year"];
					this.all_time = data["all_time"];
				});
		},

		init() {
			this.get_analytics();
		},
	}));
});
