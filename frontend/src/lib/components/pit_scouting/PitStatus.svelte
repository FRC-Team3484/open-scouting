<!-- 
@component
The pit status card on the pit scouting page

Shows every loaded pit, and how completed each one is. Clicking on a team number jumps to that team's location in the list.ArrowDown
Also shows the number of loaded pits, and a key to the status icons.
-->
<script lang="ts">
	import { ArrowDownIcon, CheckCircleIcon, DotsThreeCircleIcon, RewindCircleIcon, XCircleIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";
	import Button from "../ui/button/button.svelte";

	import type { PitScoutingData, SeasonPitScoutingQuestion } from "$lib/utils/db";


    interface Props {
        pits: PitScoutingData[];
        pit_questions: SeasonPitScoutingQuestion[];
    }
    let { pits, pit_questions }: Props = $props();

    let pitStatus: { team_number: number, status: "done" | "incomplete" | "none"}[] = $derived.by(() => {
        if (!pits || !pit_questions?.length) return [];

        return pits.map(pit => {
            const answeredCount = pit_questions.filter(q => q.required).filter(q =>
                pit.answers?.some(a => a.field_uuid === q.uuid)
            ).length;

            const answeredOptionalCount = pit_questions.filter(q => !q.required).filter(q =>
                pit.answers?.some(a => a.field_uuid === q.uuid)
            ).length;

            let status: "done" | "incomplete" | "none" = "none";

            if (answeredCount === pit_questions.filter(q => q.required).length) {
                status = "done";
            } else if (answeredCount > 0) {
                status = "incomplete";
            } else if (answeredOptionalCount > 0) {
                status = "incomplete";
            }

            return {
                team_number: pit.team_number,
                status
            };
        });
    });

    /**
     * Scroll to the team with the given team number, or the add pit section
     * 
     * @param team_number The team number to scroll to, or "addPit"
     */
    function scrollToTeam(team_number: number | "addPit") {
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
                            <CheckCircleIcon weight="bold" />
                            <p>{pit.team_number}</p>
                        </Button>
                    {:else if pit.status === "incomplete"}
                        <Button variant="ghost" size="sm" class="text-orange-400" onclick={() => scrollToTeam(pit.team_number)}>
                            <DotsThreeCircleIcon weight="bold" />
                            <p>{pit.team_number}</p>
                        </Button>
                    {:else}
                        <Button variant="ghost" size="sm" class="text-red-400" onclick={() => scrollToTeam(pit.team_number)}>
                            <XCircleIcon weight="bold" />
                            <p>{pit.team_number}</p>
                        </Button>
                    {/if}
                {/each}
            </div>

            <Button variant="outline" onclick={() => scrollToTeam("addPit")}><ArrowDownIcon weight="bold" /> Add Missing Pit</Button>
            
            <p>Loaded {pitStatus.length} pits - {pitStatus.filter(pit => pit.status === "done").length}/{pitStatus.length} ({Math.round(pitStatus.filter(pit => pit.status === "done").length / pitStatus.length * 100)}%) completed</p>
            <div class="flex flex-row gap-0.5 flex-wrap text-sm text-muted-foreground items-center">
                <CheckCircleIcon weight="bold" />
                <p class="mr-1">All answered</p>
                <DotsThreeCircleIcon weight="bold" />
                <p class="mr-1">Some answered</p>
                <XCircleIcon weight="bold" />
                <p class="mr-1">No answers</p>
            </div>
        </div>
    </Card.Content>
</Card.Root>

