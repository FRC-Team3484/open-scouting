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
}
