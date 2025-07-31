/**
 * Handles the user status and settings, and automatically stores them locally
 */

class User {
	constructor() {
		this.authenticated = false;
		this.username = "";
		this.display_name = "";
		this.team_number = "";
		this.is_staff = false;
		this.is_superuser = false;
		this.settings = [];
		this.loading_settings = null;
	}

	/**
	 * Checks with the server if the user is authenticated or not
	 *
	 * This is saved in local storage for offline use
	 */
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
						is_staff: json.is_staff,
						is_superuser: json.is_superuser,
					};

					this.username = json.username;
					this.display_name = json.display_name;
					this.team_number = json.team_number;
					this.is_staff = json.is_staff;
					this.is_superuser = json.is_superuser;
					localStorage.setItem("authenticated", JSON.stringify(auth_json));
				} else {
					this.authenticated = false;
					const auth_json = {
						authenticated: json.authenticated,
						username: json.username,
						display_name: json.display_name,
						team_number: json.team_number,
						is_staff: json.is_staff,
						is_superuser: json.is_superuser,
					};

					this.username = json.username;
					this.display_name = json.display_name;
					this.team_number = json.team_number;
					this.is_staff = json.is_staff;
					this.is_superuser = json.is_superuser;
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
					is_staff: false,
					is_superuser: false,
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
				this.is_staff = JSON.parse(
					localStorage.getItem("authenticated"),
				).is_staff;
				this.is_superuser = JSON.parse(
					localStorage.getItem("authenticated"),
				).is_superuser;
			} else {
				this.authenticated = false;
			}
		}
	}

	/**
	 * Signs the user out and reloads the page
	 */
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

	/**
	 * Gets the user settings from the server
	 */
	async load_settings() {
		if (!this.authenticated) {
			this.settings = null;
			return;
		}

		// Return same promise if already loading
		if (this.loading_settings) return this.loading_settings;

		this.loading_settings = (async () => {
			if (globalThis.offline === false) {
				try {
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
				} catch (err) {
					log("ERROR", "Settings fetch failed:", err);
					this.settings = null;
				}
			} else {
				const stored = localStorage.getItem("settings");
				this.settings = stored ? JSON.parse(stored) : null;
			}

			// clear the promise cache
			this.loading_settings = null;
		})();

		return this.loading_settings;
	}

	/**
	 * Sets the user settings on the server
	 */
	async save_settings(notify = false) {
		if (this.authenticated) {
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
						if (notify) {
							window.dispatchEvent(
								new CustomEvent("scouting_notification", {
									detail: {
										title: "Settings saved",
										message: "Your settings have been successfully saved",
										type: "success",
										icon: "check-circle",
									},
								}),
							);
						}
					});
				} else {
					log("WARNING", "Unable to save settings to the server");
				}
			} else {
				log("WARNING", "Unable to save settings offline");
			}
		}
	}

	/**
	 * Gets the value of a setting
	 */
	async get_setting(key) {
		if (!this.settings) {
			await this.load_settings(); // Load if not present
		}
		if (this.settings === null) {
			return;
		}
		const found = this.settings.find((item) => item.key === key);
		return found ? found.value : null;
	}

	/**
	 * Gets all settings
	 */
	async get_all_settings() {
		if (!this.settings) {
			await this.load_settings();
		}
		if (this.settings === null) {
			return [];
		}
		return this.settings;
	}

	/**
	 * Sets the value of a setting
	 */
	async set_setting(key, value) {
		if (!this.settings) {
			await this.load_settings();
		}

		if (this.settings === null) {
			return;
		}

		const existing = this.settings.find((item) => item.key === key);
		if (existing) {
			existing.value = value;
		}

		localStorage.setItem("settings", JSON.stringify(this.settings));
	}
}
