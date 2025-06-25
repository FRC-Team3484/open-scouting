document.addEventListener("alpine:init", () => {
	Alpine.data("favorite_toggle", () => ({
		isFavorite: false,
		loading: true,
		eventCode: "",

		async init(code) {
			this.eventCode = code;

			const favorites = (await user.get_setting("favorite_events")) || [];
			this.isFavorite = favorites.includes(this.eventCode);
			this.loading = false;

			window.addEventListener("storage", (event) => {
				if (event.key === "settings") {
					this.updateStatus();
				}
			});
		},

		async toggleFavorite() {
			let favorites = (await user.get_setting("favorite_events")) || [];

			if (this.isFavorite) {
				favorites = favorites.filter((code) => code !== this.eventCode);
			} else {
				if (!favorites.includes(this.eventCode)) {
					favorites.push(this.eventCode);
				}
			}

			await user.set_setting("favorite_events", favorites);
			await user.save_settings();

			this.isFavorite = !this.isFavorite;

			if (window.eventsComponent?.update_filters) {
				window.eventsComponent.update_filters();
			}
		},
	}));
});
