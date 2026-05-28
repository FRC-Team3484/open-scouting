<!-- 
@component
Represents a single pit on the pit scouting page

Renders questions for this pit, gets how complete it is, and allows for expanding each pit.

TODO: Add a proper interface for user
-->
<script lang="ts">
	import { slide } from "svelte/transition";
	import { CaretDownIcon, CaretUpIcon, CheckCircleIcon, DotsThreeCircleIcon, XCircleIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";
	import Button from "../ui/button/button.svelte";

	import type { PitScoutingData, SeasonPitScoutingQuestion } from "$lib/utils/db";
	import TextQuestion from "../generic/pit_questions/main/TextQuestion.svelte";
	import NumberQuestion from "../generic/pit_questions/main/NumberQuestion.svelte";
	import BooleanQuestion from "../generic/pit_questions/main/BooleanQuestion.svelte";
	import ChoiceQuestion from "../generic/pit_questions/main/ChoiceQuestion.svelte";
	import ImageQuestion from "../generic/pit_questions/main/ImageQuestion.svelte";


    interface Props {
        pit: PitScoutingData
        pit_questions: SeasonPitScoutingQuestion[]
        user: unknown
        show_avatar?: boolean
    }
    let { pit, pit_questions, user, show_avatar = false }: Props = $props();

    let pitCompletion: {answered: number, total: number, status: "done" | "incomplete" | "none"} = $derived.by(() => {
        if (!pit || !pit_questions?.length) {
            return {
                answered: 0,
                total: pit_questions?.length ?? 0,
                status: "none" as "done" | "incomplete" | "none"
            };
        }

        const answered = pit_questions.filter(q =>
            pit.answers?.some(a => a.field_uuid === q.uuid && q.required === true)
        ).length;
        const answeredOptional = pit_questions.filter(q =>
            pit.answers?.some(a => a.field_uuid === q.uuid && q.required === false)
        ).length;

        let status: "done" | "incomplete" | "none" = "none";

        if (answered === pit_questions.filter(q => q.required).length) {
            status = "done";
        } else if (answered > 0) {
            status = "incomplete";
        } else if (answeredOptional > 0) {
            status = "incomplete";
        }

        return {
            answered: answered + answeredOptional,
            total: pit_questions.filter(q => q.required).length,
            status
        };
    });

    let expanded: boolean = $state(false);
    let avatar_loaded: boolean = $state(true);
</script>

<Card.Root class="w-full md:w-auto min-w-64 md:min-w-lg" data-teamNumber={pit.team_number}>
    <Card.Content>
        <div class="flex flex-col gap-2 md:gap-4">
            <div class="flex flex-row gap-2 items-center justify-between">
                <div class="flex flex-row gap-2 items-center flex-wrap cursor-pointer" onclick={() => expanded = !expanded} tabindex="0" onkeydown={(e) => { if (e.key === "Enter") { expanded = !expanded; }}} role="button">
                    {#if show_avatar && avatar_loaded}
                        <img src={`https://www.thebluealliance.com/avatar/2026/frc${pit.team_number}.png`} class="w-10 h-10 aspect-square rounded-md bg-accent p-1" onerror={() => avatar_loaded = false} alt={`Avatar for team ${pit.team_number}`}>
                    {/if}

                    {#if pitCompletion.status === "done"}
                        <div class="flex flex-row gap-0.5 items-center text-green-300">
                            <CheckCircleIcon weight="bold" /> 
                            <p>{pitCompletion.answered}/{pitCompletion.total}</p>
                        </div>
                    {:else if pitCompletion.status === "incomplete"}
                        <div class="flex flex-row gap-0.5 items-center text-orange-400">
                            <DotsThreeCircleIcon weight="bold" /> 
                            <p>{pitCompletion.answered}/{pitCompletion.total}</p>
                        </div>
                    {:else}
                        <div class="flex flex-row gap-0.5 items-center text-red-400">
                            <XCircleIcon weight="bold" /> 
                            <p>{pitCompletion.answered}/{pitCompletion.total}</p>
                        </div>
                    {/if}
                    
                    <p class="font-bold">{pit.team_number}</p>
                    <p class="text-sm text-muted-foreground">{pit.nickname}</p>
                </div>

                <Button size="icon" variant="ghost" onclick={() => expanded = !expanded}>
                    {#if expanded}
                        <CaretDownIcon weight="bold" />
                    {:else}
                        <CaretUpIcon weight="bold" />
                    {/if}
                </Button>
            </div>

            {#if expanded}
                <div class="flex flex-col gap-1 md:gap-2 items-start" transition:slide>
                    {#each pit_questions as question}
                        {#if question.field_type === "text"}
                            <TextQuestion pit={pit} question={question} answers={pit.answers.filter((answer) => answer.field_uuid === question.uuid)} user={user} />
                        {:else if question.field_type === "number"}
                            <NumberQuestion pit={pit} question={question} answers={pit.answers.filter((answer) => answer.field_uuid === question.uuid)} user={user} />
                        {:else if question.field_type === "boolean"}
                            <BooleanQuestion pit={pit} question={question} answers={pit.answers.filter((answer) => answer.field_uuid === question.uuid)} user={user} />
                        {:else if question.field_type === "choice"}
                            <ChoiceQuestion pit={pit} question={question} answers={pit.answers.filter((answer) => answer.field_uuid === question.uuid)} user={user} />
                        {:else if question.field_type === "image"}
                            <ImageQuestion pit={pit} question={question} answers={pit.answers.filter((answer) => answer.field_uuid === question.uuid)} user={user} />
                        {/if}
                    {/each}
                </div>
            {/if}
        </div>
    </Card.Content>
</Card.Root>