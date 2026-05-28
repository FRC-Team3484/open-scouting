<!-- 
@component
Welcome component for the index page

Shows the LiveEvents widget, the logo, a description, and some useful buttons
-->
<script lang="ts">
    import { GithubLogoIcon, BugIcon, ArrowRightIcon, DiscordLogoIcon, DatabaseIcon, CalendarIcon } from "phosphor-svelte";

	import Separator from "../ui/separator/separator.svelte";
	import Button from "../ui/button/button.svelte";

    import Logo from "../generic/Logo.svelte";
	import LiveEvents from "./LiveEvents.svelte";
</script>

<div class="flex flex-col gap-4 items-center mb-8">
    <LiveEvents />
    
    <Logo />
    
    <p class="text-md text-center mb-4">An open source application for easier scouting at FIRST robotics competitions</p>
    
    <div class="flex flex-row gap-2 items-center flex-wrap justify-center">
        <Button variant="outline" href="https://discord.gg/M3wESZUP35"><DiscordLogoIcon weight="bold" /> Discord</Button>
        <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting"><GithubLogoIcon weight="bold" /> Source Code</Button>
        <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting/issues"><BugIcon weight="bold" /> Issues</Button>
    </div>
    
    <Separator orientation="horizontal" />

    <Button href="/start"><ArrowRightIcon weight="bold" /> Get Started</Button>
    
    <div class="flex flex-row gap-2 items-center flex-wrap justify-center">
        <Button href="/data" variant="outline"><DatabaseIcon weight="bold" /> Match Scouting Data</Button>
        <Button href="/events" variant="outline"><CalendarIcon weight="bold" /> Events</Button>
    </div>

</div>