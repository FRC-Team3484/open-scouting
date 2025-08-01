window.addEventListener("alpine:init", () => {
	Alpine.data("notifications", () => ({
		notifications: [],
		show: false,
		title: "",
		message: "",
		type: "success",
		icon: "",
		isProcessing: false,

		add_notification(title, message, type = "info", icon = "bell") {
			this.notifications.push({ title, message, type, icon });
		},

		show_notification(title, message, type = "info", icon = "bell") {
			this.title = title;
			this.message = message;
			this.type = type;
			this.icon = `ph-bold ph-${icon}`;
			this.show = true;
		},

		async process_queue() {
			if (this.isProcessing) return;
			this.isProcessing = true;

			while (this.notifications.length > 0) {
				const { title, message, type, icon } = this.notifications.shift();
				this.show_notification(title, message, type, icon);
				await new Promise((resolve) => setTimeout(resolve, 3000)); // show duration
				this.show = false;
				await new Promise((resolve) => setTimeout(resolve, 500)); // let transition finish
			}

			this.isProcessing = false;
		},

		init() {
			window.addEventListener("scouting_notification", (event) => {
				event.stopImmediatePropagation();
				const { title, message, type, icon } = event.detail;

				this.add_notification(title, message, type, icon);
				this.process_queue();
			});

			setTimeout(() => {
				this.process_queue();
			}, 300);
		},
	}));
});
