<script lang="ts">
	import { onMount } from "svelte";
	import { FolderPlus, PlusCircle } from "phosphor-svelte";

    import { addFieldDialogOpen, addSectionDialogOpen } from "$lib/stores/dialog";
    import { apiFetch } from "$lib/utls/api";

	import Skeleton from "../ui/skeleton/skeleton.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import Button from "../ui/button/button.svelte";
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
	import { db } from "$lib/utls/db";

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
    let gamePieces = $state([]);

    type ChoiceType = {id: string; name: string }[];
    let choices: ChoiceType[] = [];

    let { season_uuid, editable } = $props();

    async function getStructure() {
        fields = await apiFetch(`/fields/season/${season_uuid}`);
    }

    async function getGamePieces() {
        gamePieces = await apiFetch(`/gamepieces/season/${season_uuid}`);
    }

    async function submit(event: Event) {
        event.preventDefault();

        const form = event.currentTarget as HTMLFormElement;
        const formData = new FormData(form);

        await db.match_scouting.add({
            uuid: crypto.randomUUID(),
            data: Object.fromEntries(formData),
            synced: false
        });
    }

    onMount(async () => {
        while (!season_uuid) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        getStructure();
        getGamePieces();
    });
</script>

<div class="flex flex-col gap-4">
    {#if season_uuid === ""}
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
                    </div>
                </Card.Content>
            </Card.Root>
        {/if}
        
        <form method="post" onsubmit={submit}>
            {#each fields as field (field.uuid)}
                {#if field.field_type === "string"}
                    <StringField field={field} editable={editable} getFields={getStructure}/>
                {:else if field.field_type === "large_number"}
                    <LargeNumberField field={field} editable={editable} getFields={getStructure}/>
                {:else if field.field_type === "small_number"}
                    <SmallNumberField field={field} editable={editable} getFields={getStructure}/>
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

            {#if !editable}
                <MathScoutingSubmit />
            {/if}
        </form>
    {/if}
</div>


<AddFieldDialog season_uuid={season_uuid} gamePieces={gamePieces} getStructure={getStructure} />
<AddSectionDialog season_uuid={season_uuid} getStructure={getStructure} />