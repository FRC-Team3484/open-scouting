<script lang="ts">
	import Button from "../ui/button/button.svelte";
	import Logo from "./Logo.svelte";
	import { ArrowRight, List } from "phosphor-svelte";
	import Separator from "../ui/separator/separator.svelte";
	import User from "./User.svelte";
	import ExperimentalWarning from "./ExperimentalWarning.svelte";
    import * as Sheet from "$lib/components/ui/sheet/index.js";
	import { page } from "$app/state";
	import { fade, slide } from "svelte/transition";
	import { matchScoutingMatchNumber, matchScoutingTeamNumber, matchScoutingTeamPosition } from "$lib/stores/match_scouting";
	import Badge from "../ui/badge/badge.svelte";
    import * as Card from "$lib/components/ui/card/index.js"
</script>

{#snippet matchScoutingInfo()}
    {#if page.url.pathname == "/match_scouting" && ($matchScoutingTeamPosition || $matchScoutingTeamNumber || $matchScoutingMatchNumber)}
            <div transition:slide={{ axis: "x" }}>
                <Card.Root class="p-1 md:p-2">
                    <Card.Content class="flex flex-row gap-2 items-center p-1 md:p-2 whitespace-nowrap">
                        {#if $matchScoutingTeamPosition}
                            <div transition:slide={{ axis: "x" }}>
                                <Badge class={`transition-colors font-bold ${$matchScoutingTeamPosition.includes("blue") ? "bg-blue-500" : "bg-red-500"}`}>
                                    {$matchScoutingTeamPosition.replace("blue", "Blue ").replace("red", "Red ")}
                                </Badge>
                            </div>
                        {/if}
                        {#if $matchScoutingTeamNumber}
                            <div transition:slide={{ axis: "x" }}>
                                <p>Team <span class="font-bold">{$matchScoutingTeamNumber}</span></p>
                            </div>
                        {/if}
                        {#if $matchScoutingMatchNumber}
                            <div transition:slide={{ axis: "x" }}>
                                <p>Match <span class="font-bold">{$matchScoutingMatchNumber}</span></p>
                            </div>
                        {/if}
                    </Card.Content>
                </Card.Root>
            </div>
        {/if}
{/snippet}

<div class="hidden md:flex fixed top-0 left-0 right-0 w-full h-24 flex-row justify-between items-center border-1 bg-card/50 border-accent rounded-b-lg backdrop-blur-lg p-2 z-10">
    <div class="flex flex-row gap-4 items-center">
        <Logo text={true} style="tiny" href="/" />
        <ExperimentalWarning />

        <Button variant="outline" href="/" class="ml-4">Home</Button>
        <Button variant="outline" href="/data">View Data</Button>
        <Button variant="outline" href="/events">Events</Button>

        {@render matchScoutingInfo()}
    </div>

    <div class="flex flex-row gap-4 items-center">
    </div>

    <div class="flex flex-row gap-4 items-center">
        {#if page.url.pathname == "/"}
            <div transition:slide={{ axis: "x" }}>
                <div transition:fade><Button variant="default" href="/start"><ArrowRight weight="bold" /> Get Started</Button></div>
            </div>
        {/if}

        <User show_text={false} />
    </div>
</div>

<div class="flex md:hidden fixed top-0 left-0 right-0 w-full h-16 flex-row justify-between items-center border-1 bg-background/50 border-accent rounded-b-lg backdrop-blur-lg p-2 z-10">
    <div class="flex flex-row gap-2 items-center">
        <Sheet.Root>
            <Sheet.Trigger class="p-2 text-md border-1 border-border rounded-md bg-input/30">
                <List weight="bold"/>
            </Sheet.Trigger>
            <Sheet.Content class="flex flex-col gap-4 p-4 justify-between" side="left">
                <div class="flex flex-col gap-4">
                    <div class="flex flex-row gap-4 items-center justify-between">
                        <Logo text={false} style="tiny" href="/" />
                    </div>
                    <div class="flex flex-row gap-4 items-center">
                        <User show_text={true} />
                    </div>
                    <Separator orientation="horizontal" />
                    <Sheet.Close><Button variant="outline" href="/" class="w-full">Home</Button></Sheet.Close>
                    <Sheet.Close><Button variant="outline" href="/data" class="w-full">View Data</Button></Sheet.Close>
                    <Sheet.Close><Button variant="outline" href="/events" class="w-full">Events</Button></Sheet.Close>
                </div>

                <ExperimentalWarning/>
            </Sheet.Content>
        </Sheet.Root>
        <ExperimentalWarning size="sm" />

        {@render matchScoutingInfo()}
    </div>

    {#if page.url.pathname == "/"}
        <div transition:slide={{ axis: "x" }}>
            <div transition:fade><Button variant="default" href="/start"><ArrowRight weight="bold" /> Get Started</Button></div>
        </div>
    {/if}
</div>