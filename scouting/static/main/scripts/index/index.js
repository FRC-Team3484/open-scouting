document.addEventListener("alpine:init", () => {
	Alpine.data("index", () => ({
		page: 1,
		link: "",

		get_header_data(load_page) {
			window.dispatchEvent(
				new CustomEvent("get_header_data", {
					detail: { load_page },
				}),
			);
		},

		get_link_data() {
			window.dispatchEvent(new CustomEvent("get_link_data"));
		},

		load_page(page) {
			if (!this.demo) {
				if (page == "session") {
					console.log("This feature is coming soon");
				} else if (page == "contribute_separately") {
					if (!this.custom) {
						window.location.href = `${SERVER_IP}/contribute?username=${encodeURIComponent(this.username)}&team_number=${encodeURIComponent(this.team_number)}&event_name=${encodeURIComponent(this.event_name)}&event_code=${this.event_code}&year=${this.year}&`;
					} else {
						window.location.href = `${SERVER_IP}/contribute?username=${encodeURIComponent(this.username)}&team_number=${encodeURIComponent(this.team_number)}&event_name=${encodeURIComponent(this.event_name)}&event_code=${this.event_code}&year=${this.year}&custom=true&`;
					}
				} else if (page == "advanced_data") {
					window.location.href = `${SERVER_IP}/advanced_data?year=${this.year}&events=${this.event_code}`;
				} else if (page == "pit_scouting") {
					if (!this.custom) {
						window.location.href = `${SERVER_IP}/pits?username=${encodeURIComponent(this.username)}&team_number=${encodeURIComponent(this.team_number)}&event_name=${encodeURIComponent(this.event_name)}&event_code=${this.event_code}&year=${this.year}&`;
					} else {
						window.location.href = `${SERVER_IP}/pits?username=${encodeURIComponent(this.username)}&team_number=${encodeURIComponent(this.team_number)}&event_name=${encodeURIComponent(this.event_name)}&event_code=${this.event_code}&year=${this.year}&custom=true&`;
					}
				}
			} else {
				if (page == "session") {
					console.log("This feature is coming soon");
				} else if (page == "contribute_separately") {
					window.location.href = `${SERVER_IP}/contribute?year=${this.year}&demo=true&`;
				} else if (page == "advanced_data") {
					window.location.href = `${SERVER_IP}/advanced_data?year=${this.year}&events=${this.event_code}`;
				} else if (page == "pit_scouting") {
					window.location.href = `${SERVER_IP}/pits?year=${this.year}&demo=true&`;
				}
			}
		},

		async copy_event_link() {
			let link_to_event = `${SERVER_IP}/?year=${this.year}&event_name=${encodeURIComponent(this.event_name)}&event_code=${this.event_code}`;

			try {
				await navigator.clipboard.writeText(link_to_event);
				this.link = link_to_event;
				window.dispatchEvent(
					new CustomEvent("scouting_notification", {
						detail: {
							title: "Link copied",
							body: "The link to this event and year has been copied to your clipboard",
							icon: "check-circle",
						},
					}),
				);
			} catch (err) {
				console.error("Failed to copy: ", err);
			}
		},

		init() {
			window.addEventListener("start_over", (event) => {
				this.page = 1;
			});

			window.addEventListener("header_data", (event) => {
				event.stopImmediatePropagation();
				const {
					username,
					team_number,
					event_name,
					event_code,
					load_page,
					custom,
					year,
					demo,
				} = event.detail;

				this.username = username;
				this.team_number = team_number;
				this.event_name = event_name;
				this.event_code = event_code;
				this.custom = custom;
				this.year = year;
				this.demo = demo;
				this.load_page(load_page);
			});

			window.addEventListener("link_data", (event) => {
				event.stopImmediatePropagation();
				const {
					username,
					team_number,
					event_name,
					event_code,
					custom,
					year,
					demo,
				} = event.detail;

				this.username = username;
				this.team_number = team_number;
				this.event_name = event_name;
				this.event_code = event_code;
				this.custom = custom;
				this.year = year;
				this.demo = demo;
				this.copy_event_link();
			});
		},
	}));
});
