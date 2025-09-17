document.addEventListener("alpine:init", () => {
	Alpine.data("profile", () => ({
		editing: false,
		settings: false,
		api: false,
		api_creating: false,
		user_id: "",
		display_name: "",
		team_number: "",
		api_keys: [],
		api_name: "",
		api_expiry: 7,
		api_key_to_revoke: "",
		api_key_to_copy: "",

		/**
		 * Checks if the user is online before signing them out
		 */
		sign_out_check() {
			if (globalThis.offline === false) {
				this.sign_out();
			} else {
				window.dispatchEvent(
					new CustomEvent("dialog_show", {
						detail: {
							event_name: "sign_out",
							title: gettext("Signing out will clear page cache"),
							body: gettext(
								"You're currently offline. Signing out will reset any cached pages to make sure your user is actually signed in. Those pages will not be able to be cached again until you're online, so the site may not work properly if you proceed. Are you sure you want to sign out?",
							),
							buttons: [
								{
									type: "confirm",
									icon: "ph-bold ph-check",
									text: gettext("Sign out"),
								},
								{
									type: "cancel",
									icon: "ph-bold ph-x",
									text: gettext("Not now"),
								},
							],
						},
					}),
				);
			}
		},

		/**
		 * Asks the server to sign the user out
		 */
		async sign_out() {
			user.sign_out();
		},

		async save_profile() {
			const response = await fetch(`${SERVER_IP}/authentication/save_profile`, {
				method: "POST",
				headers: {
					"X-CSRFToken": CSRF_TOKEN,
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					user_id: this.user_id,
					display_name: this.display_name,
					team_number: this.team_number,
				}),
			});

			if (response.ok) {
				response.text().then((text) => {
					if (text === "success") {
						this.editing = false;

						window.dispatchEvent(
							new CustomEvent("scouting_notification", {
								detail: {
									title: gettext("Profile saved"),
									message: gettext(
										"Your profile details have been successfully saved",
									),
									type: "success",
									icon: "check-circle",
								},
							}),
						);
					}
				});
			}
		},

		async get_api_keys() {
			const response = await fetch(`${SERVER_IP}/authentication/get_api_keys`, {
				method: "POST",
				headers: {
					"X-CSRFToken": CSRF_TOKEN,
				},
			});

			if (response.ok) {
				this.api_keys = await response.json();
			}
		},

		async create_api_key() {
			const response = await fetch(`${SERVER_IP}/authentication/create_api_key`, {
				method: "POST",
				headers: {
					"X-CSRFToken": CSRF_TOKEN,
				},
				body: JSON.stringify({
					name: this.api_name,
					expires: this.api_expiry,
				}),
			});

			if (response.ok) {
				response.json().then((json) => {
					this.get_api_keys();

					this.api_key_to_copy = json.key;

					window.dispatchEvent(
						new CustomEvent("dialog_show", {
							detail: {
								event_name: "show_api_key",
								title: gettext("API Key Created"),
								body: json.key + gettext(" (You will not be able to see your key again)"),
								buttons: [
									{ type: "confirm", icon: "ph-bold ph-clipboard", text: "Copy" },
									{ type: "cancel", icon: "ph-bold ph-x", text: "Close" },
								],
							},
						}),
					);
				})
			}
		},

		async revoke_api_key(id) {
			const response = await fetch(
				`${SERVER_IP}/authentication/revoke_api_key`,
				{
					method: "POST",
					headers: {
						"X-CSRFToken": CSRF_TOKEN,
					},
					body: JSON.stringify({
						id: id,
					}),
				},
			);

			if (response.ok) {
				this.get_api_keys();
				this.api_key_to_revoke = "";
			}
		},

		prompt_revoke() {
			window.dispatchEvent(
				new CustomEvent("dialog_show", {
					detail: {
						event_name: "revoke_api_key",
						title: gettext("Are you sure you want to revoke this API key?"),
						body: gettext("You will no longer be able to use this API key, and any applications using it will no longer work. Are you sure you want to continue?"),
						buttons: [
							{ type: "confirm", icon: "ph-bold ph-check", text: "Revoke" },
							{ type: "cancel", icon: "ph-bold ph-x", text: "Cancel" },
						],
					},
				}),
			);
		},

		init() {
			window.addEventListener("beforeunload", (event) => {
				if (this.settings || this.editing || this.api_creating) {
					event.returnValue = gettext(
						"Are you sure you want to close the page? You have unsaved changes.",
					);
				}
			});

			window.addEventListener("dialog_confirm", (event) => {
				const { event_name } = event.detail;

				if (event_name === "revoke_api_key") {
					event.stopImmediatePropagation();

					this.revoke_api_key(this.api_key_to_revoke);
				} else if (event_name === "show_api_key") {
					event.stopImmediatePropagation();

					navigator.clipboard.writeText(this.api_key_to_copy);
					this.api_key_to_copy = "";

					window.dispatchEvent(
						new CustomEvent("scouting_notification", {
							detail: {
								title: gettext("API Key Copied!"),
								message: gettext("The API key has been copied to your clipboard"),
								type: "info",
								icon: "clipboard",
							},
						}),
					);
				}
			});

			this.get_api_keys();

		},
	}));
});
