document.addEventListener("alpine:init", () => {
	Alpine.data("profile", () => ({
		editing: false,
		user_id: "",
		display_name: "",
		team_number: "",

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
							title: "Signing out will clear page cache",
							body: "You're currently offline. Signing out will reset any cached pages to make sure your user is actually signed in. Those pages will not be able to be cached again until you're online, so the site may not work properly if you proceed. Are you sure you want to sign out?",
							buttons: [
								{ type: "confirm", icon: "ph-bold ph-check", text: "Sign out" },
								{ type: "cancel", icon: "ph-bold ph-x", text: "Not now" },
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

					window.location.href = "/";
				});
			} else {
				log("ERROR", "Error signing out");
			}
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
									title: "Profile saved",
									body: "Your profile details have been successfully saved",
									icon: "check-circle",
								},
							}),
						);
					}
				});
			}
		},

		init() {},
	}));
});
