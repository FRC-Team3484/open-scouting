document.addEventListener("alpine:init", () => {
	Alpine.data("field_manager", () => ({
		field_data: SEASON_FIELDS,

		/**
		 * Sends an event with the match number for the team information component
		 */
		send_match_number() {
			window.dispatchEvent(
				new CustomEvent("match_number_change", {
					detail: {
						match_number: document.querySelector("input[name='match_number']")
							.value,
					},
				}),
			);
		},

		/**
		 * Sends an event with the match type for the team information component
		 */
		send_match_type() {
			window.dispatchEvent(
				new CustomEvent("match_type_change", {
					detail: {
						match_type: document.querySelector("select[name='match_type']")
							.value,
					},
				}),
			);
		},

		/**
		 * Creates a field element for the form
		 *
		 * @param {Object} field - The field object
		 * @returns {Object} The field element
		 */
		create_field(field) {
			let label_text;
			if (field.required === true) {
				label_text = `${field.name}*`;
			} else {
				label_text = `${field.name}`;
			}

			const label = document.createElement("label");
			label.innerText = label_text;
			label.classList = "dark:text-white text-black mb-2 text-sm text-sans";

			const field_container = document.createElement("div");
			field_container.classList =
				"flex flex-col mb-4 py-2 my-2 border-l-2 pl-2 dark:border-slate-700 border-slate-300 justify-left";

			let field_element;

			if (field.type === "large_integer") {
				field_element = document.createElement("input");
				field_element.type = "number";
				field_element.pattern = "[0-9]*";
				field_element.setAttribute("name", field.simple_name);
				field_element.setAttribute("x-ref", field.simple_name);
				field_element.classList =
					"dark:text-white text-black dark:bg-slate-700 bg-slate-300 rounded-sm px-2 py-1 mb-2";

				if (field.simple_name === "match_number") {
					field_element.setAttribute(
						"x-on:input.debounce.300ms",
						"send_match_number()",
					);
				}
			} else if (field.type === "integer") {
				field_element = document.createElement("div");
				field_element.classList =
					"flex flex-row align-center items-center justify-between";
				field_element.classList.add("field_other");
				field_element.setAttribute(
					"x-data",
					`{ value: ${field.default}, min: ${field.minimum}, max: ${field.maximum} }`,
				);
				field_element.setAttribute(
					"x-init",
					`if (localStorage.getItem('${field.simple_name}') !== null) value = parseInt(localStorage.getItem('${field.simple_name}'))`,
				);
				field_element.setAttribute("x-bind:value", "value");
				field_element.setAttribute("name", field.simple_name);
				field_element.setAttribute("x-ref", field.simple_name);

				const integer_text = document.createElement("p");
				integer_text.setAttribute("x-text", "value");
				integer_text.classList = "dark:text-white text-black text-xl font-bold";

				const integer_buttons = document.createElement("div");
				integer_buttons.classList = "flex flex-row";

				const integer_add_button = document.createElement("button");
				integer_add_button.classList = "ui_button_icon mx-2 touch-manipulation";
				integer_add_button.setAttribute(
					"x-on:click",
					"value < max ? value = value + 1 : null",
				);
				integer_add_button.innerHTML = `<i class="ph-bold ph-plus"></i>`;

				const integer_subtract_button = document.createElement("button");
				integer_subtract_button.classList =
					"ui_button_icon mx-2 touch-manipulation";
				integer_subtract_button.setAttribute(
					"x-on:click",
					"value > min ? value = value - 1 : null",
				);
				integer_subtract_button.innerHTML = `<i class="ph-bold ph-minus"></i>`;

				integer_buttons.appendChild(integer_add_button);
				integer_buttons.appendChild(integer_subtract_button);

				field_element.appendChild(integer_text);
				field_element.appendChild(integer_buttons);
			} else if (field.type === "boolean") {
				field_element = document.createElement("input");
				field_element.type = "checkbox";
				field_element.setAttribute("name", field.simple_name);
				field_element.setAttribute("x-ref", field.simple_name);
				field_element.classList = "ui_checkbox ml-auto mr-2 w-8! h-8!";
			} else if (field.type === "choice") {
				field_element = document.createElement("select");
				field_element.setAttribute("name", field.simple_name);
				field_element.setAttribute("x-ref", field.simple_name);
				field_element.classList =
					"dark:text-white text-black dark:bg-slate-700 bg-slate-300 rounded-sm px-2 py-1 mb-2";

				// Add choices as options
				for (const choice of field.choices) {
					const option = document.createElement("option");
					option.value = choice[1];
					option.text = choice[0];
					field_element.appendChild(option);
				}

				if (field.simple_name === "match_type") {
					field_element.setAttribute(
						"x-on:input.debounce.300ms",
						"send_match_type()",
					);
				}
			} else if (field.type === "multiple_choice") {
				field_element = document.createElement("select");
				field_element.setAttribute("name", field.simple_name);
				field_element.setAttribute("x-ref", field.simple_name);
				field_element.setAttribute("multiple", "multiple");
				field_element.classList =
					"dark:text-white text-black dark:bg-slate-700 bg-slate-300 rounded-sm px-2 py-1 mb-2";

				// Add multiple choices as options
				for (const choice of field.choices) {
					const option = document.createElement("option");
					option.value = choice[1];
					option.text = choice[0];
					field_element.appendChild(option);
				}
			} else if (field.type === "text") {
				field_element = document.createElement("input");
				field_element.type = "text";
				field_element.setAttribute("name", field.simple_name);
				field_element.setAttribute("x-ref", field.simple_name);
				field_element.classList =
					"dark:text-white text-black dark:bg-slate-700 bg-slate-300 rounded-sm px-2 py-1 mb-2";
			}

			if (field.required) {
				field_element.setAttribute("scouting_required", true);
			} else {
				field_element.setAttribute("scouting_required", false);
			}

			field_element.setAttribute("scouting_type", field.type);
			field_element.setAttribute("scouting_stat_type", field.stat_type);
			field_element.setAttribute("scouting_game_piece", field.game_piece);

			field_container.appendChild(label);
			field_container.appendChild(field_element);

			return field_container;
		},

		/**
		 * Create a section element for the form
		 *
		 * @param {Object} section The section object
		 * @returns {HTMLElement} The section element
		 */
		create_section(section) {
			const section_text_text = document.createElement("p");
			section_text_text.innerHTML = `<i class="ph-bold ph-arrow-bend-down-right"></i> ${section.section}`;
			section_text_text.classList =
				"dark:text-white text-black text-md text-sans";

			const section_text_icon_open = document.createElement("p");
			section_text_icon_open.innerHTML = "<i class='ph-bold ph-caret-up'></i>";
			section_text_icon_open.classList = "text-black dark:text-white";
			section_text_icon_open.setAttribute("x-show", "!open");

			const section_text_icon_close = document.createElement("p");
			section_text_icon_close.innerHTML =
				"<i class='ph-bold ph-caret-down'></i>";
			section_text_icon_close.classList = "text-black dark:text-white";
			section_text_icon_close.setAttribute("x-show", "open");

			const section_text = document.createElement("div");
			section_text.appendChild(section_text_text);
			section_text.appendChild(section_text_icon_open);
			section_text.appendChild(section_text_icon_close);
			section_text.classList =
				"dark:text-white text-black flex flex-row items-center justify-between cursor-pointer";

			section_text.setAttribute("x-on:click", "open = !open");

			const section_box = document.createElement("div");
			section_box.className = "section_box mt-2";
			section_box.setAttribute("x-show", "open");
			section_box.setAttribute("x-collapse", "");

			const section_element = document.createElement("div");
			section_element.setAttribute(
				"x-ref",
				section.simple_name ? section.simple_name : "no_simple_name",
			);
			section_element.classList =
				"dark:bg-slate-800 bg-slate-200 border-2 dark:border-slate-700 border-slate-300 rounded-lg mb-4 px-8 py-4 flex flex-col";
			section_element.setAttribute("x-data", "{ open: true }");

			section_element.appendChild(section_text);
			section_element.appendChild(section_box);

			return section_element;
		},

		/**
		 * Parses the field JSON data and builds fields and sections as needed, recursively
		 */
		parse_json(data, section) {
			for (const parent of data) {
				if (section) {
					// Create all sub fields inside
					if (parent.fields) {
						// If the item is a section
						const section_element = this.create_section(parent);
						section.querySelector(".section_box").appendChild(section_element);
						this.parse_json(parent.fields, section_element);
					} else {
						// If the item is a field
						section
							.querySelector(".section_box")
							.appendChild(this.create_field(parent));
					}
				} else {
					if (parent.fields) {
						// If the item is a section
						const section_element = this.create_section(parent);
						this.$root.appendChild(section_element);
						this.parse_json(parent.fields, section_element);
					} else {
						// If the item is a field
						this.$root.appendChild(this.create_field(parent));
					}
				}
			}
		},

		/**
		 * Loads the field state from localStorage
		 */
		load_field_state() {
			const inputs = document.querySelectorAll("input");
			for (const input of inputs) {
				const name = input.getAttribute("name");
				const value = localStorage.getItem(name);
				if (value) {
					if (
						input.getAttribute("scouting_type") === "large_integer" ||
						input.getAttribute("scouting_type") === "text"
					) {
						input.value = value;
					} else if (input.getAttribute("scouting_type") === "boolean") {
						input.checked = JSON.parse(value);
					}
				}
			}

			const selects = document.querySelectorAll("select");
			for (const select of selects) {
				const name = select.getAttribute("name");
				const value = localStorage.getItem(name);
				if (value) {
					select.value = value;
				}
			}

			// NOTE: Integer values are loaded directly in the field component using x-init

			log("INFO", "Field state loaded");
		},

		/**
		 * Initialize the field manager component
		 *
		 * Parses the JSON data and builds the form,
		 * and sets the values of the match number and match type fields from the URL data
		 *
		 * Additionally, begin listening for the team number get changed from the team information component
		 */
		init() {
			this.parse_json(JSON.parse(this.field_data));

			this.load_field_state();

			const urlParams = new URLSearchParams(window.location.search);

			const match_number = urlParams.get("match_number", "");
			const match_type = urlParams.get("match_type", "N/A");

			document.querySelector('input[name="match_number"]').value = match_number;
			document.querySelector('select[name="match_type"]').value =
				decodeURIComponent(match_type);

			this.send_match_number();
			this.send_match_type();

			window.addEventListener("set_team_number", (event) => {
				event.stopImmediatePropagation();
				const { team_number } = event.detail;

				document.querySelector('input[name="team_number"]').value = team_number;
			});
		},
	}));
});
