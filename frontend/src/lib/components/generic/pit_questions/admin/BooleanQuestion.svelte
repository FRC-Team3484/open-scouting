<!-- 
@component
Admin preview for the boolean pit scouting question

Uses a hidden checkbox to always return either a true or false value

TODO: Update to match the BooleanField, to be a bit more robust

Props:
    - `question` (`PitFieldResponse`) - The data for this question
    - `editable` (`boolean`) - If this question is editable or not
    - `getQuestions` (`() => void`) - The function for fetching the questions
-->
<script lang="ts">
    import Checkbox from "$lib/components/ui/checkbox/checkbox.svelte";
    
	import type { PitFieldResponse } from "$lib/api/model";
	import BaseQuestion from "./BaseQuestion.svelte";


    interface Props {
        question: PitFieldResponse
        editable: boolean
        getQuestions: () => void
    }
    let { question, editable = false, getQuestions = () => {} }: Props = $props();

    let checked: boolean = $state(false);
</script>

<BaseQuestion question={question} editable={editable} getQuestions={getQuestions}>
    <!-- Use a hidden input to return a boolean value always, instead of only when checked if using a checkbox -->
    <input type="hidden" name={question.uuid} value={checked ? "true" : "false"} />
    <Checkbox placeholder={question.name} required={question.required} bind:checked />
</BaseQuestion>
