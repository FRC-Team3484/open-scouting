<script lang="ts">
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";
	import { CircleNotch, DownloadSimple, Export, FolderPlus, Info, PlusCircle, Trash, Warning, XCircle } from "phosphor-svelte";

    import { addFieldDialogOpen, addSectionDialogOpen } from "$lib/stores/dialog";

	import Skeleton from "../ui/skeleton/skeleton.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import Button from "../ui/button/button.svelte";
    import * as Select from "$lib/components/ui/select/index.js";
	import Separator from "../ui/separator/separator.svelte";
	import Input from "../ui/input/input.svelte";
	import * as Alert from "../ui/alert/index.js";

	import { db } from "$lib/utils/db";
	import { validateTokenOnline } from "$lib/utils/user";
	import { pushMatchScoutingData } from "$lib/utils/sync";
    
	import { clearSeasonFieldsFieldsSeasonSeasonUuidClearDelete, createSeasonFieldFieldsSeasonSeasonUuidCreatePost, getMatchScoutingFieldPresetsFieldsGetPresetsGet, getSeasonFieldsFieldsSeasonSeasonUuidGet } from "$lib/api/match-scouting-fields/match-scouting-fields";
	import { getSeasonGamepiecesGamepiecesSeasonSeasonUuidGet } from "$lib/api/gamepieces/gamepieces";
	import type { GamepieceResponse } from "$lib/api/model";

	import StringField from "./fields/StringField.svelte";
	import LargeNumberField from "./fields/LargeNumberField.svelte";
	import SmallNumberField from "./fields/SmallNumberField.svelte";
	import BooleanField from "./fields/BooleanField.svelte";
	import ChoiceField from "./fields/ChoiceField.svelte";
	import MultipleChoiceField from "./fields/MultipleChoiceField.svelte";
	import Section from "./fields/Section.svelte";

	import AddSectionDialog from "./dialogs/AddSectionDialog.svelte";
	import AddFieldDialog from "./dialogs/AddFieldDialog.svelte";
	import MathScoutingSubmit from "./MathScoutingSubmit.svelte";
	import MatchScoutingTeamInfo from "./MatchScoutingMatchInfo.svelte";
	import CoarseSmallNumberField from "./fields/CoarseSmallNumberField.svelte";
    
    
    let matchScoutingTeamInfoChild;

    type Node = {
        id: string;
        type: "section" | "field";
        name: string;
        order: number;
        children?: Node[]; // only for sections
        field_type?: string;
        stat_type?: string;
        game_piece_uuid?: string;
        required?: boolean;
        options?: any;
    };

    let fields: Node[] = $state([]);
    let gamePieces: GamepieceResponse[] = $state([]);

    type ChoiceType = {id: string; name: string }[];
    let choices: ChoiceType[] = [];

    let user;

    let fieldFile = $state(null);
    let presets = $state([]);
    let selectedPresetName = $state(null);
    let selectedPreset = $derived(
        presets.find(p => p.name === selectedPresetName) ?? null
    );

    let { season_uuid, year, event_data = {}, editable } = $props();

    async function getStructure() {
        if (editable) {
            // TODO: this needs a proper response schema
            fields = (await getSeasonFieldsFieldsSeasonSeasonUuidGet(season_uuid)).data;
        } else {
            const season = await db.season_data.get(parseInt(year));
            fields = season?.fields
        }
    }

    async function getGamePieces() {
        if (editable) {
            await getSeasonGamepiecesGamepiecesSeasonSeasonUuidGet(season_uuid).then((response) => {
                if (response.status === 200) {
                    gamePieces = response.data
                }
            });
        } else {
            const season = await db.season_data.get(parseInt(year));
            gamePieces = season?.game_pieces
        }
    }

    async function submit(event: Event) {
        event.preventDefault();

        const form = event.currentTarget as HTMLFormElement;
        const formData = new FormData(form);

        const EXCLUDED_KEYS = new Set([
            "team_number",
            "match_number",
            "match_type",
            "position",
        ]);

        // Exclude fields and merge duplicates (likely from a multiple_choice field) into a stringified array
        const filteredFields: Record<string, string> = {};
        const seen = new Set<string>();

        for (const [key, value] of formData.entries()) {
            if (EXCLUDED_KEYS.has(key)) continue;

            if (seen.has(key)) {
                const current = filteredFields[key];
                const arr = current.startsWith("[")
                    ? JSON.parse(current)
                    : [current];

                arr.push(value);
                filteredFields[key] = JSON.stringify(arr);
            } else {
                seen.add(key);
                filteredFields[key] = value as string;
            }
        }

        console.log(filteredFields);

        await db.match_scouting.add({
            uuid: crypto.randomUUID(),
            data: filteredFields,
            user_uuid: user?.uuid ?? "",
            year: event_data.year,
            team_number: parseInt(formData.get("team_number")),
            match_number: parseInt(formData.get("match_number")),
            match_type: formData.get("match_type"),
            event_code: event_data.event_code,
            event_name: event_data.event_name,
            event_type: event_data.event_type,
            event_city: event_data.event_city,
            event_country: event_data.event_country,
            event_start_date: event_data.event_start_date,
            event_end_date: event_data.event_end_date,
            synced: false
        });

        toast.success("Match scouting data saved", { duration: 5000 });
        form.reset();

        // Delay 100ms while form is resetting
        setTimeout(() => {
            matchScoutingTeamInfoChild.increment_match_number(parseInt(formData.get("match_number")), formData.get("match_type"), formData.get("position"));
        }, 100);
    
        scrollTo({ top: 0, behavior: "smooth" });

        await pushMatchScoutingData();
    }

    function exportFields() {
        const json = JSON.stringify(fields, null, 2);
        const blob = new Blob([json], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "fields.json";
        a.click();
        URL.revokeObjectURL(url);
    }

    async function getPresets() {
        // TODO: this needs a proper response schema
        await getMatchScoutingFieldPresetsFieldsGetPresetsGet().then((response) => {
            if (response.status === 200) {
                presets = response.data
            }
        });
    }

    async function createFieldRecursive(field, parentUuid: string) {
        const body = {
            uuid: field.uuid,
            name: field.name,
            season_uuid: season_uuid,
            field_type: field.field_type,
            stat_type: field.stat_type,
            required: field.required,
            order: field.order,
            organization_uuid: field.organization_uuid ?? null as string | null,
            parent_uuid: parentUuid ?? null as string | null,
            options: field.options ?? {
                choices: [],
                minimum: 0,
                maximum: 0,
                default: 0
            },
            game_piece_uuid: field.game_piece_uuid ?? null as string | null,
        }

        // Create field / section
        await createSeasonFieldFieldsSeasonSeasonUuidCreatePost(season_uuid, body).then(async (response) => {
            if (response.status === 200) {
                const newUuid = field?.uuid;
                if (!newUuid) return;
    
                // Recurse into children
                if (field.field_type === "section" && Array.isArray(field.fields)) {
                    for (const child of field.fields) {
                        await createFieldRecursive(child, newUuid);
                    }
                }
            }

        }).catch((error) => {
            console.error("Failed to create field:", field.name, error);
            return;
        });
    }

    async function importFieldsToServer(newFields) {
        await clearSeasonFieldsFieldsSeasonSeasonUuidClearDelete(season_uuid).then(async (response) => {
            if (response.status === 200) {
                for (const field of newFields) {
                    await createFieldRecursive(field, null);
                }
        
                // Refresh structure once everything is done
                toast.success("Fields imported", { duration: 5000 });
                getStructure();
            }
        });
    }

    function importAsFile() {
        const file = fieldFile[0];

        if (file && file.type === "application/json") {
            const reader = new FileReader();
            reader.onload = () => {
                try {
                    const newFields = JSON.parse(reader.result as string);

                    if (newFields.length > 0) {
                        importFieldsToServer(newFields);

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

    function importAsPreset() {
        if (selectedPreset) {
            importFieldsToServer(selectedPreset.preset);
        }
    }

    onMount(async () => {
        while (!season_uuid) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        getStructure();
        getGamePieces();

        user = await validateTokenOnline();
    });

    $effect(() => {
        season_uuid;
        year;

        getStructure();
        getGamePieces();
    })
</script>

<div class="flex flex-col gap-4">
    {#if season_uuid == ""}
        <Skeleton class="w-128 h-32" />
        <Skeleton class="w-128 h-32" />
        <Skeleton class="w-128 h-32" />
    {:else}
        {#if editable}
            <Card.Root class="w-auto min-w-64">
                <Card.Content>
                    <div class="flex flex-col gap-4">
                        <Button onclick={() => addFieldDialogOpen.set(true)}><PlusCircle weight="bold" /> Add Field</Button>
                        <Button onclick={() => addSectionDialogOpen.set(true)}><FolderPlus weight="bold" /> Add Section</Button>
                        <div class="flex flex-row gap-2 flex-wrap">
                            <Dialog.Root onOpenChange={getPresets}>
                                <Dialog.Trigger>
                                    <Button variant="outline" class="w-full"><DownloadSimple weight="bold" /> Import Fields</Button>
                                </Dialog.Trigger>
                                <Dialog.Content>
                                    <Dialog.Title>Import Field Data</Dialog.Title>
                                    <Dialog.Description>Import Field Data either from a JSON file, or from a preset provided by the server.</Dialog.Description>
                                    
                                    <Alert.Root variant="destructive">
                                        <Warning weight="bold" />
                                        <Alert.Description>All existing field data for this season will be permanently overwritten</Alert.Description>
                                    </Alert.Root>

                                    <p class="font-bold">Upload a JSON file:</p>
                                    <div class="flex flex-row gap-2 flex-wrap">
                                        <Input type="file" accept="application/json" id="presetfile" bind:files={fieldFile} />
                                        <Button variant="outline" size="icon-sm" onclick={() => fieldFile = null}><Trash weight="bold" /></Button>

                                        <Dialog.Close>
                                            <Button onclick={() => importAsFile()} disabled={fieldFile == null}>Import JSON File</Button>
                                        </Dialog.Close>
                                    </div>

                                    <p class="font-bold">Choose a preset:</p>
                                    <div class="flex flex-row gap-2 flex-wrap">
                                        {#if presets == null}
                                            <CircleNotch class="animate-spin" size={22} />
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

                                            <Button variant="outline" size="icon-sm" onclick={() => selectedPresetName = null}><XCircle weight="bold" /></Button>

                                            <Dialog.Close>
                                                <Button onclick={() => importAsPreset()} disabled={selectedPresetName == null}>Import Preset</Button>
                                            </Dialog.Close>
                                        {/if}
                                    </div>

                                    <Dialog.Footer>
                                        <Dialog.Close>
                                            <Button variant="outline">Close</Button>
                                        </Dialog.Close>
                                    </Dialog.Footer>
                                </Dialog.Content>
                            </Dialog.Root>
                            <Button variant="outline" onclick={() => exportFields()} class="flex-2"><Export weight="bold" /> Export Fields as JSON</Button>

                            <Dialog.Root>
                                <Dialog.Trigger>
                                    <Button variant="outline" size="icon"><Info weight="bold" /></Button>
                                </Dialog.Trigger>
                                <Dialog.Content>
                                    <Dialog.Title>About Exported Field Data</Dialog.Title>
                                    <Dialog.Description>Exported data can be imported on another server, or used to add a season preset into the repo at the start of a new season.</Dialog.Description>

                                    <Dialog.Footer>
                                        <Dialog.Close>
                                            <Button variant="outline">Close</Button>
                                        </Dialog.Close>
                                    </Dialog.Footer>
                                </Dialog.Content>
                            </Dialog.Root>
                        </div>
                    </div>
                </Card.Content>
            </Card.Root>

            <Separator orientation="horizontal" />
        {/if}
        
        <form method="post" onsubmit={submit} class="flex flex-col gap-2">
            {#if editable}
                <Card.Root class="w-auto min-w-64">
                    <Card.Content>
                        <div class="flex flex-row gap-2 items-center">
                            <Info weight="bold"/>
                            <p class="text-sm">Team number, match number, and match type fields are visible during full match scouting</p>
                        </div>
                    </Card.Content>
                </Card.Root>
            {:else}
                <MatchScoutingTeamInfo event_data={event_data} bind:this={matchScoutingTeamInfoChild} />
            {/if}
            
            {#each fields as field (field.uuid)}
                {#if field.field_type === "string"}
                    <StringField field={field} editable={editable} getFields={getStructure}/>
                {:else if field.field_type === "large_number"}
                    <LargeNumberField field={field} editable={editable} getFields={getStructure}/>
                {:else if field.field_type === "small_number"}
                    <SmallNumberField field={field} editable={editable} getFields={getStructure}/>
                {:else if field.field_type === "coarse_small_number"}
                    <CoarseSmallNumberField field={field} editable={editable} getFields={getStructure}/>
                {:else if field.field_type === "boolean"}
                    <BooleanField field={field} editable={editable} getFields={getStructure}/>
                {:else if field.field_type === "choice"}
                    <ChoiceField field={field} editable={editable} getFields={getStructure}/>
                {:else if field.field_type === "multiple_choice"}
                    <MultipleChoiceField field={field} editable={editable} getFields={getStructure}/>
                {:else if field.field_type === "section"}
                    <Section 
                        field={field} 
                        editable={editable} 
                        getFields={getStructure}
                    />
                {/if}
            {/each}

            {#if fields.length == 0}
                <p class="text-muted-foreground">No fields found</p>
            {/if}

            {#if !editable}
                <MathScoutingSubmit />
            {/if}
        </form>
    {/if}
</div>


<AddFieldDialog season_uuid={season_uuid} gamePieces={gamePieces} getStructure={getStructure} />
<AddSectionDialog season_uuid={season_uuid} getStructure={getStructure} />