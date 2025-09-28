<script lang="ts">
	import Welcome from "$lib/components/index/Welcome.svelte";
	import Authentication from "$lib/components/index/Authentication.svelte";
	import Header from "$lib/components/index/Header.svelte";
	import Year from "$lib/components/index/Year.svelte";

	let page = $state("year"); // welcome, auth, year, events, action

	let user = $state({
		username: "",
		team_number: 0,
		uuid: ""
	});
	let year = $state(0);

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
		<Year handleNavigate={handleNavigate} setYear={setYear}/>
	{/if}
</div>