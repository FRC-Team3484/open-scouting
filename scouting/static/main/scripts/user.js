/**
 * Handles the user status and settings, and automatically stores them locally
 */

class User {
	constructor() {
		this.authenticated = false;
		this.username = "";
		this.display_name = "";
		this.team_number = "";
	}

	async check_authentication_status() {
		if (globalThis.offline === false) {
			// Ask server for status
			const response = await fetch(
				`${SERVER_IP}/authentication/get_authentication_status`,
				{
					method: "POST",
					headers: {
						"X-CSRFToken": CSRF_TOKEN,
					},
				},
			);

			if (response.ok) {
				const json = await response.json();
				if (json.authenticated === true) {
					this.authenticated = true;
					const auth_json = {
						authenticated: json.authenticated,
						username: json.username,
						display_name: json.display_name,
						team_number: json.team_number,
					};

					this.username = json.username;
					this.display_name = json.display_name;
					this.team_number = json.team_number;
					localStorage.setItem("authenticated", JSON.stringify(auth_json));
				} else {
					this.authenticated = false;
					const auth_json = {
						authenticated: json.authenticated,
						username: json.username,
						display_name: json.display_name,
						team_number: json.team_number,
					};

					this.username = json.username;
					this.display_name = json.display_name;
					this.team_number = json.team_number;
					localStorage.setItem("authenticated", JSON.stringify(auth_json));
				}
			} else {
				log("WARNING", "Error getting authentication status");
				this.authenticated = false;
				const auth_json = {
					authenticated: false,
					username: "",
					display_name: "",
					team_number: "",
				};
				localStorage.setItem("authenticated", JSON.stringify(auth_json));
			}
		} else {
			// Check local storage for status
			if (JSON.parse(localStorage.getItem("authenticated")).authenticated) {
				this.authenticated = true;
				this.username = JSON.parse(
					localStorage.getItem("authenticated"),
				).username;
				this.display_name = JSON.parse(
					localStorage.getItem("authenticated"),
				).display_name;
				this.team_number = JSON.parse(
					localStorage.getItem("authenticated"),
				).team_number;
			} else {
				this.authenticated = false;
			}
		}
	}

	async sign_out() {
		const response = await fetch(`${SERVER_IP}/authentication/sign_out`, {
			method: "POST",
			headers: {
				"X-CSRFToken": CSRF_TOKEN,
			},
		});

		if (response.ok) {
			response.text().then(async (text) => {
				const auth_json = {
					authenticated: false,
					username: "",
					display_name: "",
					team_number: "",
				};

				localStorage.setItem("authenticated", JSON.stringify(auth_json));

				// Clear service worker cache
				await caches.delete("v1");

				window.location.reload();
			});
		} else {
			log("ERROR", "Error signing out");
		}
	}

	async get_settings() {
		if (globalThis.offline === false) {
			const response = await fetch(
				`${SERVER_IP}/authentication/get_user_settings`,
				{
					method: "POST",
					headers: {
						"X-CSRFToken": CSRF_TOKEN,
						"Content-Type": "application/json",
					},
				},
			);

			if (response.ok) {
				const json = await response.json();

				this.settings = json;
				localStorage.setItem("settings", JSON.stringify(json));
			} else {
				this.settings = null;
				log("WARNING", "Unable to get settings from the server");
			}
		} else {
			if (localStorage.getItem("settings")) {
				this.settings = JSON.parse(localStorage.getItem("settings"));
			} else {
				this.settings = null;
				log("WARNING", "Unable to get settings offline");
			}
		}
	}

	async set_settings() {
		if (globalThis.offline === false) {
			const response = await fetch(
				`${SERVER_IP}/authentication/set_user_settings`,
				{
					method: "POST",
					headers: {
						"X-CSRFToken": CSRF_TOKEN,
						"Content-Type": "application/json",
					},
					body: JSON.stringify(this.settings),
				},
			);

			if (response.ok) {
				response.text().then((text) => {
					window.dispatchEvent(
						new CustomEvent("scouting_notification", {
							detail: {
								title: "Settings saved",
								body: "Your settings have been successfully saved",
								icon: "check-circle",
							},
						}),
					);
				});
			} else {
				log("WARNING", "Unable to save settings to the server");
			}
		} else {
			log("WARNING", "Unable to save settings offline");
		}
	}

	async get_setting(setting) {
		console.log(this.settings);
		if (!this.settings) {
			await this.get_settings(); // Load if not present
		}
		const found = this.settings.find((item) => item.name === setting);
		return found ? found.value : null;
	}

	async get_all_settings() {
		if (!this.settings) {
			await this.get_settings();
		}
		return this.settings;
	}

	async set_setting(setting, value) {
		if (!this.settings) {
			await this.get_settings();
		}

		const existing = this.settings.find((item) => item.name === setting);
		if (existing) {
			existing.value = value;
		} else {
			this.settings.push({ name: setting, value, type: typeof value });
		}

		localStorage.setItem("settings", JSON.stringify(this.settings));
	}
}
