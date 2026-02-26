<script lang="ts">
    import { onMount } from "svelte";
    import { dndzone, dragHandleZone, overrideItemIdKeyNameBeforeInitialisingDndZones } from "svelte-dnd-action"
    
    import Separator from "../ui/separator/separator.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { Export, PlusCircle, Trash } from "phosphor-svelte";
    import * as Dialog from "$lib/components/ui/dialog/index.js";

	import AddPitScoutingQuestionDialog from "./dialogs/AddPitScoutingQuestionDialog.svelte";
	import { addPitScoutingQuestionDialogOpen } from "$lib/stores/dialog";
	import { db } from "$lib/utils/db";
	import TextQuestion from "./pit_questions/admin/TextQuestion.svelte";
	import NumberQuestion from "./pit_questions/admin/NumberQuestion.svelte";
	import BooleanQuestion from "./pit_questions/admin/BooleanQuestion.svelte";
	import ChoiceQuestion from "./pit_questions/admin/ChoiceQuestion.svelte";
	import { toast } from "svelte-sonner";
	import Input from "../ui/input/input.svelte";
	import { clearPitFieldsPitsFieldsSeasonUuidClearDelete, createPitFieldPitsFieldsSeasonUuidCreatePost, getPitFieldsPitsFieldsSeasonUuidGet, movePitFieldsPitsFieldsSeasonUuidReorderPatch } from "$lib/api/pit-scouting/pit-scouting";
	import type { ReorderPitFieldsRequest } from "$lib/api/model";
	import ImageQuestion from "./pit_questions/admin/ImageQuestion.svelte";

    let { season_uuid, year, event_data = {}, editable } = $props();

    let questions = $state([]);

    let fieldFile = $state(null);

    async function getQuestions() {
        if (editable) {
            questions = (await getPitFieldsPitsFieldsSeasonUuidGet(season_uuid)).data;
            questions = questions.sort((a, b) => a.order - b.order);
        } else {
            const season = await db.season_data.get(parseInt(year));
            questions = season?.pit_scouting_questions.sort((a, b) => a.order - b.order) ?? [];
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
        await clearPitFieldsPitsFieldsSeasonUuidClearDelete(season_uuid).then(async (response) => {
            if (response.status === 200) {
                for (const question of newQuestions) {
                    const body = {
                        season_uuid: season_uuid,
                        name: question.name,
                        field_type: question.field_type,
                        options: question.options ?? {
                            choices: [],
                        },
                        order: 0,
                        organization_uuid: null as string | null,
                    }

                    await createPitFieldPitsFieldsSeasonUuidCreatePost(season_uuid, body).catch((error) => {
                        console.error("Failed to create question:", question.name, error)
                    });
                }

                getQuestions();
                toast.success("Questions imported", { duration: 5000 });
            }
        });
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

    function handleDndConsider(e) {
        questions = e.detail.items;
    }

    async function handleDndFinalize(e) {
        questions = e.detail.items;
        
        let body: ReorderPitFieldsRequest = []

        for (const question of questions) {
            question.order = questions.indexOf(question);

            body.push({
                uuid: question.uuid,
                order: question.order
            })
        }


        await movePitFieldsPitsFieldsSeasonUuidReorderPatch(season_uuid, body).then((response) => {
            if (response.status !== 200) {
                toast.error("Failed to reorder questions", { duration: 5000 });
            }
        });
    }

    onMount(async () => {
        if (editable) {
            overrideItemIdKeyNameBeforeInitialisingDndZones("uuid");
        }

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
                            <Dialog.Description>Import questions from a JSON file</Dialog.Description>

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

{#snippet questionBlock()}
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
            {:else if question.field_type === "image"}
                <ImageQuestion question={question} editable={editable} getQuestions={getQuestions} />
            {/if}
        {/if}
    {/each}

    {#if questions.length === 0}
        <p class="text-muted-foreground">No questions found</p>
    {/if}
{/snippet}

{#if editable}
    <div class="flex flex-col gap-4 mt-4 max-w-screen w-full md:w-lg" use:dragHandleZone={ {items: questions, flipDurationMs: 100, dropTargetStyle: {outline: 'var(--primary) dashed 2px', borderRadius: 'var(--radius)'} }} on:consider={handleDndConsider} on:finalize={handleDndFinalize}>
        {@render questionBlock()}
    </div>
{:else}
    <div class="flex flex-col gap-4 mt-4 max-w-screen w-full md:w-lg">
        {@render questionBlock()}
    </div>
{/if}

<AddPitScoutingQuestionDialog getQuestions={getQuestions} seasonUuid={season_uuid}/>