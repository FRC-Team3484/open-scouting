<!-- 
@component
Admin preview for the image pit scouting question

Props:
    - `question` (`PitFieldResponse`) - The data for this question
    - `editable` (`boolean`) - If this question is editable or not
    - `getQuestions` (`() => void`) - The function for fetching the questions
-->
<script lang="ts">
	import type { PitFieldResponse } from "$lib/api/model";
	import BaseQuestion from "./BaseQuestion.svelte";

    
    interface Props {
        question: PitFieldResponse
        editable: boolean
        getQuestions: () => void
    }
    let { question, editable = false, getQuestions = () => {} }: Props = $props();
</script>

<BaseQuestion question={question} editable={editable} getQuestions={getQuestions}>
    <p class="text-sm text-muted-foreground">Image upload options are visible on the scouting page</p>
</BaseQuestion>
