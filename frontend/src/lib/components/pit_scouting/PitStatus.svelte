<script lang="ts">
	import { onMount } from "svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import Button from "../ui/button/button.svelte";
	import { CheckCircle, DotsThreeCircle, RewindCircle, XCircle } from "phosphor-svelte";

    let { pits, pit_questions } = $props();

    let pitStatus = $derived.by(() => {
        if (!pits || !pit_questions?.length) return [];

        return pits.map(pit => {
            const answeredCount = pit_questions.filter(q =>
                pit.answers?.some(a => a.field_uuid === q.uuid)
            ).length;

            let status: "done" | "incomplete" | "none" = "none";

            if (answeredCount === pit_questions.length) {
                status = "done";
            } else if (answeredCount > 0) {
                status = "incomplete";
            }

            return {
                team_number: pit.team_number,
                status
            };
        });
    });

    function scrollToTeam(team_number: number) {
        const element = document.querySelector(`[data-teamNumber="${team_number}"]`);
        if (element) {
            element.scrollIntoView({ behavior: "smooth" });
        }
    }
</script>

<Card.Root class="w-auto min-w-64">
    <Card.Content>
        <div class="flex flex-col gap-2 items-start">
            <p class="font-bold">Pit Scouting Status</p>
            <p class="text-sm text-muted-foreground">Click on a team number to jump to that team's location in the list</p>

            <div class="flex flex-row gap-1 items-start flex-wrap">
                {#each pitStatus as pit}
                    {#if pit.status === "done"}
                        <Button variant="ghost" size="sm" class="text-green-300" onclick={() => scrollToTeam(pit.team_number)}>
                            <CheckCircle weight="bold" />
                            <p>{pit.team_number}</p>
                        </Button>
                    {:else if pit.status === "incomplete"}
                        <Button variant="ghost" size="sm" class="text-orange-400" onclick={() => scrollToTeam(pit.team_number)}>
                            <DotsThreeCircle weight="bold" />
                            <p>{pit.team_number}</p>
                        </Button>
                    {:else}
                        <Button variant="ghost" size="sm" class="text-red-400" onclick={() => scrollToTeam(pit.team_number)}>
                            <XCircle weight="bold" />
                            <p>{pit.team_number}</p>
                        </Button>
                    {/if}
                {/each}
            </div>
            
            <p>Loaded {pitStatus.length} pits - {pitStatus.filter(pit => pit.status === "done").length}/{pitStatus.length} ({Math.round(pitStatus.filter(pit => pit.status === "done").length / pitStatus.length * 100)}%) completed</p>
            <div class="flex flex-row gap-0.5 flex-wrap text-sm text-muted-foreground items-center">
                <CheckCircle weight="bold" />
                <p class="mr-1">All answered</p>
                <DotsThreeCircle weight="bold" />
                <p class="mr-1">Some answered</p>
                <XCircle weight="bold" />
                <p class="mr-1">No answers</p>
            </div>
        </div>
    </Card.Content>
</Card.Root>

