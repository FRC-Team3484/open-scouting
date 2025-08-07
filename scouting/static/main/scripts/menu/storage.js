document.addEventListener("alpine:init", () => {
	Alpine.data("menu_storage", () => ({
		total: 0,
		used: 0,
		report_backups: 0,
		offline_reports: 0,
		pit_scouting: 0,
		pit_scouting_unsaved: 0,

		async get_data() {
			const quota = await navigator.storage.estimate();
			this.total = quota.quota;
			this.used = quota.usage;

			db.backups.count().then((count) => {
				this.report_backups = count;
			});

			db.offline_reports.count().then((count) => {
				this.offline_reports = count;
			});

			db.pit_scouting.count().then((count) => {
				this.pit_scouting = count;
			});

			db.pit_scouting
				.filter((item) => item.needs_synced === true)
				.count()
				.then((count) => {
					this.pit_scouting_unsaved = count;
				})
				.catch((error) => {
					log("WARNING", `Error counting unsaved changes: ${error}`);
				});
		},

		clear_backups_dialog() {
			window.dispatchEvent(
				new CustomEvent("dialog_show", {
					detail: {
						event_name: "clear_backups",
						title: gettext(
							"Are you sure you want to clear your report backups?",
						),
						body: gettext(
							"This will permanently delete all of your report backups and cannot be undone. Are you sure you want to continue?",
						),
						buttons: [
							{
								type: "confirm",
								icon: "ph-bold ph-check",
								text: gettext("Clear"),
							},
							{ type: "cancel", icon: "ph-bold ph-x", text: gettext("Cancel") },
						],
					},
				}),
			);
		},

		clear_offline_reports_dialog() {
			window.dispatchEvent(
				new CustomEvent("dialog_show", {
					detail: {
						event_name: "clear_offline_reports",
						title: gettext(
							"Are you sure you want to clear your offline scouting reports?",
						),
						body: gettext(
							"This will permanently delete all of your scouting reports that were not yet uploaded to the server, and this action cannot be undone. Are you sure you want to continue?",
						),
						buttons: [
							{
								type: "confirm",
								icon: "ph-bold ph-check",
								text: gettext("Clear"),
							},
							{ type: "cancel", icon: "ph-bold ph-x", text: gettext("Cancel") },
						],
					},
				}),
			);
		},

		clear_pit_scouting_dialog() {
			window.dispatchEvent(
				new CustomEvent("dialog_show", {
					detail: {
						event_name: "clear_pit_scouting",
						title: gettext(
							"Are you sure you want to clear your pit scouting data?",
						),
						body: gettext(
							"This will permanently delete all of your local pit scouting data, some of which may be unsaved. This action cannot be undone. Are you sure you want to continue?",
						),
						buttons: [
							{
								type: "confirm",
								icon: "ph-bold ph-check",
								text: gettext("Clear"),
							},
							{ type: "cancel", icon: "ph-bold ph-x", text: gettext("Cancel") },
						],
					},
				}),
			);
		},

		async init() {
			this.get_data();

			window.addEventListener("dialog_confirm", (event) => {
				const { event_name } = event.detail;
				if (event_name === "clear_backups") {
					db.backups.clear();
					this.get_data();
				} else if (event_name === "clear_offline_reports") {
					db.offline_reports.clear();
					this.get_data();
				} else if (event_name === "clear_pit_scouting") {
					db.pit_scouting.clear();
					this.get_data();
				}
			});

			if (this.used / this.total > 0.9) {
				window.dispatchEvent(
					new CustomEvent("scouting_notification", {
						detail: {
							title: gettext("Low storage space"),
							message: gettext(
								"Open Scouting is running low on storage that is allocated to it",
							),
							type: "warning",
							icon: "warning",
						},
					}),
				);

				window.dispatchEvent(new CustomEvent("storage_warning"));
			}
		},
	}));
});
