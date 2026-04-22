<script lang="ts">
	import Separator from "../ui/separator/separator.svelte";
	import Button from "../ui/button/button.svelte";
    import { GithubLogo, Bug, Rocket, ArrowRight, DiscordLogo, Database } from "phosphor-svelte";

    import Logo from "../generic/Logo.svelte";
	import LiveEvents from "./LiveEvents.svelte";
</script>

<div class="flex flex-col gap-4 items-center">
    <LiveEvents />
    
    <Logo />
    
    <p class="text-md text-center">An open source application for easier scouting at FIRST robotics competitions</p>
    
    <div class="flex flex-row gap-2 items-center flex-wrap justify-center">
        <Button variant="outline" href="https://discord.gg/M3wESZUP35"><DiscordLogo weight="bold" /> Discord</Button>
        <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting"><GithubLogo weight="bold" /> Source Code</Button>
        <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting/issues"><Bug weight="bold" /> Issues</Button>
        <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting/releases"><Rocket weight="bold" /> Releases</Button>
    </div>
    
    <Separator orientation="horizontal" />
    
    <Button href="/start"><ArrowRight weight="bold" /> Get Started</Button>
    <Button href="/data" variant="outline"><Database weight="bold" /> View Data</Button>
</div>