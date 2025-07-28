document.addEventListener("alpine:init", () => {
	Alpine.data("menu", () => ({
		open: false,
		offline: !navigator.onLine,
		notification_shown: false,
		notification: {
			title: "",
			body: "",
			icon: "",
			icon_class: "",
		},
		dark_mode: true,
		credits_open: false,
		developer_open: false,
		service_worker_cache_first: true,
		offline_manual: false,
		offline_manual_last: false,
		mrbc_open: false,
		offline_reports: false,
		offline_pit_scouting: false,
		logs_open: false,
		storage_open: false,
		storage_warning: false,
		version: "",

		/**
		 * Check if the user is offline or not, and store it in a global variable
		 *
		 * Also emits and event and notification when the user is newly online or offline
		 */
		offline_check() {
			if (this.offline_manual === true && this.offline_manual_last === true) {
				this.offline_manual_last = false;
				globalThis.offline = true;
				window.dispatchEvent(new CustomEvent("scouting_offline"));
				this.show_notification(
					"Device offline",
					"You're now offline. Some features will be reduced until you're back online.",
					"wifi-slash",
				);
			} else {
				if (this.offline_manual_last === true) {
					this.offline_manual_last = false;
					globalThis.offline = false;
					window.dispatchEvent(new CustomEvent("scouting_online"));
				}

				if (this.offline_manual === true) {
					globalThis.offline = true;
					window.dispatchEvent(new CustomEvent("scouting_offline"));
				}

				if (this.offline !== !navigator.onLine) {
					this.offline = !navigator.onLine;
					globalThis.offline = !navigator.onLine;

					if (this.offline) {
						globalThis.offline = true;
						window.dispatchEvent(new CustomEvent("scouting_offline"));
						this.show_notification(
							"Device offline",
							"You're now offline. Some features will be reduced until you're back online.",
							"wifi-slash",
						);
					} else {
						globalThis.offline = false;
						window.dispatchEvent(new CustomEvent("scouting_online"));
						this.show_notification(
							"Device online",
							"You're back online.",
							"wifi-high",
						);
					}
				}
			}
		},

		/**
		 * Show a notification across the application
		 *
		 * @param {string} title - The title of the notification
		 * @param {string} body - The body of the notification
		 * @param {string} icon - The icon of the notification (As a Phosphor icon, omit the 'ph-' part)
		 */
		show_notification(title, body, icon) {
			if (this.notification_shown) {
				this.hide_notification();
			}

			this.notification.title = title;
			this.notification.body = body;
			this.notification.icon = icon;
			this.notification.icon_class = `ph-bold ph-${icon}`;
			this.notification_shown = true;

			setTimeout(() => {
				this.hide_notification();
			}, 5000);
		},

		/**
		 * Hide the currently shown notification
		 */
		hide_notification() {
			this.notification_shown = false;
			this.notification.title = "";
			this.notification.body = "";
			this.notification.icon = "";
		},

		/**
		 * Set the document to dark mode or light mode
		 */
		update_dark_mode() {
			if (this.dark_mode) {
				document.documentElement.classList.add("dark");
				localStorage.setItem("theme", "dark");
			} else {
				document.documentElement.classList.remove("dark");
				localStorage.setItem("theme", "light");
			}
		},

		/**
		 * Toggle between dark and light mode
		 */
		toggle_dark_mode() {
			this.dark_mode = !this.dark_mode;
			this.update_dark_mode();
		},

		/**
		 * Clear the service worker cache
		 */
		async clear_service_worker_cache() {
			await caches.delete("v1");
		},

		/**
		 * Toggles the mode of the service worker from cache first to and network first
		 */
		async toggle_service_worker_mode() {
			this.service_worker_cache_first = !this.service_worker_cache_first;
			localStorage.setItem(
				"service_worker_cache_first",
				this.service_worker_cache_first,
			);
			await caches.delete("v1");

			location.reload();
		},

		/**
		 * Clear the IndexedDB database
		 */
		clear_database() {
			db.offline_reports.clear();
			db.backups.clear();
			db.pit_scouting.clear();
			db.delete();

			window.location.href = SERVER_IP;
		},

		/**
		 * Toggles the offline mode manually
		 */
		toggle_offline_manual() {
			this.offline_manual = !this.offline_manual;
			this.offline_manual_last = true;
			localStorage.setItem("offline_manual", this.offline_manual);

			window.dispatchEvent(new CustomEvent("sw_update_offline_manual"));
		},

		/**
		 * Check if there's any offline reports that can be uploaded
		 */
		check_for_offline_reports() {
			if (globalThis.offline === false) {
				db.offline_reports
					.count()
					.then((count) => {
						if (count > 0) {
							this.offline_reports = true;
							this.show_notification(
								"Reports available to upload.",
								`You have ${count} reports that were saved offline ready to upload`,
								"cloud-arrow-up",
							);
						} else {
							this.offline_reports = false;
						}
					})
					.catch((error) => {
						log("WARNING", `Error counting offline reports: ${error}`);
					});
			} else {
				this.offline_reports = false;
			}
		},

		/**
		 * Upload offline reports to the server
		 */
		upload_offline_reports() {
			db.offline_reports
				.toArray()
				.then((reports) => {
					const report_list = [];

					for (report in reports) {
						const data = {
							uuid: reports[report].uuid,
							data: reports[report].data,
							event_name: reports[report].event_name,
							event_code: reports[report].event_code,
							custom: reports[report].custom,
							year: reports[report].year,
						};

						report_list.push(data);
					}

					const response = fetch(`${SERVER_IP}/upload_offline_reports`, {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
							"X-CSRFToken": CSRF_TOKEN,
						},
						body: JSON.stringify({
							data: encodeURIComponent(JSON.stringify(report_list)),
						}),
					});

					response.then((res) => {
						if (res.ok) {
							db.offline_reports.clear().then(() => {
								this.offline_reports = false;
								this.show_notification(
									"Reports have been uploaded",
									"All your reports have been stored on the server",
									"check-circle",
								);
							});
						} else {
							log("WARNING", "There was an issue uploading scouting reports");
							this.show_notification(
								"There was an issue uploading scouting reports",
								"Your reports may have not been uploaded",
								"warning",
							);
						}
					});
				})
				.catch((error) => {
					log("WARNING", `Error adding data to the database: ${error}`);
				});
		},

		/**
		 * Check for any offline pit scouting data that can be uploaded to the server
		 */
		check_for_offline_pit_scouting() {
			if (globalThis.offline === false) {
				db.pit_scouting
					.filter(
						(element) =>
							element.uuid !== "master_questions" &&
							element.needs_synced === true,
					)
					.count()
					.then((count) => {
						if (count > 0) {
							this.offline_pit_scouting = true;
							this.show_notification(
								"Pit scouting data ready to upload",
								`You have ${count} pit scouting data that are saved offline ready to upload`,
								"cloud-arrow-up",
							);
						} else {
							this.offline_pit_scouting = false;
						}
					})
					.catch((error) => {
						log("WARNING", `Error counting offline pit scouting: ${error}`);
					});
			} else {
				this.offline_pit_scouting = false;
			}
		},

		/**
		 * Upload offline pit scouting data to the server
		 */
		upload_offline_pit_scouting() {
			let upload_failed = false;

			db.pit_scouting
				.filter((item) => item.needs_synced === true)
				.toArray()
				.then(async (data) => {
					if (data.length > 0) {
						// There's changes that need synced

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
										custom: item.custom,
										team_number: item.team_number,
										nickname: item.nickname,
										questions: item.questions || [], // In case questions are empty, send a blank list
									}),
								});
								if (response.ok) {
									await db.pit_scouting.update(item.uuid, {
										needs_synced: false,
									});
								}
							} catch (error) {
								log("WARNING", "Menu: pit uploaded failed:", error);
								upload_failed = true;
							}
						}

						if (!upload_failed) {
							this.show_notification(
								"Pit scouting data has been uploaded",
								"All your pit scouting data has been stored on the server",
								"check-circle",
							);
						} else {
							this.show_notification(
								"There was an issue uploading pit scouting data",
								"Your pit scouting data may have not been uploaded",
								"warning",
							);
						}

						this.offline_pit_scouting = false;
					}
				});
		},

		/**
		 * Initialize the menu
		 *
		 * Sets up dark mode, checks if the is offline, sets up the service worker,
		 * and checks if there's any offline reports that can be uploaded
		 */
		init() {
			if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
				this.dark_mode = true;
			} else {
				this.dark_mode = false;
			}

			this.update_dark_mode();

			this.service_worker_cache_first = JSON.parse(
				localStorage.getItem("service_worker_cache_first"),
			);
			this.offline_manual = JSON.parse(localStorage.getItem("offline_manual"));

			if (this.offline_manual == true) {
				this.offline_manual_last = true;
			}

			globalThis.offline = false;

			this.offline_check();

			// Check every half a second if the user is offline or not
			setInterval(() => {
				this.offline_check();
			}, 500);

			window.addEventListener("scouting_notification", (event) => {
				event.stopImmediatePropagation();
				const { title, body, icon } = event.detail;
				this.show_notification(title, body, icon);
			});

			this.check_for_offline_reports();
			this.check_for_offline_pit_scouting();

			window.addEventListener("scouting_online", (event) => {
				this.check_for_offline_reports();
				this.check_for_offline_pit_scouting();
			});

			window.addEventListener("storage_warning", (event) => {
				this.storage_warning = true;
			});

			window.addEventListener("version", (event) => {
				const { CLIENT_VERSION } = event.detail;

				this.version = CLIENT_VERSION;
			});

			// this.show_notification('Open Scouting', 'Welcome to Open Scouting!', 'star');
		},
	}));
});
