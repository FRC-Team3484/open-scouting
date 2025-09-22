<script type="ts">
	import icon_rounded from "$lib/assets/icon_rounded.png"
	import Button from "$lib/components/ui/button/button.svelte";
	import * as Card from "$lib/components/ui/card/index.js";

	import { GithubLogo, Bug, Rocket, ArrowRight } from "phosphor-svelte";

	let page = "welcome"; // welcome, auth, year, event, action
</script>

<div class="flex justify-center items-center h-screen">
	{#if page === "welcome"}
		<!-- 0 - Welcome -->
		<div class="flex flex-col gap-4 items-center">
			<div class="flex flex-row gap-4 items-center">
				<img src={icon_rounded} alt="Logo" class="w-24 h-24" />
				<p class="text-4xl font-bold font-mono">Open Scouting</p>
			</div>

			<p class="text-md text-center">An open source application for easier scouting at FIRST robotics competitions</p>

			<div class="flex flex-row gap-4 items-center">
				<Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting"><GithubLogo weight="bold" /> Source Code</Button>
				<Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting/issues"><Bug weight="bold" /> Issues</Button>
				<Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting/releases"><Rocket weight="bold" /> Releases</Button>
			</div>

			<Button onclick={() => page = "auth"}><ArrowRight weight="bold" /> Get Started</Button>
		</div>
	{:else if page === "auth"}
		<Card.Root class="min-w-64">
			<Card.CardHeader>
				<Card.CardTitle>Sign In</Card.CardTitle>
			</Card.CardHeader>
		</Card.Root>
	{/if}
</div>