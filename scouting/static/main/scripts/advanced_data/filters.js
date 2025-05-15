document.addEventListener("alpine:init", () => {
	Alpine.data("filters", () => ({
		YEARS: JSON.parse(YEARS).reverse(),
		teams: [],
		events: [],
		query: "",
		team_results: [],
		event_results: [],
		team_results_filtered: [],
		event_results_filtered: [],
		add_team_open: false,
		add_event_open: false,
		data: [],
		data_sorted: [],
		sort_fields: [],
		offline: false,
		data_menu_export_open: false,

		/**
		 * Get the query string from the filters
		 */
		get_query() {
			let teams_str = "";
			let events_str = "";

			if (this.teams.length > 0) {
				teams_str = `&teams=${this.teams.join(",")}`;
			} else {
				teams_str = "";
			}
			if (this.events.length > 0) {
				events_str = `&events=${this.events.map((event) => event.code).join(",")}`;
			} else {
				events_str = "";
			}

			this.query = `?year=${this.$refs.year_input.value}${teams_str}${events_str}`;

			window.history.replaceState({}, "", this.query);
		},

		/**
		 * Set the filters given a query string in the URL
		 */
		set_filters_from_query() {
			const urlParams = new URLSearchParams(window.location.search);
			const year = urlParams.get("year");
			const teams = urlParams.get("teams");
			const events = urlParams.get("events");

			if (year) {
				this.$refs.year_input.value = year;
			}

			if (teams) {
				this.teams = teams.split(",");
			}

			if (events) {
				this.events = events.split(",").map((code) => {
					return { code: code, name: code };
				});
			}

			this.update_results_and_query();
		},

		/**
		 * Clear the filters
		 */
		clear_filters() {
			this.teams = [];
			this.events = [];
			this.team_results = [];
			this.event_results = [];
			this.update_results_and_query();
		},

		/**
		 * Add a team to the filters after being selected in the search box
		 *
		 * @param {string} team
		 */
		add_team(team) {
			this.teams.push(team);
			this.$refs.teams_search.value = "";
			this.update_results_and_query();
		},

		/**
		 * Add an event to the filters after being selected in the search box
		 *
		 * @param {string} event
		 */
		add_event(event) {
			this.events.push(event);
			this.$refs.events_search.value = "";
			this.update_results_and_query();
		},

		/**
		 * Remove a team from the filters
		 *
		 * @param {string} team
		 */
		remove_team(team) {
			this.teams = this.teams.filter((t) => t !== team);
			this.update_results_and_query();
		},

		/**
		 * Remove an event from the filters
		 *
		 * @param {string} event
		 */
		remove_event(event) {
			this.events = this.events.filter((e) => e !== event);
			this.update_results_and_query();
		},

		/**
		 * Update the results and query string based on the current filters
		 *
		 * Then, update the data
		 */
		update_results_and_query() {
			this.get_teams_with_filters();
			this.get_events_with_filters();
			this.get_query();

			this.get_data();
			const data_promise = this.get_data();
			data_promise.then(() => {
				this.get_sortable_fields();
			});
		},

		/**
		 * Update the team search box based on the query
		 */
		update_team_search() {
			const search = this.$refs.teams_search.value.toLowerCase();
			this.team_results_filtered = this.team_results.filter((team) =>
				team?.toString().toLowerCase().includes(search),
			);
		},

		/**
		 * Update the event search box based on the query
		 */
		update_event_search() {
			const search = this.$refs.events_search.value.toLowerCase();
			this.event_results_filtered = this.event_results.filter((event) =>
				event.name.toLowerCase().includes(search),
			);
		},

		/**
		 * Get the fields from the data that can be used for sorting
		 */
		get_sortable_fields() {
			const sort_fields = {};

			if (!this.data) {
				console.warn("No data available");
				return [];
			}

			// Default sorting option
			sort_fields.disabled = {
				simple_name: "disabled",
				name: "Don't sort",
			};

			// Process each team's auton & teleop sections
			for (const team_number in this.data) {
				const team_data = this.data[team_number];

				for (const section of ["auton", "teleop"]) {
					if (team_data[section]) {
						for (const game_piece of Object.keys(team_data[section])) {
							const game_piece_data = team_data[section][game_piece];

							for (const type of ["score", "miss"]) {
								if (game_piece_data[type]) {
									for (const field of Object.keys(game_piece_data[type])) {
										sort_fields[field] = {
											simple_name: field,
											name: field
												.replace(/_/g, " ")
												.replace(/\b\w/g, (l) => l.toUpperCase()),
										};
									}
								}
							}
						}
					}
				}
			}

			// console.log("Sortable fields:", sort_fields);

			// Convert to array
			this.sort_fields = Object.values(sort_fields);
		},

		/**
		 * Sort the teams based on the selected field and order
		 *
		 * @param {Object} data
		 */
		sort_teams_by_field(data) {
			if (!data) {
				console.warn("No data available");
				return [];
			}

			const field = this.$refs.sort_field.value;
			const order = this.$refs.sort_order.value;

			const sortedTeams = Object.keys(data)
				.map((teamNumber) => ({
					teamNumber,
					data: data[teamNumber],
					sortValue: this.get_team_field_value(teamNumber, field, data),
				}))
				.sort((a, b) =>
					order === "ascending"
						? a.sortValue - b.sortValue
						: b.sortValue - a.sortValue,
				)
				.map(({ teamNumber, data }) => ({ teamNumber, data }));

			// console.log(sortedTeams);

			return sortedTeams;
		},

		/**
		 * Get the value of a field for a specific team
		 *
		 * @param {string} team
		 * @param {string} field
		 *
		 * @returns {Array}
		 */
		get_team_field_value(teamNumber, field, data) {
			const team = data[teamNumber];
			if (!team) return 0;

			// Look through auton and teleop
			for (const section of ["auton", "teleop"]) {
				const sectionData = team[section];
				if (!sectionData) continue;

				for (const piece of Object.values(sectionData)) {
					for (const type of ["score", "miss"]) {
						const typeData = piece[type];
						if (!typeData) continue;

						if (
							field in typeData &&
							typeof typeData[field]?.average === "number"
						) {
							return typeData[field].average;
						}
					}
				}
			}

			// Check capabilities
			if (team.capabilities?.[field]) {
				const values = Object.values(team.capabilities[field]);
				if (values.length > 0 && typeof values[0] === "number") {
					return values[0];
				}
			}

			return 0;
		},

		/**
		 * Get the teams that match the filters for the team results box
		 */
		async get_teams_with_filters() {
			const response = await fetch(`${SERVER_IP}/get_teams_with_filters`, {
				method: "POST",
				headers: {
					"X-CSRFToken": CSRF_TOKEN,
				},
				body: JSON.stringify({
					year: this.$refs.year_input.value,
					events: JSON.stringify(this.events),
				}),
			});

			if (response.ok) {
				const results = await response.json();
				this.team_results = [...new Set(results)].filter(
					(t) => !this.teams.includes(t),
				);
				this.team_results_filtered = this.team_results;
				this.update_team_search();
			}
		},

		/**
		 * Get the events that match the filters for the event results box
		 */
		async get_events_with_filters() {
			const response = await fetch(`${SERVER_IP}/get_events_with_filters`, {
				method: "POST",
				headers: {
					"X-CSRFToken": CSRF_TOKEN,
				},
				body: JSON.stringify({
					year: this.$refs.year_input.value,
					teams: JSON.stringify(this.teams),
				}),
			});

			if (response.ok) {
				const results = await response.json();
				this.event_results = [
					...new Map(results.map((event) => [event.code, event])).values(),
				].filter((event) => !this.events.some((e) => e.code === event.code));
				this.event_results_filtered = this.event_results;
				this.update_event_search();
			}
		},

		/**
		 * Parse the data from the server into the format needed for displaying on the client
		 *
		 * @param {Array} data
		 *
		 * @returns {Object}
		 */
		parse_server_data(data) {
			const final_data = {};

			for (const team of data) {
				const team_number = team.team_number;

				if (!final_data[team_number]) {
					final_data[team_number] = {
						auton: {},
						teleop: {},
						capabilities: {},
						other: [],
					};
				}

				for (const match of team.data) {
					for (const field of match) {
						const { stat_type, game_piece, name, value } = field;

						switch (stat_type) {
							case "auton_score":
							case "auton_miss": {
								if (!game_piece) break;
								if (!final_data[team_number].auton[game_piece]) {
									final_data[team_number].auton[game_piece] = {
										score: {},
										miss: {},
									};
								}
								const autonType =
									stat_type === "auton_score" ? "score" : "miss";
								if (
									!final_data[team_number].auton[game_piece][autonType][name]
								) {
									final_data[team_number].auton[game_piece][autonType][name] = {
										values: [],
										average: 0,
										stat_type,
									};
								}
								final_data[team_number].auton[game_piece][autonType][
									name
								].values.push(value);
								break;
							}

							case "score":
							case "miss": {
								if (!game_piece) break;
								if (!final_data[team_number].teleop[game_piece]) {
									final_data[team_number].teleop[game_piece] = {
										score: {},
										miss: {},
									};
								}
								const teleopType = stat_type === "score" ? "score" : "miss";
								if (
									!final_data[team_number].teleop[game_piece][teleopType][name]
								) {
									final_data[team_number].teleop[game_piece][teleopType][name] =
										{ values: [], average: 0, stat_type };
								}
								final_data[team_number].teleop[game_piece][teleopType][
									name
								].values.push(value);
								break;
							}

							case "capability":
								if (!final_data[team_number].capabilities[name]) {
									final_data[team_number].capabilities[name] = {};
								}
								if (!final_data[team_number].capabilities[name][value]) {
									final_data[team_number].capabilities[name][value] = 0;
								}
								final_data[team_number].capabilities[name][value]++;
								break;

							case "other":
								final_data[team_number].other.push(value);
								break;
						}
					}
				}

				// Calculate averages per field for auton
				for (const game_piece in final_data[team_number].auton) {
					const piece_data = final_data[team_number].auton[game_piece];
					["score", "miss"].forEach((type) => {
						for (const field_name in piece_data[type]) {
							const field_data = piece_data[type][field_name];
							const count = field_data.values.length;
							field_data.average =
								count > 0
									? field_data.values.reduce((a, b) => a + b, 0) / count
									: 0;
						}
					});
				}

				// Calculate averages per field for teleop
				for (const game_piece in final_data[team_number].teleop) {
					const piece_data = final_data[team_number].teleop[game_piece];
					["score", "miss"].forEach((type) => {
						for (const field_name in piece_data[type]) {
							const field_data = piece_data[type][field_name];
							const count = field_data.values.length;
							field_data.average =
								count > 0
									? field_data.values.reduce((a, b) => a + b, 0) / count
									: 0;
						}
					});
				}

				// Convert capability counts to percentages per team
				const team_caps = final_data[team_number].capabilities;
				for (const cap_name in team_caps) {
					const cap_values = team_caps[cap_name];
					const total_entries = Object.values(cap_values).reduce(
						(a, b) => a + b,
						0,
					);
					for (const value in cap_values) {
						cap_values[value] = (cap_values[value] / total_entries) * 100;
					}
				}
			}

			// console.log(final_data);

			return final_data;
		},

		/**
		 * Get the data from the server using the query
		 */
		async get_data() {
			const response = await fetch(`${SERVER_IP}/get_data_from_query`, {
				method: "POST",
				headers: {
					"X-CSRFToken": CSRF_TOKEN,
				},
				body: JSON.stringify({
					query: this.query,
				}),
			});

			if (response.ok) {
				this.data = this.parse_server_data(await response.json());
				this.data_sorted = this.sort_teams_by_field(this.data);
				// this.data_sorted = this.data;
				window.dispatchEvent(
					new CustomEvent("data", {
						detail: { data: this.data_sorted },
					}),
				);
			}
		},

		export_as_json() {
			const jsonData = JSON.stringify(this.data_sorted, null, 2);
			const blob = new Blob([jsonData], { type: "application/json" });
			const url = URL.createObjectURL(blob);
			const a = document.createElement("a");
			a.href = url;
			a.download = `open_scouting_data_${this.query}.json`;
			a.click();
			URL.revokeObjectURL(url);
		},

		flattenTeam(teamNumber, teamData) {
			const flat = { team: teamNumber };

			function walk(obj, prefix = "") {
				for (const key in obj) {
					const value = obj[key];
					const newKey = prefix ? `${prefix}_${key}` : key;

					if (
						typeof value === "object" &&
						value !== null &&
						!Array.isArray(value)
					) {
						walk(value, newKey);
					} else if (Array.isArray(value)) {
						flat[newKey] = value.join("; "); // join arrays into strings
					} else {
						flat[newKey] = value;
					}
				}
			}

			walk(teamData);
			return flat;
		},

		export_as_csv() {
			// Step 1: Flatten all teams
			const flattened = [];
			for (const teamNumber in this.data_sorted) {
				flattened.push(
					this.flattenTeam(teamNumber, this.data_sorted[teamNumber]),
				);
			}

			// Step 2: Build CSV
			const allKeys = new Set();
			for (const team of flattened) {
				for (const key of Object.keys(team)) {
					allKeys.add(key);
				}
			}
			const headers = Array.from(allKeys);

			const csvRows = [];
			csvRows.push(headers.join(",")); // header row

			for (const team of flattened) {
				const row = headers.map((header) => {
					const value = team[header] ?? "";
					return `"${String(value).replace(/"/g, '""')}"`; // escape quotes
				});
				csvRows.push(row.join(","));
			}

			const csvString = csvRows.join("\n");

			// Done! You can now download or log it
			// console.log(csvString);

			const blob = new Blob([csvString], { type: "text/csv;charset=utf-8;" });
			const link = document.createElement("a");
			link.href = URL.createObjectURL(blob);
			link.download = `open_scouting_data_${this.query}.csv`;
			link.click();
		},

		/**
		 * Initialize the advanced data view page
		 */
		init() {
			// Wait to ensure year drop down is populated
			setTimeout(() => {
				const urlParams = new URLSearchParams(window.location.search);
				const query = urlParams.toString();

				if (query) {
					this.query = query;
					this.get_events_with_filters();

					this.set_filters_from_query();
					this.update_results_and_query();
				} else {
					this.update_results_and_query();
				}

				this.get_data();

				if (globalThis.offline) {
					this.offline = true;
				} else {
					this.offline = false;
				}
			}, 100);
		},
	}));
});
