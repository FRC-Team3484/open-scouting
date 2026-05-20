<!-- 
@component
Main component used for rendering pit scouting fields

Only used on the admin page.

TODO: SeasonPitScoutingQuestion and PitFieldResponse need a unified schema
TODO: Pit scouting field presets need a proper response schema

Props:
    - `season_uuid` (`string`) - The uuid of the season to render fields for
    - `year` (`number`) - The year to render fields for
    - `event_data` (`Event`) - The current event that is being scouted
    - `editable` (`boolean`) - If the fields are editable or not
-->
<script lang="ts">
    import { onMount } from "svelte";
	import { toast } from "svelte-sonner";
    import { dragHandleZone } from "svelte-dnd-action"
	import { CircleNotchIcon, ExportIcon, PlusCircleIcon, TrashIcon, XCircleIcon } from "phosphor-svelte";
    
    import Separator from "../ui/separator/separator.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
	import Input from "../ui/input/input.svelte";

	import { db, type Event, type SeasonPitScoutingQuestion } from "$lib/utils/db";
	import AddPitScoutingQuestionDialog from "./dialogs/AddPitScoutingQuestionDialog.svelte";
	import { addPitScoutingQuestionDialogOpen } from "$lib/stores/dialog";
	import { clearPitFieldsPitsFieldsSeasonUuidClearDelete, createPitFieldPitsFieldsSeasonUuidCreatePost, getPitFieldsPitsFieldsSeasonUuidGet, getPitScoutingFieldPresetsPitsGetPresetsGet, movePitFieldsPitsFieldsSeasonUuidReorderPatch } from "$lib/api/pit-scouting/pit-scouting";
	import type { ReorderPitFieldsRequest } from "$lib/api/model";

	import TextQuestion from "./pit_questions/admin/TextQuestion.svelte";
	import NumberQuestion from "./pit_questions/admin/NumberQuestion.svelte";
	import BooleanQuestion from "./pit_questions/admin/BooleanQuestion.svelte";
	import ChoiceQuestion from "./pit_questions/admin/ChoiceQuestion.svelte";
	import ImageQuestion from "./pit_questions/admin/ImageQuestion.svelte";

    interface Props {
        season_uuid: string
        year: number
        event_data?: Event | null
        editable: boolean
    }    
    let { season_uuid, year, event_data = null, editable }: Props = $props();

    let questions: SeasonPitScoutingQuestion[] = $state([]);

    let fieldFile = $state(null);
    let presets = $state([]);
    let selectedPresetName = $state(null);
    let selectedPreset = $derived(
        presets.find(p => p.name === selectedPresetName) ?? null
    );

    /**
     * Get the pit scouting questions from the server if editing, and from the offline cache otherwise
     */
    async function getQuestions() {
        if (editable) {
            questions = (await getPitFieldsPitsFieldsSeasonUuidGet(season_uuid)).data;
            questions = questions.sort((a, b) => a.order - b.order);
        } else {
            const season = await db.season_data.get(season_uuid);
            questions = season?.pit_scouting_questions.sort((a, b) => a.order - b.order) ?? [];
        }
    }

    /**
     * Export pit scouting questions as JSON
     */
    async function exportQuestionsAsJSON() {
        const blob = new Blob([JSON.stringify(questions)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "pit_scouting_questions.json";
        a.click();
        URL.revokeObjectURL(url);
    }

    /**
     * Get pit scouting presets from the server
     */
    async function getPresets() {
        // TODO: this needs a proper response schema
        await getPitScoutingFieldPresetsPitsGetPresetsGet().then((response) => {
            if (response.status === 200) {
                presets = response.data
            }
        });
    }

    /**
     * Import pit scouting questions to the server
     * 
     * @param newQuestions The questions to import
     */
    async function importQuestionsToServer(newQuestions: SeasonPitScoutingQuestion[]) {
        await clearPitFieldsPitsFieldsSeasonUuidClearDelete(season_uuid).then(async (response) => {
            if (response.status === 200) {
                for (const question of newQuestions) {
                    const body = {
                        uuid: question.uuid,
                        season_uuid: season_uuid,
                        name: question.name,
                        description: question.description,
                        field_type: question.field_type,
                        options: question.options ?? {
                            choices: [],
                        },
                        required: question.required,
                        order: question.order,
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

    /**
     * Import pit scouting questions from the selected file
     */
    function importAsFile() {
        if (!fieldFile) {toast.error("No file selected"); return;}
        const file: File = fieldFile[0];

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

    /**
     * Import the selected question preset to teh server
     */
    function importAsPreset() {
        if (selectedPreset) {
            importQuestionsToServer(selectedPreset.preset);
        }
    }

    /**
     * Handler for when a drag item is being hovered over a drop area
     * 
     * @param e Drag and drop event
     */
    function handleDndConsider(e: Event) {
        questions = e.detail.items;
    }

    /**
     * Handler for when a drag item has been released into a drop area
     * 
     * The order of each question is updated to the server once an item is released
     * 
     * @param e Drag and drop event
     */
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

    /**
     * When the component initializes, get the questions
     */
    onMount(async () => {   
        getQuestions();
    });

    /**
     * When season_uuid or year changes, initalize the component again
     */
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
                    <Button onclick={() => {addPitScoutingQuestionDialogOpen.set(true);}}><PlusCircleIcon weight="bold" /> Add Question</Button>
                    <Dialog.Root onOpenChange={getPresets}>
                        <Dialog.Trigger>
                            <Button variant="outline" class="w-full"><ExportIcon weight="bold" /> Import Questions</Button>
                        </Dialog.Trigger>
                    
                        <Dialog.Content>
                            <Dialog.Title>Import Pit Scouting Questions</Dialog.Title>
                            <Dialog.Description>Import questions from a JSON file</Dialog.Description>

                            <p class="font-bold">Upload a JSON file:</p>
                            <div class="flex flex-row gap-2 flex-wrap">
                                <Input type="file" accept="application/json" id="presetfile" bind:files={fieldFile} />
                                <Button variant="outline" size="icon-sm" onclick={() => fieldFile = null}><TrashIcon weight="bold" /></Button>

                                <Dialog.Close>
                                    <Button onclick={() => importAsFile()} disabled={fieldFile == null}>Import JSON File</Button>
                                </Dialog.Close>
                            </div>

                            <p class="font-bold">Choose a preset:</p>
                            <div class="flex flex-row gap-2 flex-wrap">
                                {#if presets == null}
                                    <CircleNotchIcon class="animate-spin" size={22} />
                                    <p>Loading presets...</p>
                                {:else if presets.length == 0}
                                    <p class="text-muted-foreground">No presets found on the server</p>
                                {:else}
                                    <Select.Root
                                        type="single"
                                        name="preset"
                                        id="preset"
                                        bind:value={selectedPresetName}
                                        >
                                        <Select.Trigger>
                                            {selectedPresetName ?? "Select a preset"}
                                        </Select.Trigger>

                                        <Select.Content>
                                            {#each presets as preset}
                                            <Select.Item
                                                value={preset.name}
                                                label={preset.name}
                                            />
                                            {/each}
                                        </Select.Content>
                                    </Select.Root>

                                    <Button variant="outline" size="icon-sm" onclick={() => selectedPresetName = null}><XCircleIcon weight="bold" /></Button>

                                    <Dialog.Close>
                                        <Button onclick={() => importAsPreset()} disabled={selectedPresetName == null}>Import Preset</Button>
                                    </Dialog.Close>
                                {/if}
                            </div>

                            <Dialog.Footer>
                                <Dialog.Close><Button variant="outline">Close</Button></Dialog.Close>
                            </Dialog.Footer>
                        </Dialog.Content>
                    </Dialog.Root>
                    <Button variant="outline" onclick={() => {exportQuestionsAsJSON();}}><ExportIcon weight="bold" /> Export as JSON</Button>
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