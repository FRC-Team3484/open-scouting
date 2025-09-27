<script lang="ts">
    import * as Card from "$lib/components/ui/card";
	import { ArrowDown, ArrowLeft, ArrowUp } from "phosphor-svelte";
	import Logo from "../generic/Logo.svelte";
	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import Progress from "../ui/progress/progress.svelte";

    let details = false;
    let progress = 1;

    export let handleNavigate: (next: string) => void;
</script>

<Card.Card class="w-full">
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
                    <p class="text-md">Step <strong>1 of 4</strong></p>
                    <Progress value={progress} max={4} />
                    <Button onclick={() => details = !details} class="max-w-fit" variant="ghost">
                        <div class="flex items-center">
                            <ArrowDown weight="bold" class="transform transition-transform duration-200 ease-in-out {details ? 'rotate-180' : 'rotate-0'}" />
                        </div>
                        Details
                    </Button>
                </div>
            </div>

            {#if details}
                <div class="flex flex-col gap-2">
                    <div class="flex flex-row gap-4 items-center">
                        <p class="text-lg text-muted-foreground">Details</p>
                        <Separator orientation="horizontal" class="!w-3/4"/>
                    </div>
                    <p>User: </p>
                    <p>Year: </p>
                    <p>Event: </p>
                </div>
            {/if}
        </div>
    </Card.Content>
</Card.Card>