<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
    import Switch from "$lib/components/ui/switch/switch.svelte";
	import { db } from "$lib/utils/db";
	import BaseQuestion from "./BaseQuestion.svelte";

    let { pit, question, answers, user } = $props();

    let checked = $state(false);
    let resetBase;

    async function addAnswer() {
        const newAnswer = { uuid: crypto.randomUUID(), value: checked, username: user?.username ?? "guest", field_uuid: question.uuid, created_at: new Date().toISOString() }
        await db.pit_scouting.update(pit.uuid, {
        answers: [...pit.answers, newAnswer],
            synced: false
        });

        checked = false;
        resetBase();
    }
</script>

<BaseQuestion question={question} answers={answers} bind:reset={resetBase}>
    <div class="flex flex-row gap-2 items-center">
        <!-- Use a hidden input to return a boolean value always, instead of only when checked if using a checkbox -->
        <input type="hidden" name={question.uuid} value={checked ? "true" : "false"} />
        <Switch class="touch-manipulation" placeholder={question.name} bind:checked />
        <p>{checked.toString().charAt(0).toUpperCase() + checked.toString().slice(1)}</p>
        <Button onclick={addAnswer}>Save</Button>
    </div>
</BaseQuestion>