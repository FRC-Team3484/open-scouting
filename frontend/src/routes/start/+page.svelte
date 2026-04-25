<script lang="ts">
	import Authentication from "$lib/components/index/Authentication.svelte";
	import Header from "$lib/components/index/Header.svelte";
	import Year from "$lib/components/index/Year.svelte";
	import Events from "$lib/components/index/Events.svelte";
	import Action from "$lib/components/index/Action.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import { onMount, tick } from "svelte";
	import { pushState, replaceState } from "$app/navigation";
	import { toast } from "svelte-sonner";
	import Link from "$lib/components/index/Link.svelte";
	
	// /start?year=2026&event_code=alhu&event_name=Rocket City Regional&action=match_scouting

	let page = $state("auth"); // auth, year, events, action, link

	let user = $state({
		username: "",
		team_number: 0,
		uuid: ""
	});
	let year = $state(0);
	let selected_event = $state({
		event_code: "",
		year: 0,
		name: ""
	});
	let action = $state(""); // match_scouting, pit_scouting, data

	/**
	 * Sets the local user information. Should be used from another component
	 * 
	 * @param username The username to authenticate as
	 * @param team_number The team number for the user that's authenticating
	 * @param uuid The uuid for the user that's authenticating
	 */
	function setUser(username: string, team_number: number, uuid: string): void {
		user = {
			username: username,
			team_number: team_number,
			uuid: uuid
		}
	};

	/**
	 * Sets the year to scout for. Should be used from another component
	 * 
	 * @param newYear The year to scout for
	 */
	function setYear(newYear: number): void {
		year = newYear;
	}
	
	/**
	 * Set the event to scout for. Should be used from another component
	 * 
	 * @param event_code The event code for the event
	 * @param year The year of the event
	 * @param name The name of the event
	 */
	function setEvent(event_code: string, year: number, name: string): void {
		selected_event = {
			event_code: event_code,
			year: year,
			name: name
		}
	}
	
	/**
	 * Resets the states and brings the user back to the auth page
	 */
	function startOver(): void {
		page = "auth";
		user = {
			username: "",
			team_number: 0,
			uuid: ""
		}
		year = 0;
		selected_event = {
			event_code: "",
			year: 0,
			name: ""
		}
		action = "";
	}
	
	/**
	 * Decides the correct page to send the user to, then updates the browser history state accordingly
	 * 
	 * @param nextPage The next page to go to
	 */
	function handleNavigate(nextPage: string): void {
		const resolved = resolvePage(nextPage);

		console.log(resolved, nextPage);

		if (resolved == "action" && nextPage === "year") {
			toast.success("Event selected from URL", { duration: 5000 });
		} else if (resolved == "link" && nextPage === "year") {
			toast.success("Event and action selected from URL", { duration: 5000 });
		}

		page = resolved;
		updateUrl(true);
	}

	/**
	 * Resolves the page based on the target page
	 * 
	 * If the user isn't authenticated, go to the auth page
	 * If the year has been set, go to the event page
	 * If going to the event page, check and see if an action is provided. If so, go to the link page, otherwise go to the action page
	 * 
	 * @param target The target page to go to next
	 * @returns The target page to actually go to
	 */
	function resolvePage(target: string): string {
		if (!(user.uuid && user.uuid.length > 0)) {
			return "auth";
		}

		if (target === "year" && year !== 0) {
			return resolvePage("events");
		}

		if (target === "events" && selected_event.event_code !== "") {
			const validActions = new Set(["match_scouting", "pit_scouting", "data"]);

			if (validActions.has(action)) {
				return "link";
			}

			return "action";
		}

		return target;
	}

	/**
	 * Updates the browser history with the current page state
	 */
	function syncPageWithState() {
		const resolved = resolvePage(page);

		if (resolved !== page) {
			page = resolved;

			updateUrl(false);
		}
	}

	/**
	 * Loads the URL parameters and sets the initial page state
	 */
	function loadUrlParams() {
		const url = new URL(window.location.href);

		page = url.searchParams.get("page") ?? "auth";

		year = url.searchParams.has("year")
			? parseInt(url.searchParams.get("year"))
			: 0;

		if (
			url.searchParams.has("event_code") &&
			url.searchParams.has("year") &&
			url.searchParams.has("event_name")
		) {
			selected_event = {
				event_code: url.searchParams.get("event_code"),
				year: parseInt(url.searchParams.get("year")),
				name: url.searchParams.get("event_name")
			};
		} else {
			selected_event = { event_code: "", year: 0, name: "" };
		}

		action = url.searchParams.get("action") ?? "";
	}

	/**
	 * Update the URL params with the current page, year, and event data
	 * 
	 * @param push If the browser state should be pushed or replaced
	 */
	function updateUrl(push = false) {
		const url = new URL(window.location.href);

		url.searchParams.set("page", page);

		if (year > 0) url.searchParams.set("year", String(year));
		else url.searchParams.delete("year");

		if (selected_event.event_code)
			url.searchParams.set("event_code", selected_event.event_code);
		else url.searchParams.delete("event_code");

		if (selected_event.name)
			url.searchParams.set("event_name", selected_event.name);
		else url.searchParams.delete("event_name");

		if (push) {
			pushState(url, {});
		} else {
			replaceState(url, {});
		}
	}

	onMount(() => {
		tick().then(() => {
			loadUrlParams();
			syncPageWithState();
	
			addEventListener("popstate", () => {
				loadUrlParams();
				syncPageWithState();
			});
		});
	});
</script>

<PageContainer>
    <Header startOver={startOver} page={page} user={user} year={year} event={selected_event}/>
		
	{#if page === "auth"}
		<!-- 1 - Authentication -->
		<Authentication handleNavigate={handleNavigate} setUser={setUser}/>

	{:else if page === "year"}
		<!-- 2 - Year -->
		<Year handleNavigate={handleNavigate} setYear={setYear}/>

	{:else if page === "events"}
		<!-- 3 - Events -->
		<Events handleNavigate={handleNavigate} year={year} setEvent={setEvent}/>

	{:else if page === "action"}
		<!-- 4 - Action -->
		<Action year={year} event={selected_event} user={user}/>

	{:else if page === "link"}
		<!-- Link -->
		<Link year={year} event={selected_event} user={user} action={action} startOver={startOver} />

	{/if}
</PageContainer>