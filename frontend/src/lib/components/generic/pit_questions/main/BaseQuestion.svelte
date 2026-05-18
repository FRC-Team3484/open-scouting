<!--
@component
Base pit scouting question component for the actual pit scouting page

TODO: Create a proper type interface for pit scouting answers from the db
TODO: Change how the reset function works to be more Svelte-like

Props:
    - `question` (`SeasonPitScoutingQuestion`) - Data for the question
    - `answers` (`PitScoutingAnswer[]`) - Answers for this question
    - `reset` (`() => void`) - Internal, bindable function, used by children questions to reset their mode
    - `children` (`Snippet`) - Child components to render
-->
<script lang="ts">
	import { slide } from "svelte/transition";
	import { CalendarIcon, EyeIcon, PlusCircleIcon, UserIcon, XIcon } from "phosphor-svelte";

	import Badge from "$lib/components/ui/badge/badge.svelte";
    import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import type { Snippet } from "svelte";
	import type { PitScoutingAnswer, SeasonPitScoutingQuestion } from "$lib/utils/db";


    interface Props {
        question: SeasonPitScoutingQuestion
        answers: PitScoutingAnswer[]
        reset: () => void
        children: Snippet
    }
    let { question, answers, reset = $bindable(), children }: Props = $props();

    type Mode = "none" | "view" | "add";

    let mode: Mode = $state("none");

    reset = () => {
        mode = "none";
    }
</script>

<Card.Root class="w-full items-start px-4">
    <div class="flex flex-col gap-2 justify-between flex-wrap">
        <div class="flex flex-col md:flex-row gap-2 flex-wrap items-start">
            <p class="font-bold text-left">{question.name}</p>
            {#if question.required}
                <span class="text-red-500">*</span>
            {/if}
            <Badge variant="outline">{answers.length} {answers.length == 1 ? "answer" : "answers"}</Badge>
        </div>

        {#if question.description}
            <p class="text-sm text-muted-foreground text-left mb-2">{question.description}</p>
        {/if}

        {#if mode == "none"}
            <div class="flex flex-row gap-2 flex-wrap">
                <Button size="sm" onclick={() => mode = "add"}><PlusCircleIcon weight="bold" /> Add Answer</Button>
                <Button size="sm" variant="outline" onclick={() => mode = "view"}><EyeIcon weight="bold" /> View Answers</Button>
            </div>
        {:else if mode == "add" || mode == "view"}
            <div class="flex flex-row gap-2 flex-wrap">
                <Button size="sm" variant="outline" onclick={() => mode = "none"}><XIcon weight="bold" /> Close</Button>
            </div>
        {/if}
    </div>

    {#if mode == "add"}
        <Card.Content>
            <div class="flex flex-col gap-2 items-start w-full" transition:slide>
                {@render children()}
            </div>
        </Card.Content>

    {:else if mode == "view"}
        <Card.Content>
            <div class="flex flex-row gap-2 w-full" transition:slide>
                {#if answers.length == 0}
                    <p class="text-muted-foreground">No answers yet</p>
                {:else}
                    <div class="flex flex-col gap-2">
                        {#each answers as answer}
                            <div class="flex flex-row items-center flex-wrap text-left">
                                <p class="wrap-anywhere">{answer.value}</p>
                                <UserIcon weight="bold" class="text-muted-foreground ml-2 mr-1"/>
                                <p class="text-muted-foreground text-sm">{answer.username}</p>
                                <CalendarIcon weight="bold" class="text-muted-foreground ml-2 mr-1"/>
                                <p class="text-muted-foreground text-sm">{new Intl.DateTimeFormat('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }).format(new Date(answer.created_at))}</p>
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>
        </Card.Content>
    {/if}
</Card.Root>