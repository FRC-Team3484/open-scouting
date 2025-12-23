<script lang="ts">
	import BaseQuestion from "./BaseQuestion.svelte";

    let { question, answers } = $props();
</script>

<BaseQuestion question={question} answers={answers}>
    <p>Number question</p>
</BaseQuestion>