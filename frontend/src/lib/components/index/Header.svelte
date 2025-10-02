<script lang="ts">
    import { fade, slide } from "svelte/transition";

    import * as Card from "$lib/components/ui/card";
	import { ArrowDown, ArrowLeft, ArrowUp } from "phosphor-svelte";
	import Logo from "../generic/Logo.svelte";
	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import Progress from "../ui/progress/progress.svelte";

    let details = false;
    let progress = 1;

    export let handleNavigate: (nextPage: string) => void;
    export let page: string;
    export let user: any;
    export let year: number;
    export let event: any;

    $: {
        switch (page) {
            case "welcome":
                progress = 0;
                break;
            case "auth":
                progress = 1;
                break;
            case "year":
                progress = 2;
                break;
            case "events":
                progress = 3;
                break;
            case "action":
                progress = 4;
                break;
            default:
                progress = 1;
        }
    }
</script>

<Card.Card class="w-auto">
    <Card.Content>
        <div class="flex flex-col gap-2">
            <div class="flex flex-row gap-4 items-center">
                <Logo text={false} style="small" />

                <div class="flex flex-col gap-2">
                    <p class="text-lg font-bold font-mono">Open Scouting</p>
                    <Button onclick={() => handleNavigate("welcome")} class="max-w-fit" variant="ghost"><ArrowLeft weight="bold" /> Start Over</Button>
                </div>

                <Separator orientation="vertical" class="min-h-16" />

                <div class="flex flex-col gap-2">
                    <p class="text-md">Step <strong>{progress} of 5</strong></p>
                    <Progress value={progress} max={5} />
                    <Button onclick={() => details = !details} class="max-w-fit" variant="ghost">
                        <div class="flex items-center">
                            <ArrowDown weight="bold" class="transform transition-transform duration-200 ease-in-out {details ? 'rotate-180' : 'rotate-0'}" />
                        </div>
                        Details
                    </Button>
                </div>
            </div>

            {#if details}
                <div class="flex flex-col gap-2" transition:slide>
                    <div class="flex flex-row gap-4 items-center">
                        <p class="text-lg text-muted-foreground">Details</p>
                        <Separator orientation="horizontal" class="!w-3/4"/>
                    </div>
                    <div class="flex flex-row gap-2">
                        <p>User: </p>
                        <p class="font-bold">{user.username}</p>
                        <p class="font-mono">{user.team_number}</p>
                        {#if user.uuid}
                            <p class="text-sm text-muted-foreground">Authenticated</p>
                        {:else}
                            <p class="text-sm text-muted-foreground">Not Authenticated</p>
                        {/if}
                    </div>
                    <p>Year: {year}</p>
                    <div class="flex flex-row gap-2">
                        <p>Event: </p>
                        <p class="font-bold">{event.name}</p>
                        <p class="font-mono">{event.event_code}</p>
                    </div>
                </div>
            {/if}
        </div>
    </Card.Content>
</Card.Card>