<script lang="ts">
	import { onMount } from "svelte";
    
    import Separator from "../ui/separator/separator.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { Export, PlusCircle, Trash } from "phosphor-svelte";
    import * as Dialog from "$lib/components/ui/dialog/index.js";

	import AddPitScoutingQuestionDialog from "./dialogs/AddPitScoutingQuestionDialog.svelte";
	import { addPitScoutingQuestionDialogOpen } from "$lib/stores/dialog";
	import { apiFetch } from "$lib/utils/api";
	import { db } from "$lib/utils/db";
	import TextQuestion from "./pit_questions/admin/TextQuestion.svelte";
	import NumberQuestion from "./pit_questions/admin/NumberQuestion.svelte";
	import BooleanQuestion from "./pit_questions/admin/BooleanQuestion.svelte";
	import ChoiceQuestion from "./pit_questions/admin/ChoiceQuestion.svelte";
	import { toast } from "svelte-sonner";
	import Input from "../ui/input/input.svelte";

    let { season_uuid, year, event_data = {}, editable } = $props();

    let questions = $state([]);

    let fieldFile = $state(null);

    async function getQuestions() {
        if (editable) {
            questions = await apiFetch(`/pits/fields/${season_uuid}`);
        } else {
            const season = await db.season_data.get(parseInt(year));
            questions = season?.pit_scouting_questions;
        }
    }

    async function exportQuestionsAsJSON() {
        const blob = new Blob([JSON.stringify(questions)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "pit_scouting_questions.json";
        a.click();
        URL.revokeObjectURL(url);
    }

    async function importQuestionsToServer(newQuestions) {
        // Clear existing pit questions
        await apiFetch(`/pits/fields/${season_uuid}/clear`, {
            method: "DELETE",
            token: localStorage.getItem("access_token")
        });

        // Create questions in order
        for (let i = 0; i < newQuestions.length; i++) {
            const question = newQuestions[i];

            const body = new FormData();
            body.append("name", question.name);
            body.append("field_type", question.field_type);
            body.append("order", question.order?.toString() ?? i.toString());
            body.append("organization_uuid", "");

            if (question.field_type === "choice") {
                body.append("options", JSON.stringify(question.options ?? []));
            } else {
                body.append("options", "[]");
            }

            try {
                await apiFetch(`/pits/fields/${season_uuid}/create`, {
                    method: "POST",
                    data: body,
                    token: localStorage.getItem("access_token")
                });
            } catch (error) {
                console.error("Failed to import pit question:", question.name, error);
            }
        }

        getQuestions();
        toast.success("Questions imported", { duration: 5000 });
    }

    function importAsFile() {
        const file = fieldFile[0];

        if (file && file.type === "application/json") {
            const reader = new FileReader();
            reader.onload = () => {
                try {
                    const newQuestions = JSON.parse(reader.result as string);

                    if (newQuestions.length > 0) {
                        importQuestionsToServer(newQuestions);

                    } else {
                        toast.error("File is empty or invalid", { duration: 5000 });
                        fieldFile = null;
                    }
                } catch (error) {
                    console.error(error);
                    toast.error("Invalid file", { duration: 5000 });
                    fieldFile = null;
                }
            };
            reader.readAsText(file);
        } else {
            toast.error("Invalid file type", { duration: 5000 });
            fieldFile = null;
        }
    }

    onMount(async () => {
        getQuestions();
    });

    $effect(() => {
        season_uuid;
        year;

        getQuestions();
    })
</script>

{#if editable}
    <div class="flex flex-col gap-4">
        <Separator orientation="horizontal" />

        <Card.Root class="w-auto min-w-64">
            <Card.Content>
                <div class="flex flex-col gap-2">
                    <Button onclick={() => {addPitScoutingQuestionDialogOpen.set(true);}}><PlusCircle weight="bold" /> Add Question</Button>
                    <Dialog.Root>
                        <Dialog.Trigger>
                            <Button variant="outline" class="w-full"><Export weight="bold" /> Import Questions</Button>
                        </Dialog.Trigger>
                    
                        <Dialog.Content>
                            <Dialog.Title>Import Pit Scouting Questions</Dialog.Title>
                            <Dialog.Description>Not yet implemented</Dialog.Description>

                            <p class="font-bold">Upload a JSON file:</p>
                            <div class="flex flex-row gap-2 flex-wrap">
                                <Input type="file" accept="application/json" id="presetfile" bind:files={fieldFile} />
                                <Button variant="outline" size="icon-sm" onclick={() => fieldFile = null}><Trash weight="bold" /></Button>

                                <Dialog.Close>
                                    <Button onclick={() => importAsFile()} disabled={fieldFile == null}>Import JSON File</Button>
                                </Dialog.Close>
                            </div>

                            <Dialog.Footer>
                                <Dialog.Close><Button variant="outline">Close</Button></Dialog.Close>
                            </Dialog.Footer>
                        </Dialog.Content>
                    </Dialog.Root>
                    <Button variant="outline" onclick={() => {exportQuestionsAsJSON();}}><Export weight="bold" /> Export as JSON</Button>
                </div>
            </Card.Content>
        </Card.Root>
    </div>
{/if}

<div class="flex flex-col gap-4 mt-4">
    {#each questions as question (question.uuid)}
        {#if question.field_type !== "undefined"}
            {#if question.field_type === "text"}
                <TextQuestion question={question} editable={editable} getQuestions={getQuestions} />
            {:else if question.field_type === "number"}
                <NumberQuestion question={question} editable={editable} getQuestions={getQuestions} />
            {:else if question.field_type === "boolean"}
                <BooleanQuestion question={question} editable={editable} getQuestions={getQuestions} />
            {:else if question.field_type === "choice"}
                <ChoiceQuestion question={question} editable={editable} getQuestions={getQuestions} />
            {/if}
        {/if}
    {/each}

    {#if questions.length === 0}
        <p class="text-muted-foreground">No questions found</p>
    {/if}
</div>

<AddPitScoutingQuestionDialog getQuestions={getQuestions} seasonUuid={season_uuid}/>