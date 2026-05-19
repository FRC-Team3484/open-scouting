<!-- 
@component
The pit scouting question for a single choice

Props:
    - `pit` (`PitScoutingData`) - The parent pit for this question
    - `question` (`SeasonPitScoutingQuestion`) - The question
    - `answers` (`PitScoutingAnswer[]`) - Any answers for this question
    - `user` (`unknown`) - The user from the parent
-->
<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Select from "$lib/components/ui/select/index.js";

	import { db, type PitScoutingAnswer, type PitScoutingData, type SeasonPitScoutingQuestion } from "$lib/utils/db";
	import BaseQuestion from "./BaseQuestion.svelte";

    
    interface Props {
        pit: PitScoutingData
        question: SeasonPitScoutingQuestion
        answers: PitScoutingAnswer[]
        user: unknown
    }
    let { pit, question, answers, user }: Props = $props();

    let value = $state("na");
    const selectedOptionLabel = $derived(
        question.options.choices.find((o) => o.id === value) ?? { id: "na", name: "N/A" }
    )

    let baseQuestion: ReturnType<typeof BaseQuestion>;

    /**
     * Add the typed answer to this question
     */
    async function addAnswer() {
        const newAnswer = { uuid: crypto.randomUUID(), value: selectedOptionLabel.name, username: user?.username ?? "guest", field_uuid: question.uuid, created_at: new Date().toISOString() }
        await db.pit_scouting.update(pit.uuid, {
            answers: [...pit.answers, newAnswer],
            synced: false
        });

        value = "na";
        baseQuestion.reset();
    }
</script>

<BaseQuestion question={question} answers={answers} bind:this={baseQuestion}>
    <div class="flex flex-row gap-2 items-center">

        <Select.Root type="single" name={question.uuid} required={question.required} bind:value>
            <Select.Trigger>{selectedOptionLabel.name}</Select.Trigger>

            <Select.Content>
                <Select.Label>Options</Select.Label>
                <Select.Item value="na">N/A</Select.Item>
                {#each question.options.choices as option}
                    <Select.Item value={option.id}>
                        {option.name}
                    </Select.Item>
                {/each}
            </Select.Content>
        </Select.Root>

        <Button onclick={addAnswer}>Save</Button>
    </div>
</BaseQuestion>