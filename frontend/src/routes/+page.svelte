<script lang="ts">
	import Welcome from "$lib/components/index/Welcome.svelte";
	import Authentication from "$lib/components/index/Authentication.svelte";
	import Header from "$lib/components/index/Header.svelte";
	import Year from "$lib/components/index/Year.svelte";
	import Events from "$lib/components/index/Events.svelte";
	

	let page = $state("events"); // welcome, auth, year, events, action

	let user = $state({
		username: "",
		team_number: 0,
		uuid: ""
	});
	let year = $state(2025);

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
</script>

<div class="flex flex-col justify-center items-center h-screen gap-4">
	{#if page !== "welcome"}
		<Header handleNavigate={handleNavigate} page={page} user={user} year={year}/>
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
		<Events handleNavigate={handleNavigate} year={year}/>

	{/if}
</div>