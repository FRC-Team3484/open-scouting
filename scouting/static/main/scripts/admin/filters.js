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

					this.update_display();
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

			this.update_display();
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

					window.dispatchEvent(
						new CustomEvent("scouting_notification", {
							detail: {
								title: "Success",
								message: "The admin operation was successful",
								type: "success",
								icon: "check-circle",
							},
						}),
					);
				});
		},

		update_display() {
			if (this.type === "data") {
				this.data.data_display = this.data.data.filter((item) => {
					const eventMatch =
						this.data_filters.event.items.length === 0 ||
						this.data_filters.event.items.some(
							(e) => e.event_code === item.event_code,
						);
					const userMatch =
						this.data_filters.user.items.length === 0 ||
						this.data_filters.user.items.some(
							(u) => u.username === item.user.username,
						);
					return eventMatch && userMatch;
				});
			} else if (this.type === "event") {
				this.data.events_display = this.data.events.filter((item) => {
					const nameMatch = item.name
						.toLowerCase()
						.includes(this.event_filters.name.value.toLowerCase());
					const yearMatch =
						this.event_filters.year.items.length === 0 ||
						this.event_filters.year.items.includes(item.year);
					const codeMatch =
						this.event_filters.event_code.items.length === 0 ||
						this.event_filters.event_code.items.includes(item.event_code);
					return nameMatch && yearMatch && codeMatch;
				});
			} else if (this.type === "user") {
				this.data.users_display = this.data.users.filter((item) => {
					const usernameMatch =
						this.user_filters.username.items.length === 0 ||
						this.user_filters.username.items.includes(item.username);
					const teamMatch =
						this.user_filters.team_number.items.length === 0 ||
						this.user_filters.team_number.items.includes(item.team_number);
					return usernameMatch && teamMatch;
				});
			} else if (this.type === "pit") {
				this.data.pits_display = this.data.pits.filter((item) => {
					const eventMatch =
						this.pit_filters.event.items.length === 0 ||
						this.pit_filters.event.items.some(
							(e) => e.event_code === item.event_code,
						);
					const yearMatch =
						this.pit_filters.year.items.length === 0 ||
						this.pit_filters.year.items.includes(item.year);
					return eventMatch && yearMatch;
				});
			}
		},

		init() {
			this.data.events_filtered = [];
			this.data.users_filtered = [];
			this.data.pits_filtered = [];

			this.data.data_display = [];
			this.data.events_display = [];
			this.data.users_display = [];
			this.data.pits_display = [];

			this.get_data();

			setTimeout(() => {
				window.dispatchEvent(
					new CustomEvent("dialog_show", {
						detail: {
							event_name: "admin_warning",
							title: "Actions made here are irreversible",
							body: "By using this admin dashboard, be warned that any action you take is irreversible (deleting data, etc.). You will not be asked to confirm any actions beyond this dialog. Use caution when interacting on this page.",
							buttons: [
								{
									type: "confirm",
									icon: "ph-bold ph-check",
									text: "I understand",
								},
							],
						},
					}),
				);
			}, 300);
		},
	}));
});
