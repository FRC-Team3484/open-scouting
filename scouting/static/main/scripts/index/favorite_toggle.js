document.addEventListener("alpine:init", () => {
	Alpine.data("favorite_toggle", () => ({
		isFavorite: false,
		loading: true,
		eventCode: "",

		init() {
			this.eventCode = this.$el.dataset.eventCode;
			this.updateStatus();

			window.addEventListener("favorite_updated", (event) => {
				if (event.detail.code === this.eventCode) {
					this.updateStatus();
				}
			});
		},

		async updateStatus() {
			const favorites = (await user.get_setting("favorite_events")) || [];
			this.isFavorite = favorites.includes(this.eventCode);
			this.loading = false;
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
			window.dispatchEvent(
				new CustomEvent("favorite_updated", {
					detail: { code: this.eventCode },
				}),
			);

			if (window.eventsComponent?.update_filters) {
				window.eventsComponent.update_filters();
			}

			window.dispatchEvent(
				new CustomEvent("favorite_updated", {
					detail: { code: this.eventCode },
				}),
			);
		},
	}));
});
