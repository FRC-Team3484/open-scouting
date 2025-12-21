<script lang="ts">
    import Separator from "../ui/separator/separator.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import { Button } from "$lib/components/ui/button/index.js";
	import { PlusCircle } from "phosphor-svelte";

	import AddPitScoutingQuestionDialog from "./dialogs/AddPitScoutingQuestionDialog.svelte";
	import { addPitScoutingQuestionDialogOpen } from "$lib/stores/dialog";

    let { season_uuid, year, editable } = $props();

    async function getQuestions() {}
</script>

{#if editable}
    <div class="flex flex-col gap-4">
        <Separator orientation="horizontal" />

        <Card.Root class="w-auto min-w-64">
            <Card.Content>
                <Button onclick={() => {addPitScoutingQuestionDialogOpen.set(true);}}><PlusCircle weight="bold" /> Add Question</Button>
            </Card.Content>
        </Card.Root>
    </div>
{/if}

<AddPitScoutingQuestionDialog getQuestions={getQuestions} seasonUuid={season_uuid}/>