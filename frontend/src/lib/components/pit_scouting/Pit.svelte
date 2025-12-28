<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { CaretDown, CaretUp, CheckCircle, DotsThreeCircle, XCircle } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import { slide } from "svelte/transition";
	import TextQuestion from "../generic/pit_questions/main/TextQuestion.svelte";
	import NumberQuestion from "../generic/pit_questions/main/NumberQuestion.svelte";
	import BooleanQuestion from "../generic/pit_questions/main/BooleanQuestion.svelte";
	import ChoiceQuestion from "../generic/pit_questions/main/ChoiceQuestion.svelte";

    let { pit, pit_questions, user, show_avatar = false } = $props();

    let pitCompletion = $derived.by(() => {
        if (!pit || !pit_questions?.length) {
            return {
                answered: 0,
                total: pit_questions?.length ?? 0,
                status: "none" as "done" | "incomplete" | "none"
            };
        }

        const answered = pit_questions.filter(q =>
            pit.answers?.some(a => a.field_uuid === q.uuid)
        ).length;

        let status: "done" | "incomplete" | "none" = "none";

        if (answered === pit_questions.length) {
            status = "done";
        } else if (answered > 0) {
            status = "incomplete";
        }

        return {
            answered,
            total: pit_questions.length,
            status
        };
    });

    let expanded = $state(false);
    let avatar_loaded = $state(true);
</script>

<Card.Root class="w-auto md:min-w-128" data-teamNumber={pit.team_number}>
    <Card.Content>
        <div class="flex flex-col gap-4">
            <div class="flex flex-row gap-2 items-center justify-between">
                <div class="flex flex-row gap-2 items-center flex-wrap">
                    {#if show_avatar && avatar_loaded}
                        <img src={`https://www.thebluealliance.com/avatar/2026/frc${pit.team_number}.png`} class="w-10 h-10 aspect-square rounded-md bg-accent p-1" onerror={() => avatar_loaded = false}>
                    {/if}

                    {#if pitCompletion.status === "done"}
                        <div class="flex flex-row gap-0.5 items-center text-green-300">
                            <CheckCircle weight="bold" /> 
                            <p>{pitCompletion.answered}/{pitCompletion.total}</p>
                        </div>
                    {:else if pitCompletion.status === "incomplete"}
                        <div class="flex flex-row gap-0.5 items-center text-orange-400">
                            <DotsThreeCircle weight="bold" /> 
                            <p>{pitCompletion.answered}/{pitCompletion.total}</p>
                        </div>
                    {:else}
                        <div class="flex flex-row gap-0.5 items-center text-red-400">
                            <XCircle weight="bold" /> 
                            <p>{pitCompletion.answered}/{pitCompletion.total}</p>
                        </div>
                    {/if}
                    
                    <p class="font-bold">{pit.team_number}</p>
                    <p class="text-sm text-muted-foreground">{pit.nickname}</p>
                </div>

                <Button size="icon" variant="ghost" onclick={() => expanded = !expanded}>
                    {#if expanded}
                        <CaretDown weight="bold" />
                    {:else}
                        <CaretUp weight="bold" />
                    {/if}
                </Button>
            </div>

            {#if expanded}
                <div class="flex flex-col gap-2 items-start" transition:slide>
                    {#each pit_questions as question}
                        {#if question.field_type === "text"}
                            <TextQuestion pit={pit} question={question} answers={pit.answers.filter((answer) => answer.field_uuid === question.uuid)} user={user} />
                        {:else if question.field_type === "number"}
                            <NumberQuestion pit={pit} question={question} answers={pit.answers.filter((answer) => answer.field_uuid === question.uuid)} user={user} />
                        {:else if question.field_type === "boolean"}
                            <BooleanQuestion pit={pit} question={question} answers={pit.answers.filter((answer) => answer.field_uuid === question.uuid)} user={user} />
                        {:else if question.field_type === "choice"}
                            <ChoiceQuestion pit={pit} question={question} answers={pit.answers.filter((answer) => answer.field_uuid === question.uuid)} user={user} />
                        {/if}
                    {/each}
                </div>
            {/if}
        </div>
    </Card.Content>
</Card.Root>