<!-- 
@component
Admin preview for the number pit scouting question

Props:
    - `question` (`PitFieldResponse`) - The data for this question
    - `editable` (`boolean`) - If this question is editable or not
    - `getQuestions` (`() => void`) - The function for fetching the questions
-->
<script lang="ts">
    import Input from "$lib/components/ui/input/input.svelte";
    
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
    <Input type="number" name={question.uuid} placeholder={question.name} required={question.required} />
</BaseQuestion>
