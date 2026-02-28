<script lang="ts">
	import BaseQuestion from "./BaseQuestion.svelte";

    let { question, editable = false, getQuestions = () => {} } = $props();
</script>

<BaseQuestion question={question} editable={editable} getQuestions={getQuestions}>
    <p class="text-sm text-muted-foreground">Image upload options are visible on the scouting page</p>
</BaseQuestion>
