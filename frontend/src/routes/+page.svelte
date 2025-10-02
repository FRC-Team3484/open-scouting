<script lang="ts">
	import Welcome from "$lib/components/index/Welcome.svelte";
	import Authentication from "$lib/components/index/Authentication.svelte";
	import Header from "$lib/components/index/Header.svelte";
	import Year from "$lib/components/index/Year.svelte";
	import Events from "$lib/components/index/Events.svelte";
	import Action from "$lib/components/index/Action.svelte";
	

	let page = $state("action"); // welcome, auth, year, events, action

	let user = $state({
		username: "",
		team_number: 0,
		uuid: ""
	});
	let year = $state(2025);
	let selected_event = $state({
		event_code: "",
		year: 0,
		name: ""
	});

	function handleNavigate(nextPage: string): void {
		page = nextPage;
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
</script>

<div class="flex flex-col justify-center items-center h-screen gap-4">
	{#if page !== "welcome"}
		<Header handleNavigate={handleNavigate} page={page} user={user} year={year} event={selected_event}/>
	{/if}

	{#if page === "welcome"}
		<!-- 0 - Welcome -->
		<Welcome handleNavigate={handleNavigate} />
		
	{:else if page === "auth"}
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

		<Action />

	{/if}
</div>