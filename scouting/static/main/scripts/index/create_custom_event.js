document.addEventListener("alpine:init", () => {
	Alpine.data("create_custom_event", () => ({
		shown: false,
		YEARS: YEARS.reverse(),
		selected_year: null,
		able_to_submit: false,

		update_date_fields(e) {
			this.selected_year = e.target.value;

			this.$refs.date_begins.min = `${this.selected_year}-01-01`;
			this.$refs.date_begins.max = `${this.selected_year}-12-31`;
			this.$refs.date_ends.min = `${this.selected_year}-01-01`;
			this.$refs.date_ends.max = `${this.selected_year}-12-31`;
		},

		check_date_fields() {
			let date_begins_value = new Date(
				Date.parse(this.$refs.date_begins.value),
			);
			let date_ends_value = new Date(Date.parse(this.$refs.date_ends.value));
			let valid = false;

			if (!this.$refs.date_begins.checkValidity()) {
				this.$refs.date_begins.value = `${this.selected_year}-${date_begins_value.getMonth()}-${date_begins_value.getDate()}`;
			}

			if (!this.$refs.date_ends.checkValidity()) {
				this.$refs.date_ends.value = `${this.selected_year}-${date_begins_value.getMonth()}-${date_begins_value.getDate()}`;
			}

			this.check_fields();
		},

		check_fields() {
			if (
				this.$refs.date_begins.value == "" ||
				this.$refs.date_ends.value == "" ||
				this.$refs.name.value == "" ||
				this.$refs.location.value == "" ||
				this.$refs.type.value == "N/A"
			) {
				valid = false;
			} else {
				valid = true;
			}

			if (valid) {
				this.able_to_submit = true;
			} else {
				this.able_to_submit = false;
			}
		},

		async create_event() {
			const response = await fetch(`${SERVER_IP}/create_custom_event`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": CSRF_TOKEN,
				},
				body: JSON.stringify({
					name: this.$refs.name.value,
					year: this.$refs.year.value,
					date_begins: this.$refs.date_begins.value,
					date_ends: this.$refs.date_ends.value,
					location: this.$refs.location.value,
					type: this.$refs.type.value,
				}),
			});

			response.text().then(async (text) => {
				if (response.ok) {
					this.close_dialog();
					window.dispatchEvent(new CustomEvent("refresh_event_list"));
				}
			});
		},

		close_dialog() {
			this.shown = false;

			this.$refs.name.value = "";
			this.$refs.date_begins.value = "";
			this.$refs.date_ends.value = "";
			this.$refs.location.value = "";
			this.$refs.type.value = "N/A";
		},

		init() {
			window.addEventListener("open_create_custom_event", (event) => {
				event.stopImmediatePropagation();

				this.shown = true;
			});

			this.selected_year = this.YEARS[0];
			this.$refs.date_begins.min = `${this.selected_year}-01-01`;
			this.$refs.date_begins.max = `${this.selected_year}-12-31`;
			this.$refs.date_ends.min = `${this.selected_year}-01-01`;
			this.$refs.date_ends.max = `${this.selected_year}-12-31`;
		},
	}));
});
