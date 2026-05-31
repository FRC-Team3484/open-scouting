<!-- 
@component
Wrapper components for all pit scouting questions on the admin page

Handles deleting, editing, and reordering of pit scouting 
    questions, if the question is editable.

Props:
    - `question` (`PitFieldResponse`) - Data for this question
    - `editable` (`boolean`) - If the question if editable or not
    - `getQuestions` (`() => void`) - The function for fetching questions
    - `children` (`Snippet`) - The children to render inside the component
-->
<script lang="ts">
	import { dragHandle } from "svelte-dnd-action";
	import type { Snippet } from "svelte";
	import { toast } from "svelte-sonner";
	import { DotsSixVerticalIcon, DotsThreeIcon, PencilIcon, TrashIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";

	import { deletePitFieldPitsFieldsFieldUuidDeleteDelete } from "$lib/api/pit-scouting/pit-scouting";
	import { addPitScoutingQuestionData, addPitScoutingQuestionDialogOpen } from "$lib/stores/dialog";
	import type { PitFieldResponse } from "$lib/api/model";


    interface Props {
        question: PitFieldResponse
        editable: boolean
        getQuestions: () => void
        children: Snippet
    }
    let { question, editable = false, getQuestions = () => {}, children }: Props = $props();

    /**
     * Delete this question
     */
    async function deleteQuestion() {
        await deletePitFieldPitsFieldsFieldUuidDeleteDelete(question.uuid).then(async (response) => {
            await getQuestions();
            toast.success("Question deleted", { duration: 5000 });
        }).catch((error) => {
            console.warn("Failed to delete question", error);
            toast.error("Failed to delete question", { duration: 5000 });
        });
    }

    /**
     * Open the dialog for editing this question
     */
    function editQuestion() {
        addPitScoutingQuestionDialogOpen.set(true);
        addPitScoutingQuestionData.set(question);
    }
</script>

<Card.Root class="w-auto min-w-64">
    <Card.Header>
        <div class="flex flex-col gap-2 text-left">
            <div class="flex flex-row gap-2 items-center justify-between flex-wrap">
                <div class="flex flex-row gap-2 items-center">
                    <div class="text-muted-foreground" use:dragHandle>
                        <DotsSixVerticalIcon weight="bold" />
                    </div>
                    <p>
                        {question.name}
                        {#if question.required}
                            <span class="text-red-500">*</span>
                        {/if}
                    </p>
                    {#if editable}
                        <p class="text-sm opacity-80">{question.field_type}</p>
                    {/if}
                </div>
                {#if editable}
                    <DropdownMenu.Root>
                        <DropdownMenu.Trigger>
                            <Button size="icon" variant="outline"><DotsThreeIcon weight="bold" /></Button>
                        </DropdownMenu.Trigger>
                        <DropdownMenu.Content class="w-56" align="start">
                            <DropdownMenu.Label>Question Options</DropdownMenu.Label>
                            <DropdownMenu.Group>
                                <DropdownMenu.Item onclick={editQuestion}><PencilIcon weight="bold" /> Edit</DropdownMenu.Item>
                                <DropdownMenu.Item onclick={deleteQuestion}><TrashIcon weight="bold" /> Delete</DropdownMenu.Item>
                            </DropdownMenu.Group>
                        </DropdownMenu.Content>
                    </DropdownMenu.Root>
                {/if}
            </div>

            {#if question.description}
                <p class="text-sm text-muted-foreground">{question.description}</p>
            {/if}
        </div>
    </Card.Header>

    <Card.Content>
        {@render children()}
    </Card.Content>
</Card.Root>