<script lang="ts">
	import { apiFetch } from "$lib/utls/api";
	import { onMount } from "svelte";
	import Skeleton from "../ui/skeleton/skeleton.svelte";
	import { ArrowLeft, ArrowRight, FolderPlus, Minus, Pencil, Plus, PlusCircle, Trash, X } from "phosphor-svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";
    import * as Field from "$lib/components/ui/field/index.js";
	import Input from "../ui/input/input.svelte";
	import * as Select from "$lib/components/ui/select/index.js";
	import Checkbox from "../ui/checkbox/checkbox.svelte";
	import { get } from "svelte/store";
	import { Root } from "../ui/alert";
	import { Trigger } from "../ui/alert-dialog";
	import { json } from "@sveltejs/kit";
	import StringField from "./fields/StringField.svelte";
	import LargeNumberField from "./fields/LargeNumberField.svelte";
	import SmallNumberField from "./fields/SmallNumberField.svelte";
	import BooleanField from "./fields/BooleanField.svelte";
	import ChoiceField from "./fields/ChoiceField.svelte";
	import MultipleChoiceField from "./fields/MultipleChoiceField.svelte";
	import BaseSection from "./fields/BaseSection.svelte";
	import Section from "./fields/Section.svelte";
	import AddSectionDialog from "./dialogs/AddSectionDialog.svelte";
	import AddFieldDialog from "./dialogs/AddFieldDialog.svelte";

    let fields = $state([]);
    let gamePieces = $state([]);

    type ChoiceType = {id: string; name: string }[];
    let choices: ChoiceType[] = [];

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

    let { season_uuid, editable } = $props();

    let openAddSectionDialog = $state(false);
    let openAddFieldDialog = $state(false);

    async function getStructure() {
        fields = await apiFetch(`/fields/season/${season_uuid}`);

        console.log("fields structure:", fields);
    }

    async function getGamePieces() {
        gamePieces = await apiFetch(`/gamepieces/season/${season_uuid}`);
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
        <Card.Root class="w-auto min-w-64">
            <Card.Content>
                <div class="flex flex-col gap-4">
                    <Button onclick={() => openAddFieldDialog = true}><PlusCircle weight="bold" /> Add Field</Button>
                    <Button onclick={() => openAddSectionDialog = true}><FolderPlus weight="bold" /> Add Section</Button>
                </div>
            </Card.Content>
        </Card.Root>

        <!-- {#each fields as field}
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
            {/if}
        {/each} -->

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
                <Section field={field} editable={editable} getFields={getStructure}/>
            {/if}
        {/each}
    {/if}
</div>

<AddFieldDialog bind:open={openAddFieldDialog} season_uuid={season_uuid} gamePieces={gamePieces} getStructure={getStructure} />
<AddSectionDialog bind:open={openAddSectionDialog} season_uuid={season_uuid} getStructure={getStructure} />