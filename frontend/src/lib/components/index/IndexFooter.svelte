<!-- 
@component
A footer for the index page, with some links to important places and credit information
-->
<script lang="ts">
	import { ArrowRightIcon, BugIcon, CalendarIcon, DatabaseIcon, DiscordLogoIcon, GithubLogoIcon, RocketIcon } from "phosphor-svelte";

	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";

    import Logo from "../generic/Logo.svelte";
</script>

<div class="flex flex-col gap-2 w-full mt-16 mb-8 text-left">
    <Separator orientation="horizontal" class="my-4" />

    <Logo style="tiny" href="/" />
    <p class="mb-4">An open source application for easier <br>scouting at FIRST robotics competitions</p>

    <div class="flex flex-row gap-2 flex-wrap mb-4">
        <Button href="/start"  class="w-fit"><ArrowRightIcon weight="bold" /> Get Started</Button>
        <Button href="/data" variant="outline" class="w-fit"><DatabaseIcon weight="bold" /> Match Scouting Data</Button>
        <Button href="/events" variant="outline" class="w-fit"><CalendarIcon weight="bold" /> Events</Button>
    </div>

    <Button variant="outline" href="https://discord.gg/M3wESZUP35" size="sm" class="w-fit"><DiscordLogoIcon weight="bold" /> Discord</Button>
    
    <div class="flex flex-row gap-2 flex-wrap mb-4">
        <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting" size="sm" class="w-fit"><GithubLogoIcon weight="bold" /> Source Code</Button>
        <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting/issues" size="sm" class="w-fit"><BugIcon weight="bold" /> Issues</Button>
        <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting/releases" size="sm" class="w-fit"><RocketIcon weight="bold" /> Releases</Button>
    </div>

    <p class="text-muted-foreground">Made by <a class="underline" href="https://github.com/FRC-Team3484/">FRC 3484 Short Circuit</a></p>
    <p class="text-muted-foreground">Powered by <a class="underline" href="https://www.thebluealliance.com/">The Blue Alliance</a></p>
</div>