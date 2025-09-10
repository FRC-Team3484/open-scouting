/**
 * Handles the submit button on the contribute page
 *
 * Checks to be sure all required fields are filled out, builds the JSON data to send to the server,
 * and uploads the scouting report the server
 *
 * If the user is offline, stores the scouting report locally
 */

document.addEventListener("alpine:init", () => {
	Alpine.data("submit_manager", () => ({
		missing_required_fields: false,
		menu_open: false,
		save_field_last: [],
		wakeLock: null,

		/**
		 * Check fields for any missing required fields
		 *
		 * @returns {boolean} True if all required fields are filled out
		 */
		check_fields() {
			const all_fields = document.querySelectorAll("input");
			let missing_field_found = false;

			for (const field of all_fields) {
				if (
					field.getAttribute("scouting_required") === "true" &&
					field.value === ""
				) {
					field.classList.add("field_missing");
					missing_field_found = true;
				} else {
					field.classList.remove("field_missing");
				}
			}

			this.missing_required_fields = missing_field_found;

			if (missing_field_found) {
				return false;
			} else {
				return true;
			}
		},

		/**
		 * Creates the JSON data of the scouting match data to send to the server or store locally
		 *
		 * @returns {Object} The JSON data
		 */
		create_json_data() {
			const data = [];

			const all_inputs = document.querySelectorAll("input");
			const all_selects = document.querySelectorAll("select");
			const other_fields = document.querySelectorAll(".field_other");

			for (const field of all_inputs) {
				let value;
				if (field.value) {
					if (
						field.getAttribute("scouting_type") === "large_integer" ||
						field.getAttribute("scouting_type") === "text"
					) {
						value = field.value;
					} else if (field.getAttribute("scouting_type") === "boolean") {
						value = field.checked;
					}

					const data_field = {
						name: field.getAttribute("x-ref"),
						type: field.getAttribute("scouting_type"),
						value: value,
						stat_type: field.getAttribute("scouting_stat_type"),
						game_piece: field.getAttribute("scouting_game_piece"),
					};

					data.push(data_field);
				}
			}

			for (const field of all_selects) {
				let value;
				if (field.value) {
					if (
						field.getAttribute("scouting_type") === "choice" ||
						field.getAttribute("scouting_type") === "multiple_choice"
					) {
						value = field.value;
						pretty_value = field.options[field.selectedIndex].text;
					}

					const data_field = {
						name: field.getAttribute("x-ref"),
						type: field.getAttribute("scouting_type"),
						value: value,
						pretty_value: pretty_value,
						stat_type: field.getAttribute("scouting_stat_type"),
						game_piece: field.getAttribute("scouting_game_piece"),
					};

					console.log(pretty_value);

					data.push(data_field);
				}
			}

			for (const field of other_fields) {
				let value;
				if (field.value) {
					if (field.getAttribute("scouting_type") === "integer") {
						value = field.value;
					}

					const data_field = {
						name: field.getAttribute("x-ref"),
						type: field.getAttribute("scouting_type"),
						value: value,
						stat_type: field.getAttribute("scouting_stat_type"),
						game_piece: field.getAttribute("scouting_game_piece"),
					};

					data.push(data_field);
				} else {
					const data_field = {
						name: field.getAttribute("x-ref"),
						type: field.getAttribute("scouting_type"),
						value: 0,
						stat_type: field.getAttribute("scouting_stat_type"),
						game_piece: field.getAttribute("scouting_game_piece"),
					};

					data.push(data_field);
				}
			}

			return data;
		},

		/**
		 * Either sends the scouting report to the server or stores it locally if the user is offline
		 *
		 * Additionally, doesn't do anything if the user is in demo mode and correctly
		 * sets up the url parameters for the status and next match number
		 */
		async submit_button() {
			try {
				var demo_param = JSON.parse(
					new URL(window.location.href).searchParams.get("demo").toLowerCase(),
				);
			} catch {
				var demo_param = false;
			}

			const match_number = document.querySelector(
				"input[name='match_number']",
			).value;
			const type = document.querySelector("select[name='match_type']").value;

			if (!demo_param) {
				if (this.check_fields()) {
					const report_uuid = crypto.randomUUID();

					db.open()
						.then(() => {
							const report_backup = {
								uuid: report_uuid,
								data: this.create_json_data(),
								event_name: encodeURIComponent(EVENT_NAME),
								event_code: EVENT_CODE,
								custom: CUSTOM,
								year: YEAR,
							};

							db.backups
								.add(report_backup)
								.then(() => {
									log("INFO", "Data added to the database");
								})
								.catch((error) => {
									log("WARNING", `Error adding data to the database: ${error}`);
								});
						})
						.catch((error) => {
							log("WARNING", `Error opening database: ${error}`);
						});

					if (globalThis.offline === false) {
						const response = await fetch(`${SERVER_IP}/submit`, {
							method: "POST",
							headers: {
								"Content-Type": "application/json",
								"X-CSRFToken": CSRF_TOKEN,
							},
							body: JSON.stringify({
								uuid: report_uuid,
								data: JSON.stringify(this.create_json_data()),
								event_name: encodeURIComponent(EVENT_NAME),
								event_code: EVENT_CODE,
								custom: CUSTOM,
								year: YEAR,
							}),
						});

						response.text().then(async (text) => {
							const url = new URL(window.location.href);

							url.searchParams.set("submitted", true);
							url.searchParams.delete("submitted_offline");
							url.searchParams.delete("submitted_demo");

							url.searchParams.set(
								"match_number",
								Number.parseInt(match_number, 10) + 1,
							);
							url.searchParams.set("match_type", encodeURIComponent(type));

							this.clear_field_state();
							window.location.href = url.toString();
						});
					} else {
						log("INFO", "You're offline, report will be saved offline.");

						db.offline_reports
							.put({
								uuid: report_uuid,
								data: this.create_json_data(),
								event_name: encodeURIComponent(EVENT_NAME),
								event_code: EVENT_CODE,
								custom: CUSTOM,
								year: YEAR,
							})
							.then(() => {
								log("INFO", "Data added to the database");

								const url = new URL(window.location.href);

								url.searchParams.set("submitted_offline", true);
								url.searchParams.delete("submitted");
								url.searchParams.delete("submitted_demo");

								url.searchParams.set(
									"match_number",
									Number.parseInt(match_number, 10) + 1,
								);
								url.searchParams.set("match_type", encodeURIComponent(type));

								this.clear_field_state();
								window.location.href = url.toString();
							})
							.catch((error) => {
								log("WARNING", `Error adding data to the database: ${error}`);
							});
					}
				}
			} else {
				log("INFO", "Submitted in demo mode");

				const url = new URL(window.location.href);

				url.searchParams.set("submitted_demo", true);
				url.searchParams.delete("submitted");
				url.searchParams.delete("submitted_offline");

				url.searchParams.set(
					"match_number",
					Number.parseInt(match_number, 10) + 1,
				);
				url.searchParams.set("match_type", encodeURIComponent(type));
				this.clear_field_state();

				window.location.href = url.toString();
			}
		},

		export_as_json() {
			const report_uuid = crypto.randomUUID();

			const blob = new Blob(
				[
					JSON.stringify(
						{
							uuid: report_uuid,
							data: this.create_json_data(),
							event_name: EVENT_NAME,
							event_code: EVENT_CODE,
							custom: CUSTOM,
							year: YEAR,
							open_scouting: true,
						},
						null,
						2,
					),
				],
				{
					type: "application/json",
				},
			);
			const url = URL.createObjectURL(blob);
			const link = document.createElement("a");
			link.href = url;
			const date = new Date();
			const formattedDate = date
				.toISOString()
				.replace(/[:.]/g, "-")
				.slice(0, 19);
			link.download = `open_scouting_report_${formattedDate}.json`;
			link.click();
		},

		reset() {
			const match_number = document.querySelector(
				"input[name='match_number']",
			).value;
			const type = document.querySelector("select[name='match_type']").value;

			const url = new URL(window.location.href);

			url.searchParams.delete("submitted_offline");
			url.searchParams.delete("submitted");
			url.searchParams.delete("submitted_demo");

			url.searchParams.set(
				"match_number",
				Number.parseInt(match_number, 10) + 1,
			);
			url.searchParams.set("match_type", encodeURIComponent(type));
			this.clear_field_state();

			window.location.href = url.toString();
		},

		save_report_offline() {
			if (this.check_fields()) {
				const report_uuid = crypto.randomUUID();

				const match_number = document.querySelector(
					"input[name='match_number']",
				).value;
				const type = document.querySelector("select[name='match_type']").value;

				db.offline_reports
					.put({
						uuid: report_uuid,
						data: this.create_json_data(),
						event_name: encodeURIComponent(EVENT_NAME),
						event_code: EVENT_CODE,
						custom: CUSTOM,
						year: YEAR,
					})
					.then(() => {
						log("INFO", "Data added to the database");

						const url = new URL(window.location.href);

						url.searchParams.set("submitted_offline", true);
						url.searchParams.delete("submitted");
						url.searchParams.delete("submitted_demo");

						url.searchParams.set(
							"match_number",
							Number.parseInt(match_number, 10) + 1,
						);
						url.searchParams.set("match_type", encodeURIComponent(type));
						this.clear_field_state();

						window.location.href = url.toString();
					})
					.catch((error) => {
						log("WARNING", `Error adding data to the database: ${error}`);
					});
			}
		},

		async import_from_json(e) {
			const match_number = document.querySelector(
				"input[name='match_number']",
			).value;
			const type = document.querySelector("select[name='match_type']").value;

			const files = e.target.files;

			for (const file of files) {
				if (file) {
					const reader = new FileReader();

					reader.onload = async () => {
						try {
							const data = JSON.parse(reader.result);
							if (data.open_scouting) {
								if (globalThis.offline === false) {
									const response = await fetch(`${SERVER_IP}/submit`, {
										method: "POST",
										headers: {
											"Content-Type": "application/json",
											"X-CSRFToken": CSRF_TOKEN,
										},
										body: JSON.stringify({
											uuid: data.uuid,
											data: JSON.stringify(data.data),
											event_name: encodeURIComponent(data.event_name),
											event_code: data.event_code,
											custom: data.custom,
											year: data.year,
										}),
									});

									response.text().then(async (text) => {
										const url = new URL(window.location.href);

										url.searchParams.set("submitted", true);
										url.searchParams.delete("submitted_offline");
										url.searchParams.delete("submitted_demo");

										url.searchParams.set(
											"match_number",
											Number.parseInt(match_number, 10) + 1,
										);
										url.searchParams.set(
											"match_type",
											encodeURIComponent(type),
										);

										window.location.href = url.toString();
									});
								} else {
									log("INFO", "You're offline, report will be saved offline.");

									db.offline_reports
										.put({
											uuid: data.uuid,
											data: data.data,
											event_name: encodeURIComponent(data.event_name),
											event_code: data.event_code,
											custom: data.custom,
											year: data.year,
										})
										.then(() => {
											log("INFO", "Data added to the database");

											const url = new URL(window.location.href);

											url.searchParams.set("submitted_offline", true);
											url.searchParams.delete("submitted");
											url.searchParams.delete("submitted_demo");

											url.searchParams.set(
												"match_number",
												Number.parseInt(match_number, 10) + 1,
											);
											url.searchParams.set(
												"match_type",
												encodeURIComponent(type),
											);

											window.location.href = url.toString();
										})
										.catch((error) => {
											log(
												"WARNING",
												`Error adding data to the database: ${error}`,
											);
										});
								}
							} else {
								log("WARNING", "Invalid JSON format for import");
							}
						} catch (error) {
							log("ERROR", "Failed to parse JSON:", error);
						}
					};

					reader.readAsText(file);
				}
			}
		},

		/**
		 * Saves the state of the fields to localStorage
		 */
		save_field_state(data) {
			for (const field in data) {
				localStorage.setItem(data[field].name, data[field].value);
			}
		},

		/**
		 * Clears the state of the fields from localStorage
		 */
		clear_field_state() {
			for (const field in this.save_field_last) {
				localStorage.removeItem(this.save_field_last[field].name);
			}
		},

		/**
		 * Acquires a wake lock to prevent the device from sleeping
		 */
		async request_wake_lock() {
			try {
				this.wakeLock = await navigator.wakeLock.request("screen");
				log("DEBUG", "Wake lock acquired");

				// Optionally handle visibility changes (some platforms release the lock when page is hidden)
				document.addEventListener("visibilitychange", async () => {
					if (
						this.wakeLock !== null &&
						document.visibilityState === "visible"
					) {
						try {
							this.wakeLock = await navigator.wakeLock.request("screen");
							log("DEBUG", "Wake lock re-acquired");
						} catch (err) {
							log(
								"WARNING",
								`Failed to re-acquire wake lock: ${err.name}, ${err.message}`,
							);
						}
					}
				});
			} catch (err) {
				log(
					"WARNING",
					`Failed to acquire wake lock: ${err.name}, ${err.message}`,
				);
			}
		},

		/**
		 * Initializes the submit manager component
		 *
		 * Prevents the device from sleeping while on this page
		 */
		async init() {
			const handle_click_once = () => {
				this.request_wake_lock();
				document.removeEventListener("click", handle_click_once); // Only run once
			};

			document.addEventListener("click", handle_click_once, { once: true });

			setInterval(() => {
				const save_field_data = this.create_json_data();

				if (save_field_data !== this.save_field_last) {
					this.save_field_state(save_field_data);

					this.save_field_last = save_field_data;
				}
			}, 5000);
		},
	}));
});
