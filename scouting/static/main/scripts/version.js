import semver from "https://esm.sh/semver";
/**
 * Handles comparing versions of the client and server, and if the client version is older than the server version,
 * prompt the user to clear their service worker cache to ensure all pages are up to date
 */

const CLIENT_VERSION = "v0.1.10-alpha";
async function get_server_version() {
	if (!navigator.onLine) {
		log(
			"WARNING",
			"The user is offline, so the client is unable to check for updates",
		);
		return false;
	}

	const response = await fetch(`${SERVER_IP}/get_version`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
	});

	if (response.ok) {
		return await response.json();
		// biome-ignore lint/style/noUselessElse: <explanation>
	} else {
		log("WARNING", `Failed to get server version: ${response.statusText}`);
		return false;
	}
}

/**
 * Print a startup message to the console
 *
 * Open Scouting (version)
 * github.com/FRC-Team3484/open-scouting
 */
console.log(
	`%c\n\nOpen Scouting %c${CLIENT_VERSION}\n%cgithub.com/FRC-Team3484/open-scouting\n\n\n`,
	"color: #ff5151; font-weight: bold;",
	"color: #9e9e9eb3;",
	"color: #45b0ff;",
);

window.addEventListener("dialog_confirm", (event) => {
	const { event_name } = event.detail;

	if (event_name === "client_update") {
		event.stopImmediatePropagation();

		caches.delete("v1");

		location.reload();
	}
});

get_server_version().then((server_version) => {
	if (server_version) {
		if (semver.lt(CLIENT_VERSION, server_version.version)) {
			log(
				"WARNING",
				`Client version ${CLIENT_VERSION} is older than server version ${server_version.version}`,
			);
			window.dispatchEvent(
				new CustomEvent("dialog_show", {
					detail: {
						event_name: "client_update",
						title: "Client update available",
						body: "You currently have old client files cached. It's recommended to clear your service worker cache to ensure all client side code is up to date. Do you wish to clear your cache now?",
						buttons: [
							{
								type: "confirm",
								icon: "ph-bold ph-check",
								text: "Clear cache",
							},
							{ type: "cancel", icon: "ph-bold ph-x", text: "Not now" },
						],
					},
				}),
			);
		} else {
			log("INFO", `Client version ${CLIENT_VERSION} is up to date`);
		}
	}
});

window.dispatchEvent(
	new CustomEvent("version", {
		detail: { CLIENT_VERSION },
	}),
);
