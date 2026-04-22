<script lang="ts">
	import Welcome from "$lib/components/index/Welcome.svelte";
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
	import { navigating } from "$app/state";
	
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
	let lastPage = $state(page);

	function handleNavigate(nextPage: string): void {
		if (nextPage === "year" && year !== 0) {
			handleNavigate("events");
		} else if (nextPage === "events" && selected_event.event_code !== "") {
			if (action === "match_scouting" || action === "pit_scouting" || action === "data") {
				handleNavigate("link");
			} else {
				handleNavigate("action");
				toast.success("Event selected from URL", { duration: 5000 });
			}
		} else {
			page = nextPage;
		}
	};

	function setUser(username: string, team_number: number, uuid: string): void {
		user = {
			username: username,
			team_number: team_number,
			uuid: uuid
		}
	};

	function setYear(newYear: number): void {
		year = newYear;
	}

	function setEvent(event_code: string, year: number, name: string): void {
		selected_event = {
			event_code: event_code,
			year: year,
			name: name
		}
	}

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

	function loadUrlParams() {
		const url = new URL(window.location.href);

		if (url.searchParams.has("page")) {
			page = url.searchParams.get("page");
		}

		if (url.searchParams.has("year")) {
			setYear(parseInt(url.searchParams.get("year")));
		}

		if (url.searchParams.has("event_code") && url.searchParams.has("year") && url.searchParams.has("event_name")) {
			setEvent(url.searchParams.get("event_code"), parseInt(url.searchParams.get("year")), url.searchParams.get("event_name"));
		}

		if (url.searchParams.has("action")) {
			action = url.searchParams.get("action");
		}
	}

	function setUrlParams(push = false) {
		const url = new URL(window.location.href);

		url.searchParams.set("page", page);

		if (year > 0) {
			url.searchParams.set("year", String(year));
		} else {
			url.searchParams.delete("year");
		}

		if (selected_event.event_code.length > 0) {
			url.searchParams.set("event_code", selected_event.event_code);
		} else {
			url.searchParams.delete("event_code");
		}

		if (selected_event.name.length > 0) {
			url.searchParams.set("event_name", selected_event.name);
		} else {
			url.searchParams.delete("event_name");
		}

		tick().then(() => {
			if (push) {
				pushState(url, {});
			} else {
				replaceState(url, {});
			}
		});
	}

	function updatePageFromUrl() {
		const url = new URL(window.location.href);

		if (url.searchParams.has("page") && url.searchParams.get("page") != page) {
			page = url.searchParams.get("page");

			console.log("set page to", page);
		}
	}

	$effect(() => {
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

		// 🔑 CRITICAL: do nothing if URL is already identical
		if (url.toString() === window.location.href) return;

		if (page !== lastPage) {
			pushState(url, {});
			lastPage = page;
		} else {
			replaceState(url, {});
		}
	});

	onMount(async () => {
		loadUrlParams();

		addEventListener("popstate", () => {
			loadUrlParams();
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