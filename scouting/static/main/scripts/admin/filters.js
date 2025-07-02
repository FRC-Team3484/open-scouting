document.addEventListener("alpine:init", () => {
	Alpine.data("filters", () => ({
		data: {
			data: [],
			events: [],
			users: [],
			pits: [],
		},
		type: "",
		data_filters: {
			event: {
				open: false,
				items: [],
			},
			user: {
				open: false,
				items: [],
			},
		},
		event_filters: {
			year: {
				open: false,
				items: [],
			},
			name: {
				open: false,
				value: "",
			},
			event_code: {
				open: false,
				items: [],
			},
		},
		user_filters: {
			username: {
				open: false,
				items: [],
			},
			team_number: {
				open: false,
				items: [],
			},
		},
		pit_filters: {
			event: {
				open: false,
				items: [],
			},
			year: {
				open: false,
				items: [],
			},
		},

		get_data() {
			fetch(`${SERVER_IP}/get_admin_data`, {
				method: "POST",
				headers: {
					"X-CSRFToken": CSRF_TOKEN,
				},
				body: JSON.stringify({
					type: "",
				}),
			})
				.then((response) => response.json())
				.then((data) => {
					this.data = data;

					this.data.events_filtered = this.data.events;
					this.data.users_filtered = this.data.users;
				});
		},

		init() {
			this.data.events_filtered = [];

			this.get_data();
		},
	}));
});
