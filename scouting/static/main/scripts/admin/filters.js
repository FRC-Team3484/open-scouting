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
					this.data.pits_filtered = this.data.pits;
				});
		},

		clear_filters() {
			this.data_filters.event.items = [];
			this.data_filters.user.items = [];

			this.event_filters.year.items = [];
			this.event_filters.name.value = "";
			this.event_filters.event_code.items = [];

			this.user_filters.username.items = [];
			this.user_filters.team_number.items = [];

			this.pit_filters.event.items = [];
			this.pit_filters.year.items = [];
		},

		download_json(data, file_name) {
			const blob = new Blob([JSON.stringify(data)], {
				type: "application/json",
			});
			const link = document.createElement("a");
			link.href = window.URL.createObjectURL(blob);
			link.download = file_name;
			link.click();
		},

		do_admin_operation(type, operation, data) {
			fetch(`${SERVER_IP}/do_admin_operation`, {
				method: "POST",
				headers: {
					"X-CSRFToken": CSRF_TOKEN,
				},
				body: JSON.stringify({
					type: type,
					operation: operation,
					data: data,
				}),
			})
				.then((response) => response.text())
				.then((data) => {
					this.get_data();
				});
		},

		init() {
			this.data.events_filtered = [];
			this.data.users_filtered = [];
			this.data.pits_filtered = [];

			this.get_data();
		},
	}));
});
