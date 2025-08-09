/**
 * Handles the main functionality of the pit scouting page
 *
 * Pulls data from the server, syncs the data to the server, and stores the data locally
 */

document.addEventListener("alpine:init", () => {
	Alpine.data("pits", () => ({
		pit_data: [],
		filtered_pit_data: [],
		filter: "all",
		pit_status: [],
		state: "loading",

		/**
		 * Add an answer to a question to the local database
		 *
		 * @param {Event} event - The event object
		 * @param {string} simple_name - The simple name of the question
		 * @param {string} type - The type of the question
		 */
		async submit_answer(event, simple_name, type) {
			const urlParams = new URLSearchParams(window.location.search);
			const username = urlParams.get("username");

			const input = event.target
				.closest("div")
				.querySelector(".ui_input, .ui_checkbox");
			const uuid = event.target.closest(".pit_top").getAttribute("team_uuid");

			const today = new Date();
			const date = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`;

			const value =
				type === "text"
					? input.value
					: type === "number"
						? Number(input.value)
						: type === "boolean"
							? input.checked
							: type === "choice"
								? input.value
								: console.error("Unknown question type:", type);

			// Fetch the pit object from the DB
			const pit = await db.pit_scouting.get(uuid);
			if (!pit) {
				console.error("Pit data not found for uuid:", uuid);
				return;
			}

			// Find the question in the pit data
			const question = pit.questions.find((q) => q.simple_name === simple_name);
			if (!question) {
				console.error("Question not found:", simple_name);
				return;
			}

			// Add the new answer
			if (!Array.isArray(question.answers)) {
				question.answers = [];
			}
			question.answers.push({
				contributed: date,
				value: value,
				uuid: String(crypto.randomUUID()),
				user: username,
			});

			pit.needs_synced = true;

			await db.pit_scouting.put(pit);
		},

		/**
		 * Add a question to the local database
		 *
		 * @param {Event} event - The event object
		 * @param {HTMLInputElement} name - The input element containing the question text
		 */
		async submit_question(event, name) {
			const uuid = event.target.closest(".pit_top").getAttribute("team_uuid");

			const simple_name = name.value.toLowerCase().replace(/[^\w]+/g, "_");

			// Get the pit from the database by UUID
			const pit = await db.pit_scouting.get(uuid);
			if (!pit) {
				console.error("Pit data not found for uuid:", uuid);
				return;
			}

			// Add the new question to the database
			pit.questions.push({
				text: name.value,
				simple_name: simple_name,
				type: "text",
				answers: [],
			});

			pit.needs_synced = true;

			// Save the pit
			await db.pit_scouting.put(pit);

			name.value = "";
		},

		/**
		 * Add a new team to the local database
		 *
		 * Uses The Blue Alliance to attempt to get the team's nickname
		 *
		 * @param {Event} event - The event object
		 * @param {HTMLInputElement} team_number - The input element with the team number
		 */
		async submit_team(event, team_number) {
			const urlParams = new URLSearchParams(window.location.search);
			const event_name = urlParams.get("event_name");
			const event_code = urlParams.get("event_code");
			const year = Number(urlParams.get("year")); // ensure correct type
			const custom = urlParams.get("custom") || false;

			let nickname = " ";
			if (globalThis.offline === false) {
				try {
					const response = await fetch(
						`https://www.thebluealliance.com/api/v3/team/frc${team_number.value}`,
						{
							method: "GET",
							headers: {
								"X-TBA-Auth-Key": TBA_API_KEY,
							},
						},
					);
					if (response.ok) {
						const json = await response.json();
						nickname = json.nickname || " ";
					}
				} catch (error) {
					log("WARNING", "TBA fetch failed:", error);
				}
			}

			// Retrieve the master list of questions from the local database
			const masterQuestions = await db.pit_scouting
				.where("uuid")
				.equals("master_questions")
				.first();

			const new_pit = {
				uuid: crypto.randomUUID(),
				event_name: event_name,
				event_code: event_code,
				year: year,
				custom: custom,
				team_number: team_number.value,
				nickname: nickname,
				needs_synced: true,
				questions: masterQuestions.questions,
			};

			await db.pit_scouting.put(new_pit);

			team_number.value = "";
		},

		/**
		 * Store the master list of questions locally for adding teams while offline
		 */
		store_master_list_of_questions_locally(questions) {
			db.pit_scouting
				.put({
					uuid: "master_questions",
					event_name: "",
					event_code: "",
					year: "",
					custom: false,
					team_number: "",
					nickname: "",
					needs_synced: false,
					questions: questions,
				})
				.then(() => {
					log("INFO", "Master questions added to the database");
				})
				.catch((error) => {
					log("WARNING", `Error adding data to the database: ${error}`);
				});
		},

		/**
		 * Get the status of each pit in the local database,
		 * so scouts can quickly press buttons to go to a team
		 */
		get_pit_status() {
			// Creates a list of all the teams and their status to add buttons for the scout to scroll to
			// TODO: Fix for new pit scouting system
			const completed = [];
			const incomplete = [];
			const no_data = [];

			for (const pit of this.pit_data) {
				const questions = pit.questions || []; // Default to empty array if undefined
				const totalQuestions = questions.length;
				const answeredQuestions = questions.filter(
					(q) => (q.answers || []).length > 0,
				).length;

				if (answeredQuestions === 0) {
					no_data.push({ team_number: pit.team_number, status: "no_data" });
				} else if (answeredQuestions === totalQuestions) {
					completed.push({ team_number: pit.team_number, status: "completed" });
				} else {
					incomplete.push({
						team_number: pit.team_number,
						status: "incomplete",
					});
				}
			}

			const all = [...no_data, ...incomplete, ...completed];

			if (this.filter === "completed") {
				this.pit_status = completed;
			} else if (this.filter === "incomplete") {
				this.pit_status = incomplete;
			} else if (this.filter === "no_data") {
				this.pit_status = no_data;
			} else if (this.filter === "all") {
				this.pit_status = all;
			} else {
				this.pit_status = all;
			}
		},

		/**
		 * Filters the displayed pit data by
		 */
		filter_pit_data() {
			const completed = [];
			const incomplete = [];
			const no_data = [];

			for (const pit of this.pit_data) {
				const questions = pit.questions || []; // Default to empty array if undefined
				const totalQuestions = questions.length;
				const answeredQuestions = questions.filter(
					(q) => (q.answers || []).length > 0,
				).length;

				if (answeredQuestions === 0) {
					no_data.push(pit);
				} else if (answeredQuestions === totalQuestions) {
					completed.push(pit);
				} else {
					incomplete.push(pit);
				}
			}

			if (this.filter === "completed") {
				this.filtered_pit_data = completed;
			} else if (this.filter === "incomplete") {
				this.filtered_pit_data = incomplete;
			} else if (this.filter === "no_data") {
				this.filtered_pit_data = no_data;
			} else if (this.filter === "all") {
				this.filtered_pit_data = this.pit_data;
			} else {
				this.filtered_pit_data = this.pit_data;
			}
		},

		/**
		 * Scroll to a pit on the page
		 *
		 * @param {string} pit - The team number of the pit to scroll to
		 */
		scroll_to_pit(pit) {
			const pit_div = document.querySelector(`div[team_number='${pit}']`);
			pit_div.scrollIntoView({ behavior: "smooth" });
		},

		/**
		 * Scroll to the top of the page
		 */
		go_to_top() {
			window.scrollTo({ top: 0, behavior: "smooth" });
		},

		/**
		 * Store pit data from server into the local database
		 */
		setup_pit_data(pit_data) {
			for (const pit in pit_data.pits) {
				db.pit_scouting
					.put({
						uuid: pit_data.pits[pit].uuid,
						event_name: pit_data.event_name,
						event_code: pit_data.event_code,
						year: pit_data.year,
						custom: pit_data.custom,
						team_number: pit_data.pits[pit].team_number,
						nickname: pit_data.pits[pit].nickname,
						needs_synced: false,
						questions: pit_data.pits[pit].questions,
					})
					.then(() => {
						log("INFO", "Pit data added to the database");
					})
					.catch((error) => {
						log("WARNING", `Error adding data to the database: ${error}`);
					});
			}
		},

		/**
		 * Get pit data from the server
		 */
		async get_pit_data() {
			const urlParams = new URLSearchParams(window.location.search);
			const event_name = urlParams.get("event_name");
			const event_code = urlParams.get("event_code");
			const year = urlParams.get("year");
			const custom = urlParams.get("custom");

			this.state = "loading";

			const pits_response = await fetch(`${SERVER_IP}/get_pits`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": CSRF_TOKEN,
				},
				body: JSON.stringify({
					event_name: event_name,
					event_code: event_code,
					year: year,
					custom: custom,
				}),
			});

			if (pits_response.ok) {
				this.setup_pit_data(await pits_response.json());
				this.state = "saved";
				this.get_pit_status();
				this.filter_pit_data();
			}
		},

		/**
		 * Get the master list of questions from the server
		 */
		async get_master_questions() {
			const urlParams = new URLSearchParams(window.location.search);
			const year = urlParams.get("year");

			const master_list_of_questions_response = await fetch(
				`${SERVER_IP}/get_pit_questions`,
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
						"X-CSRFToken": CSRF_TOKEN,
					},
					body: JSON.stringify({
						year: year,
					}),
				},
			);

			if (master_list_of_questions_response.ok) {
				this.store_master_list_of_questions_locally(
					await master_list_of_questions_response.json(),
				);
			}
		},

		/**
		 * Sync the pit data by saving the local database to the server
		 * and then retrieving the data from the server
		 */
		async sync_pit_data() {
			const urlParams = new URLSearchParams(window.location.search);
			const event_name = urlParams.get("event_name");
			const event_code = urlParams.get("event_code");
			const year = Number(urlParams.get("year"));
			const custom = urlParams.get("custom") || false;

			if (!globalThis.offline) {
				// User is online, so check for any unsaved changes and sync if needed

				db.pit_scouting
					.filter(
						(item) =>
							item.needs_synced === true &&
							item.event_name === event_name &&
							item.event_code === event_code &&
							item.year === year,
					)
					.toArray()
					.then(async (data) => {
						if (data.length > 0) {
							// There's changes that need synced
							this.state = "syncing";

							for (const item of data) {
								try {
									const response = await fetch(`${SERVER_IP}/update_pit`, {
										method: "POST",
										headers: {
											"X-TBA-Auth-Key": TBA_API_KEY,
											"Content-Type": "application/json",
											"X-CSRFToken": CSRF_TOKEN,
										},
										body: JSON.stringify({
											uuid: item.uuid,
											event_name: item.event_name,
											event_code: item.event_code,
											year: item.year,
											custom: custom,
											team_number: item.team_number,
											nickname: item.nickname,
											questions: item.questions || [], // In case questions are empty, send a blank list
										}),
									});
									if (response.ok) {
										await db.pit_scouting.update(item.uuid, {
											needs_synced: false,
										});
										// log("DEBUG", `Pit ${item.uuid} synced`);
									}
								} catch (error) {
									log("WARNING", "Pit sync failed:", error);
								}
							}

							// Fetch any new data from the server
							this.get_pit_data();
						} else {
							// There's no changes that need synced
							this.get_pit_data();
						}
					});
			}
		},

		/**
		 * Check if there are any unsaved changes to update the status indicator
		 */
		check_for_unsaved_changes() {
			const urlParams = new URLSearchParams(window.location.search);
			const event_name = urlParams.get("event_name");
			const event_code = urlParams.get("event_code");
			const year = Number(urlParams.get("year"));

			db.pit_scouting
				.filter(
					(item) =>
						item.event_name === event_name &&
						item.event_code === event_code &&
						item.year === year &&
						item.needs_synced === true &&
						item.uuid !== "master_questions",
				)
				.count()
				.then((count) => {
					if (count > 0) {
						this.state = "unsaved";
					} else {
						this.state = "saved";
					}
				})
				.catch((error) => {
					log("WARNING", `Error counting unsaved changes: ${error}`);
				});
		},

		/**
		 * Initialize the pit scouting page
		 *
		 * If the user isn't offline, get the pit data and master list of questions and store them locally
		 *
		 * If the user is offline, don't do anything
		 *
		 * Start the syncing process
		 *
		 * Also doesn't let the page be closed with unsaved changes
		 */
		init() {
			if (!new URLSearchParams(window.location.search).has("demo")) {
				// Delay by 100ms to make sure globalThis.offline is defined by menu
				setTimeout(async () => {
					if (globalThis.offline === false) {
						// Get pit data and master list of questions from server, and save in IndexedDB

						await this.sync_pit_data();
						await this.get_master_questions();
					}
				}, 100);

				window.addEventListener("beforeunload", (event) => {
					if (this.state !== "saved") {
						event.preventDefault();
						event.returnValue = "";
						return "";
					}
				});

				const urlParams = new URLSearchParams(window.location.search);
				const event_name = urlParams.get("event_name");
				const event_code = urlParams.get("event_code");
				const year = Number(urlParams.get("year"));

				const pit_scouting_observable = Dexie.liveQuery(() =>
					db.pit_scouting
						.filter(
							(pit) =>
								pit.event_name === event_name &&
								pit.event_code === event_code &&
								pit.year === year,
						)
						.toArray(),
				);

				db.pit_scouting
					.filter(
						(pit) =>
							pit.event_name === event_name &&
							pit.event_code === event_code &&
							pit.year === year,
					)
					.toArray()
					.then((data) => {
						this.pit_data = data.sort((a, b) => a.team_number - b.team_number);
						this.get_pit_status();
						this.filter_pit_data();
					});

				const subscription = pit_scouting_observable.subscribe({
					next: (result) => {
						this.pit_data = result.sort(
							(a, b) => a.team_number - b.team_number,
						);
						this.filter_pit_data();
					},
					error: (error) => {
						log("ERROR", "Error subscribing to pit scouting db", error);
					},
				});

				setInterval(() => {
					this.sync_pit_data();
				}, 10000);

				setInterval(() => {
					this.check_for_unsaved_changes();
				}, 500);
			} else {
				log("INFO", "Pit scouting is in demo mode");
				this.state = "demo";

				setTimeout(() => {
					window.dispatchEvent(
						new CustomEvent("dialog_show", {
							detail: {
								event_name: "pit_scouting_demo",
								title: gettext("Pit scouting is not avaliable in demo mode"),
								body: gettext(
									"Unfortunately, this feature is not currently available in demo mode",
								),
								buttons: [
									{
										type: "confirm",
										icon: "ph-bold ph-house",
										text: "Go home",
									},
								],
							},
						}),
					);
				}, 100);
			}

			window.addEventListener("dialog_confirm", (event) => {
				const { event_name } = event.detail;

				if (event_name === "pit_scouting_demo") {
					event.stopImmediatePropagation();
					window.location.href = "/";
				}
			});
		},
	}));
});
