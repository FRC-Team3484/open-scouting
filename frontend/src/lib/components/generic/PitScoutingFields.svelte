<script lang="ts">
	import { onMount } from "svelte";
    
    import Separator from "../ui/separator/separator.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { PlusCircle } from "phosphor-svelte";

	import AddPitScoutingQuestionDialog from "./dialogs/AddPitScoutingQuestionDialog.svelte";
	import { addPitScoutingQuestionDialogOpen } from "$lib/stores/dialog";
	import { apiFetch } from "$lib/utils/api";
	import { db } from "$lib/utils/db";
	import TextQuestion from "./pit_questions/admin/TextQuestion.svelte";
	import NumberQuestion from "./pit_questions/admin/NumberQuestion.svelte";
	import BooleanQuestion from "./pit_questions/admin/BooleanQuestion.svelte";
	import ChoiceQuestion from "./pit_questions/admin/ChoiceQuestion.svelte";

    let { season_uuid, year, event_data = {}, editable } = $props();

    let questions = $state([]);

    async function getQuestions() {
        if (editable) {
            questions = await apiFetch(`/pits/fields/${season_uuid}`);
        } else {
            const season = await db.season_data.get(parseInt(year));
            questions = season?.pit_scouting_questions;
        }
    }

    onMount(async () => {
        getQuestions();
    })
</script>

{#if editable}
    <div class="flex flex-col gap-4">
        <Separator orientation="horizontal" />

        <Card.Root class="w-auto min-w-64">
            <Card.Content>
                <Button onclick={() => {addPitScoutingQuestionDialogOpen.set(true);}}><PlusCircle weight="bold" /> Add Question</Button>
            </Card.Content>
        </Card.Root>
    </div>
{/if}

<div class="flex flex-col gap-4 mt-4">
    {#each questions as question (question.uuid)}
        {#if question.field_type !== "undefined"}
            {#if question.field_type === "text"}
                <TextQuestion question={question} editable={editable} getQuestions={getQuestions} />
            {:else if question.field_type === "number"}
                <NumberQuestion question={question} editable={editable} getQuestions={getQuestions} />
            {:else if question.field_type === "boolean"}
                <BooleanQuestion question={question} editable={editable} getQuestions={getQuestions} />
            {:else if question.field_type === "choice"}
                <ChoiceQuestion question={question} editable={editable} getQuestions={getQuestions} />
            {/if}
        {/if}
    {/each}
</div>

<AddPitScoutingQuestionDialog getQuestions={getQuestions} seasonUuid={season_uuid}/>