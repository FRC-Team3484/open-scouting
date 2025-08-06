document.addEventListener("alpine:init", () => {
	Alpine.data("menu_logs", () => ({
		copy_to_clipboard(level, date, message) {
			navigator.clipboard.writeText(`${level} ${date} ${message}`);
		},

		copy_all_logs_to_clipboard() {
			const logText = logs
				.map((log) => `${log.level} ${log.date} ${log.message}`)
				.join("\n");
			navigator.clipboard.writeText(logText);

			setTimeout(() => {
				this.$refs.copy_all_logs_button.innerHTML = `<i class="ph-bold ph-clipboard-text"></i> ${gettext("Copy all logs")}`;
			}, 3000);
		},

		download_log_file() {
			const lines = logs.map(
				(log) => `${log.level} ${log.date} ${log.message}`,
			);
			const blob = new Blob([lines.join("\n")], {
				type: "text/plain",
			});
			const url = URL.createObjectURL(blob);
			const link = document.createElement("a");
			link.href = url;

			const date = new Date();
			const year = date.getFullYear().toString().padStart(4, "0");
			const month = (date.getMonth() + 1).toString().padStart(2, "0");
			const day = date.getDate().toString().padStart(2, "0");
			const hour = date.getHours().toString().padStart(2, "0");
			const minutes = date.getMinutes().toString().padStart(2, "0");
			const fileName = `open_scouting_log_${year}_${month}_${day}_${hour}_${minutes}.txt`;
			link.download = fileName;

			link.click();
		},
	}));
});
