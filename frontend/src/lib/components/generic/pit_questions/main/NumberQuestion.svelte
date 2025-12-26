<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
	import { db } from "$lib/utils/db";
	import BaseQuestion from "./BaseQuestion.svelte";

    let { pit, question, answers, user } = $props();

    let value = $state(0);
    let resetBase;

    async function addAnswer() {
        const newAnswer = { uuid: crypto.randomUUID(), value: value, username: user.username, field_uuid: question.uuid, created_at: new Date().toISOString() }
        await db.pit_scouting.update(pit.uuid, {
            answers: [...pit.answers, newAnswer],
            synced: false
        });

        value = 0;
        resetBase();
    }
</script>

<BaseQuestion question={question} answers={answers} bind:reset={resetBase}>
    <div class="flex flex-row gap-2 items-center">
        <Input type="number" placeholder={question.name} bind:value />
        <Button onclick={addAnswer}>Save</Button>
    </div>
</BaseQuestion>