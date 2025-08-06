document.addEventListener("alpine:init", () => {
	Alpine.data("profile", () => ({
		editing: false,
		settings: false,
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

		init() {
			window.addEventListener("beforeunload", (event) => {
				if (this.settings || this.editing) {
					event.returnValue = gettext(
						"Are you sure you want to close the page? You have unsaved changes.",
					);
				}
			});
		},
	}));
});
