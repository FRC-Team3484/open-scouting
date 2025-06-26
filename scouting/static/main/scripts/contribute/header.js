document.addEventListener("alpine:init", () => {
	Alpine.data("header", () => ({
		demo: false,
		page_dropdown: false,
		page_path: "/contribute",

		/**
		 * Navigates to the contribute page using the current event information
		 */
		go_to_contribute() {
			const url = new URL(window.location.href);
			url.pathname = url.pathname.replace(this.page_path, "/contribute");
			window.location.href = url.toString();
		},

		/**
		 * Navigates to the pit scouting page using the current event information
		 */
		go_to_pits() {
			const url = new URL(window.location.href);
			url.pathname = url.pathname.replace(this.page_path, "/pits");
			window.location.href = url.toString();
		},

		init() {
			try {
				this.demo = JSON.parse(DEMO);
			} catch {
				this.demo = false;
			}
		},
	}));
});
