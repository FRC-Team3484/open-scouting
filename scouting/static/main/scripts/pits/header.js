document.addEventListener("alpine:init", () => {
	Alpine.data("header", () => ({
		demo: false,
		page_dropdown: false,
		page_path: "/pits",

		/**
		 * Redirects to the contribute page using the current event information
		 */
		go_to_contribute() {
			const url = new URL(window.location.href);
			url.pathname = url.pathname.replace(this.page_path, "/contribute");
			window.location.href = url.toString();
		},

		/**
		 * Navigates to the advanced data page using the current event information
		 */
		go_to_advanced_data() {
			const url = new URL(window.location.href);
			const eventCode = url.searchParams.get("event_code");
			const year = url.searchParams.get("year");

			window.location.href = `/advanced_data?year=${year}&events=${eventCode}`;
		},

		/**
		 * Redirects to the pits page using the current event information
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
