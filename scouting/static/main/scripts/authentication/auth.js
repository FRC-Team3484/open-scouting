/**
 * Handles the client side code for the authentication page
 *
 * Goes through the steps of creating an account and signing in,
 * sends and checks verification codes,
 * and tells the server to authenticate and create accounts
 */

document.addEventListener("alpine:init", () => {
	Alpine.data("auth", () => ({
		sign_in: true,
		create_account_page: 1,
		forgot_password: false,
		forgot_password_page: 1,
		forgot_password_error: "",
		sending_forgot_password: false,
		forgot_password_user: "",
		forgot_password_code: "",
		forgot_password_email: "",
		user: {
			uuid: "",
			display_name: "",
			team_number: "",
			email: "",
			password: "",
		},
		team_number: {
			show: false,
			show_image: false,
			nickname: "",
			avatar: "",
		},
		password_strength: "",
		verification_code_error: "",
		verification_code_success: "",
		create_account_error: "",
		sending_email: false,
		sign_in_error: "",
		sign_in_show_password: false,
		EMAIL_ENABLED: EMAIL_ENABLED,

		/**
		 * Reset the create account form
		 */
		create_account_start_over() {
			this.$refs.create_display_name.value = "";
			this.$refs.create_team_number.value = "";
			this.$refs.create_email.value = "";
			this.$refs.create_verification_code.value = "";
			this.$refs.create_password.value = "";
			this.create_account_page = 1;

			this.team_number.show = false;

			this.user.uuid = "";
			this.user.email = "";

			this.password_strength = "";
			this.verification_code_error = "";
			this.verification_code_success = "";
			this.sending_email = false;

			this.check_display_name_and_team_number();
			this.check_email();
		},

		/**
		 * Display the team number's nickname and avatar
		 *
		 * @param {Event} e
		 */
		async display_team_number(e) {
			const current_season = await fetch(
				"https://www.thebluealliance.com/api/v3/status",
				{
					method: "GET",
					headers: {
						"X-TBA-Auth-Key": "{{ TBA_API_KEY }}",
					},
				},
			);

			if (current_season.ok) {
				const current_season_data = await current_season.json();

				try {
					const response = await fetch(
						`https://www.thebluealliance.com/api/v3/team/frc${e.target.value}`,
						{
							method: "GET",
							headers: {
								"X-TBA-Auth-Key": "{{ TBA_API_KEY }}",
							},
						},
					);

					if (response.ok) {
						const data = await response.json();
						this.team_number.nickname = data.nickname;
						this.team_number.avatar = `https://www.thebluealliance.com/avatar/${current_season_data.current_season}/frc${e.target.value}.png`;
						this.team_number.show = true;
						this.team_number.show_image = true;
					} else if (response.status === 404) {
						this.team_number.show = false;
					}
				} catch {}
			}
		},

		/**
		 * Check the display name and team number fields and set the next button to be disabled or not if the fields are valid
		 */
		check_display_name_and_team_number() {
			if (
				this.$refs.create_display_name.value &&
				this.$refs.create_team_number.value
			) {
				this.$refs.create_display_name_team_number_next.disabled = false;
			} else {
				this.$refs.create_display_name_team_number_next.disabled = true;
			}
		},

		/**
		 * Check the email field and set the next button to be disabled or not if the fields are valid
		 */
		check_email() {
			if (
				this.$refs.create_email.value?.includes("@") &&
				this.$refs.create_email.value.includes(".")
			) {
				this.$refs.create_email_next.disabled = false;
			} else {
				this.$refs.create_email_next.disabled = true;
			}
		},

		/**
		 * Check the verification code field and set the next button to be disabled or not if the fields are valid
		 */
		check_verification_code_fields() {
			if (this.$refs.create_verification_code.value) {
				this.$refs.create_verify_next.disabled = false;
			} else {
				this.$refs.create_verify_next.disabled = true;
			}
		},

		/**
		 * Tell the server to create a verification code and send it to the user's email
		 * If email isn't enabled, skips this step
		 */
		async send_verification_code() {
			this.user.email = this.$refs.create_email.value;
			this.user.uuid = crypto.randomUUID();

			this.$refs.create_email_next.disabled = true;

			if (this.EMAIL_ENABLED) {
				const response = await fetch(
					`${SERVER_IP}/authentication/send_verification_code`,
					{
						method: "POST",
						headers: {
							"X-CSRFToken": CSRF_TOKEN,
							"Content-Type": "application/json",
						},
						body: JSON.stringify({
							uuid: this.user.uuid,
							email: this.$refs.create_email.value,
							display_name: this.$refs.create_display_name.value,
						}),
					},
				);

				if (response.ok) {
					response.json().then(async (json) => {
						this.create_account_page = 3;
					});
				} else {
					response.text().then(async (text) => {
						log("WARNING", "Unable to send verification code");
					});
				}
			} else {
				this.create_account_page = 4;
			}
		},

		/**
		 * Check if the verification code the user entered is valid with the server
		 */
		async check_verification_code() {
			const response = await fetch(
				`${SERVER_IP}/authentication/check_verification_code`,
				{
					method: "POST",
					headers: {
						"X-CSRFToken": CSRF_TOKEN,
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						code: this.$refs.create_verification_code.value,
						user_uuid: this.user.uuid,
					}),
				},
			);

			if (response.ok) {
				response.json().then(async (json) => {
					log("INFO", "Verification code is valid");
					this.verification_code_success = "Your email has been verified!";
					this.create_account_page = 4;
				});
			} else {
				response.json().then(async (json) => {
					if (json.reason === "expired") {
						this.verification_code_error =
							"The verification code has expired. Use the 'Resend Code' to send a new one.";
					} else if (json.reason === "does_not_exist") {
						this.verification_code_error =
							"The verification code is incorrect!";
					}
				});
			}
		},

		/**
		 * Check the password field for the strength and show how strong the user's password is
		 */
		check_password_field_and_strength() {
			if (this.$refs.create_password.value) {
				this.$refs.create_create_account.disabled = false;
			} else {
				this.$refs.create_create_account.disabled = true;
			}

			let password_strength = 0;

			if (this.$refs.create_password.value.length >= 8) {
				password_strength += 1;
			}

			if (this.$refs.create_password.value.match(/[A-Z]/)) {
				password_strength += 1;
			}

			if (this.$refs.create_password.value.match(/[0-9]/)) {
				password_strength += 1;
			}

			if (
				this.$refs.create_password.value.match(/[!@#$%^&*(),.?":{}|<>\-_=+]/)
			) {
				password_strength += 1;
			}

			if (this.$refs.create_password.value === "") {
				this.password_strength = "";
			}

			if (password_strength === 0) {
				this.password_strength = "Poor Password";
			} else if (password_strength === 1) {
				this.password_strength = "Weak Password";
			} else if (password_strength === 2) {
				this.password_strength = "Okay Password";
			} else if (password_strength === 3) {
				this.password_strength = "Strong Password";
			} else if (password_strength === 4) {
				this.password_strength = "Very Strong Password";
			} else {
				this.password_strength = "";
			}
		},

		/**
		 * Toggles the visibility of the password field when the "Show password" checkbox is pressed
		 */
		check_password_visibility() {
			if (this.$refs.create_password.type === "password") {
				this.$refs.create_password.type = "text";
				this.$refs.create_password_visibility_label.innerText = "Hide";
			} else {
				this.$refs.create_password.type = "password";
				this.$refs.create_password_visibility_label.innerText = "Show";
			}
		},

		/**
		 * Create the account on the server
		 */
		async create_account() {
			const response = await fetch(
				`${SERVER_IP}/authentication/create_account`,
				{
					method: "POST",
					headers: {
						"X-CSRFToken": CSRF_TOKEN,
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						uuid: this.user.uuid,
						display_name: this.$refs.create_display_name.value,
						team_number: this.$refs.create_team_number.value,
						email: this.$refs.create_email.value,
						password: this.$refs.create_password.value,
						verify: this.EMAIL_ENABLED,
					}),
				},
			);

			if (response.ok) {
				response.text().then(async (text) => {
					log("INFO", "Account has been created!");

					this.create_account_page = 5;
					setTimeout(() => this.go_to_index(), 10000);
				});
			} else {
				response.text().then(async (text) => {
					this.verification_code_success = "";

					if (text === "username_exists") {
						this.create_account_error =
							"A user with that username already exists. Reload this page or press 'Start Over' to create an account with a different username";
					} else if (text === "error") {
						this.create_account_error =
							"There was an issue creating your account";
					} else {
						this.create_account_error =
							"There was an unknown issue creating your account";
						log("ERROR", text);
					}
				});
			}
		},

		/**
		 * Check the email and password fields for the sign in form, if the fields aren't valid don't show the sign in button
		 */
		check_sign_in_fields() {
			if (this.$refs.sign_in_email.value && this.$refs.sign_in_password.value) {
				this.$refs.sign_in_button.disabled = false;
			} else {
				this.$refs.sign_in_button.disabled = true;
			}
		},

		/**
		 * Check if the user is offline to present a confirmation to sign in
		 */
		check_sign_in() {
			if (globalThis.offline === false) {
				this.sign_in_request();
			} else {
				window.dispatchEvent(
					new CustomEvent("dialog_show", {
						detail: {
							event_name: "sign_in",
							title: "Signing in will clear page cache",
							body: "You're currently offline. Signing in will reset any cached pages to make sure your user is actually signed in. Those pages will not be able to be cached again until you're online, so the site may not work properly if you proceed. Are you sure you want to sign in?",
							buttons: [
								{ type: "confirm", icon: "ph-bold ph-check", text: "Sign in" },
								{ type: "cancel", icon: "ph-bold ph-x", text: "Not now" },
							],
						},
					}),
				);
			}
		},

		/**
		 * Send the sign in request to the server
		 *
		 * If the request is successful, go to the index page
		 */
		async sign_in_request() {
			const response = await fetch(`${SERVER_IP}/authentication/sign_in`, {
				method: "POST",
				headers: {
					"X-CSRFToken": CSRF_TOKEN,
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					email: this.$refs.sign_in_email.value,
					password: this.$refs.sign_in_password.value,
				}),
			});

			if (response.ok) {
				response.text().then(async (text) => {
					// Clear service worker cache
					await caches.delete("v1");

					this.go_to_index();
				});
			} else {
				response.text().then(async (text) => {
					if (text === "incorrect_credentials") {
						this.sign_in_error = "Your username or password is incorrect";
					} else if (text === "error") {
						this.sign_in_error = "There was an issue signing you in";
					} else {
						this.sign_in_error = "There was an unknown issue signing you in";
					}
				});
			}
		},

		/**
		 * Go to the index page
		 */
		go_to_index() {
			window.location.href = `${SERVER_IP}/`;
		},

		cancel_forgot_password() {
			this.forgot_password_page = 1;
			this.$refs.forgot_password_email.value = "";
			this.$refs.forgot_password_email_next.disabled = true;
			this.$refs.forgot_password_verification_code.value = "";
			this.$refs.forgot_password_verify_next.disabled = true;
			this.$refs.forgot_password_password.value = "";
			this.$refs.forgot_password_password_next.disabled = true;

			this.forgot_password_user = "";
			this.sending_forgot_password = false;

			this.forgot_password_error = "";
			this.forgot_password = false;
		},

		async send_forgot_password_email() {
			const email = this.$refs.forgot_password_email.value;
			this.forgot_password_email = email;

			this.$refs.forgot_password_email_next.disabled = true;
			this.sending_forgot_password = true;

			if (this.EMAIL_ENABLED) {
				const response = await fetch(
					`${SERVER_IP}/authentication/forgot_password`,
					{
						method: "POST",
						headers: {
							"X-CSRFToken": CSRF_TOKEN,
							"Content-Type": "application/json",
						},
						body: JSON.stringify({
							email: email,
						}),
					},
				);

				if (response.ok) {
					response.json().then(async (json) => {
						this.forgot_password_user = json.user_uuid;
						this.sending_forgot_password = false;

						this.forgot_password_page = 2;
					});
				} else {
					response.text().then(async (text) => {
						log("WARNING", "Unable to send verification code");
						this.sending_forgot_password = false;
						this.forgot_password_error = "Unable to send verification code";
					});
				}
			} else {
				this.sending_forgot_password = false;

				this.forgot_password_page = 3;
			}
		},

		async verify_forgot_password_code() {
			const response = await fetch(
				`${SERVER_IP}/authentication/check_verification_code`,
				{
					method: "POST",
					headers: {
						"X-CSRFToken": CSRF_TOKEN,
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						code: this.$refs.forgot_password_verification_code.value,
						user_uuid: this.forgot_password_user,
					}),
				},
			);

			if (response.ok) {
				response.json().then(async (json) => {
					log("INFO", "Verification code is valid");
					this.forgot_password_page = 3;
					this.forgot_password_code =
						this.$refs.forgot_password_verification_code.value;
				});
			} else {
				response.json().then(async (json) => {
					if (json.reason === "expired") {
						this.forgot_password_error =
							"The verification code has expired. Use the 'Resend Code' to send a new one.";
					} else if (json.reason === "does_not_exist") {
						this.forgot_password_error = "The verification code is incorrect!";
					}
				});
			}
		},

		async change_password() {
			let unsafe = false;
			let user_uuid = this.forgot_password_user;

			if (this.EMAIL_ENABLED) {
				unsafe = false;
				user_uuid = this.forgot_password_user;
			} else {
				unsafe = true;
				user_uuid = this.forgot_password_email;
			}

			const response = await fetch(
				`${SERVER_IP}/authentication/change_password`,
				{
					method: "POST",
					headers: {
						"X-CSRFToken": CSRF_TOKEN,
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						password: this.$refs.forgot_password_password.value,
						user_uuid: user_uuid,
						code: this.forgot_password_code,
						unsafe: unsafe,
					}),
				},
			);

			if (response.ok) {
				response.text().then(async (text) => {
					log("INFO", "Password changed successfully");
					this.forgot_password_page = 4;

					setTimeout(() => {
						this.cancel_forgot_password();
					}, 5000);
				});
			} else {
				response.text().then(async (text) => {
					if (text.reason === "expired") {
						this.forgot_password_error =
							"The verification code has expired. Use the 'Resend Code' to send a new one.";
					} else if (text.reason === "does_not_exist") {
						this.forgot_password_error = "The verification code is incorrect!";
					} else {
						this.forgot_password_error = `Unable to change password: ${text}`;
					}
				});
			}
		},

		init() {
			this.EMAIL_ENABLED = this.EMAIL_ENABLED === "True";

			window.addEventListener("dialog_confirm", (event) => {
				const { event_name } = event.detail;

				if (event_name === "sign_in") {
					event.stopImmediatePropagation();

					localStorage.setItem("offline_manual", false);
					window.dispatchEvent(new CustomEvent("sw_update_offline_manual"));

					this.sign_in_request();
				}
			});
		},
	}));
});
