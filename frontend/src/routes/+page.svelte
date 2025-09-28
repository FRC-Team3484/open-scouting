<script lang="ts">
	import Welcome from "$lib/components/index/Welcome.svelte";
	import Authentication from "$lib/components/index/Authentication.svelte";
	import Header from "$lib/components/index/Header.svelte";

	let page = $state("auth"); // welcome, auth, year, events, action

	let user = $state({
		username: "",
		team_number: 0,
		uuid: ""
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
</script>

<div class="flex flex-col justify-center items-center h-screen gap-4">
	{#if page === "welcome"}
		<!-- 0 - Welcome -->
		<Welcome handleNavigate={handleNavigate} />
		
	{:else if page === "auth"}
		<!-- 1 - Authentication -->
		<Header handleNavigate={handleNavigate} page={page} user={user}/>
		<Authentication handleNavigate={handleNavigate} setUser={setUser}/>
	{/if}
</div>