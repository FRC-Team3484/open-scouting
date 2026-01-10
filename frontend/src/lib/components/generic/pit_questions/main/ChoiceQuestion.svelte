<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Select from "$lib/components/ui/select/index.js";
	import { db } from "$lib/utils/db";
	import BaseQuestion from "./BaseQuestion.svelte";

    let { pit, question, answers, user } = $props();

    let value = $state("na");
    const selectedOptionLabel = $derived(
        question.options.find((o) => o.id === value) ?? { id: "na", name: "N/A" }
    )

    let resetBase;

    async function addAnswer() {
        const newAnswer = { uuid: crypto.randomUUID(), value: selectedOptionLabel.name, username: user?.username ?? "guest", field_uuid: question.uuid, created_at: new Date().toISOString() }
        await db.pit_scouting.update(pit.uuid, {
            answers: [...pit.answers, newAnswer],
            synced: false
        });

        value = "na";
        resetBase();
    }
</script>

<BaseQuestion question={question} answers={answers} bind:reset={resetBase}>
    <div class="flex flex-row gap-2 items-center">

        <Select.Root type="single" name={question.uuid} required={question.required} bind:value>
            <Select.Trigger>{selectedOptionLabel.name}</Select.Trigger>

            <Select.Content>
                <Select.Label>Options</Select.Label>
                <Select.Item value="na">N/A</Select.Item>
                {#each question.options as option}
                    <Select.Item value={option.id}>
                        {option.name}
                    </Select.Item>
                {/each}
            </Select.Content>
        </Select.Root>

        <Button onclick={addAnswer}>Save</Button>
    </div>
</BaseQuestion>