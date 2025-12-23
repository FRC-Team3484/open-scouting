<script lang="ts">
    import Checkbox from "$lib/components/ui/checkbox/checkbox.svelte";
	import BaseQuestion from "./BaseQuestion.svelte";

    let { question, editable = false, getQuestions = () => {} } = $props();

    let checked = $state(false);
</script>

<BaseQuestion question={question} editable={editable} getQuestions={getQuestions}>
    <!-- Use a hidden input to return a boolean value always, instead of only when checked if using a checkbox -->
    <input type="hidden" name={question.uuid} value={checked ? "true" : "false"} />
    <Checkbox placeholder={question.name} required={question.required} bind:checked />
</BaseQuestion>
