document.addEventListener("alpine:init", () => {
	Alpine.data("filters", () => ({
		data: {},
		type: "",

		get_data() {
			fetch(`${SERVER_IP}/get_admin_data`, {
				method: "POST",
				headers: {
					"X-CSRFToken": CSRF_TOKEN,
				},
				body: JSON.stringify({
					type: this.type,
				}),
			})
				.then((response) => response.json())
				.then((data) => {
					this.data = data;
				});
		},

		init() {
			this.get_data();
		},
	}));
});
