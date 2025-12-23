<script lang="ts">
    import Input from "$lib/components/ui/input/input.svelte";
	import BaseQuestion from "./BaseQuestion.svelte";

    let { question, editable = false, getQuestions = () => {} } = $props();
</script>

<BaseQuestion question={question} editable={editable} getQuestions={getQuestions}>
    <Input type="number" name={question.uuid} placeholder={question.name} required={question.required} />
</BaseQuestion>
