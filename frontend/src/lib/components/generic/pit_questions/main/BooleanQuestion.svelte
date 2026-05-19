<!-- 
@component
The boolean pit scouting question

Uses a hidden input to always return a true or a false value

TODO: Add an interface for the user
TODO: Match the fake checkbox method to what is done in BooleanField, to be more robust

Props:
    - `pit` (`PitScoutingData`) - The parent pit for this question
    - `question` (`SeasonPitScoutingQuestion`) - The question
    - `answers` (`PitScoutingAnswer[]`) - Any answers for this question
    - `user` (`unknown`) - The user from the parent
-->
<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
    import Switch from "$lib/components/ui/switch/switch.svelte";

	import { db, type PitScoutingAnswer, type PitScoutingData, type SeasonPitScoutingQuestion } from "$lib/utils/db";
	import BaseQuestion from "./BaseQuestion.svelte";


    interface Props {
        pit: PitScoutingData
        question: SeasonPitScoutingQuestion
        answers: PitScoutingAnswer[]
        user: unknown
    }
    let { pit, question, answers, user }: Props = $props();

    let checked = $state(false);
    let baseQuestion: ReturnType<typeof BaseQuestion>;

    /**
     * Add the typed answer to this question
     */
    async function addAnswer() {
        const newAnswer: PitScoutingAnswer = { uuid: crypto.randomUUID(), value: checked, username: user?.username ?? "guest", field_uuid: question.uuid, created_at: new Date().toISOString() }
        await db.pit_scouting.update(pit.uuid, {
        answers: [...pit.answers, newAnswer],
            synced: false
        });

        checked = false;
        baseQuestion.reset();
    }
</script>

<BaseQuestion question={question} answers={answers} bind:this={baseQuestion}>
    <div class="flex flex-row gap-2 items-center">
        <!-- Use a hidden input to return a boolean value always, instead of only when checked if using a checkbox -->
        <input type="hidden" name={question.uuid} value={checked ? "true" : "false"} />
        <Switch class="touch-manipulation" placeholder={question.name} bind:checked />
        <p>{checked.toString().charAt(0).toUpperCase() + checked.toString().slice(1)}</p>
        <Button onclick={addAnswer}>Save</Button>
    </div>
</BaseQuestion>