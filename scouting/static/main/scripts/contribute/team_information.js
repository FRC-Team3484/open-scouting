/**
 * Handles the team information and team number autofilling on the contribute page
 *
 * This fills in the team number on the page based on which scouting position is selected
 */

document.addEventListener("alpine:init", () => {
	Alpine.data("team_information", () => ({
		show: true,
		match_number: "",
		match_type: "",
		team_to_watch: "",
		event_data: [],
		event_cached: "",

		/**
		 * Gets the matches in an event
		 */
		async get_event_data() {
			const team = this.$refs.team.value;
			const year = new URL(window.location.href).searchParams.get("year");
			const event_code = new URL(window.location.href).searchParams.get(
				"event_code",
			);

			const response = await fetch(
				`https://www.thebluealliance.com/api/v3/event/${year + event_code}/matches/simple`,
				{
					method: "GET",
					headers: {
						"X-TBA-Auth-Key": "{{ TBA_API_KEY }}",
					},
				},
			);

			if (response.ok) {
				const data = await response.json();
				this.event_data = data;
				this.event_cached = year + event_code;
			}
		},

		/**
		 * Processes the team information to get the team to watch
		 */
		async process_data() {
			const team = this.$refs.team.value;
			const year = new URL(window.location.href).searchParams.get("year");
			const event_code = new URL(window.location.href).searchParams.get(
				"event_code",
			);

			if (this.event_cached !== year + event_code) {
				await this.get_event_data();
			}

			if (
				this.match_type === "Practice Match" ||
				this.match_type === "Other Match" ||
				this.match_type === "N/A"
			) {
				// Don't return a team

				this.team_to_watch = "";
				this.show = false;
			} else if (
				this.match_type === "Qualification Match" ||
				this.match_type === "Playoff Match"
			) {
				// Return a team based off of the match type
				this.show = true;

				if (this.match_type === "Qualification Match") {
					const data = this.event_data.filter(
						(match) =>
							match.comp_level === "qm" &&
							match.match_number === Number.parseInt(this.match_number),
					);
					if (data[0] !== undefined) {
						if (team.includes("Red")) {
							this.team_to_watch = data[0].alliances.red.team_keys[
								team.replace("Red ", "") - 1
							].replace("frc", "");
						} else if (team.includes("Blue")) {
							this.team_to_watch = data[0].alliances.blue.team_keys[
								team.replace("Blue ", "") - 1
							].replace("frc", "");
						}
					} else {
						this.team_to_watch = "";
					}
				} else if (this.match_type === "Playoff Match") {
					const data = this.event_data.filter(
						(match) =>
							match.comp_level === "sf" &&
							match.match_number === Number.parseInt(this.match_number),
					);
					if (data[0] !== undefined) {
						if (team.includes("Red")) {
							this.team_to_watch = data[0].alliances.red.team_keys[
								team.replace("Red ", "") - 1
							].replace("frc", "");
						} else if (team.includes("Blue")) {
							this.team_to_watch = data[0].alliances.blue.team_keys[
								team.replace("Blue ", "") - 1
							].replace("frc", "");
						}
					} else {
						this.team_to_watch = "";
					}
				}
			}

			if (this.team_to_watch) {
				window.dispatchEvent(
					new CustomEvent("set_team_number", {
						detail: { team_number: this.team_to_watch },
					}),
				);
			}
		},

		/**
		 * Initializes the team information component
		 *
		 * Gets the position from the URL and makes sure the input has the correct color,
		 * and begins listening for the match number and match type changes so the team number can
		 * be updated accordingly
		 */
		init() {
			const position = decodeURIComponent(
				new URL(window.location.href).searchParams.get("position"),
			);
			this.$refs.team.value = position;
			const selectedOption = Array.from(this.$refs.team.options).find(
				(option) => option.value === position,
			);
			if (selectedOption) {
				this.$refs.team.className = `ui_input w-32! ${selectedOption.className}`;
			}

			window.addEventListener("match_number_change", (event) => {
				event.stopImmediatePropagation();
				const { match_number } = event.detail;

				this.match_number = match_number;

				this.process_data();
			});

			window.addEventListener("match_type_change", (event) => {
				event.stopImmediatePropagation();
				const { match_type } = event.detail;

				this.match_type = match_type;

				this.process_data();
			});
		},
	}));
});
