<script lang="ts">
    import * as Card from "$lib/components/ui/card";
	import { CheckCircle, X } from "phosphor-svelte";
    import Button from "../ui/button/button.svelte";
	import Dialog from "../generic/Dialog.svelte";

    let operations = [{name: "", description: "", data: {}, operation: ""}]; // {name: "", description: "", data: {}, operation: ""}

    let showApplyDialog = false;
    let showClearDialog = false;

    function handleCancel() {
        showApplyDialog = false;
        showClearDialog = false;
    }

    function applyAll() {
        
        showApplyDialog = false;
    }

    function clearAll() {
        operations = [];

        showClearDialog = false;
    }
</script>

<Card.Root class="w-auto min-w-64 mt-4">
    <Card.Content>
        <div class="flex flex-col gap-4">
            {#if operations.length === 0}
                <p>No admin operations yet</p>

            {:else}
                <p>Admin operations</p>
                <div class="flex flex-row gap-2">
                    <Button variant="default" onclick={() => {showApplyDialog = true}}><CheckCircle weight="bold"/> Apply</Button>
                    <Button variant="destructive" onclick={() => {showClearDialog = true}}><X weight="bold"/> Clear</Button>
                </div>

                {#each operations as operation}
                    <div class="flex flex-row gap-2 justify-between items-center border-1 border-accent rounded-lg p-2">
                        <div class="flex flex-row gap-2 items-center flex-wrap text-left">
                            <p>{operation.name}</p>
                            <p class="text-sm opacity-80">{operation.description}</p>
                        </div>

                        <div class="flex flex-row gap-2">
                            <Button variant="destructive" size="icon" onclick={() => {operations = operations.filter(op => op.name !== operation.name)}}><X weight="bold"/></Button>
                        </div>
                    </div>
                {/each}
            {/if}
            
        </div>
    </Card.Content>
</Card.Root>

<Dialog bind:open={showApplyDialog} 
    title="Apply all admin operations" 
    description="Are you sure you want to apply all admin operations? Make sure that you understand the consequences of the operations you may be applying, as they are irreversible." 
    buttons={[
        { label: "Cancel", variant: "cancel", onClick: handleCancel },
        { label: "Apply", variant: "action", onClick: applyAll },
    ]}
/>

<Dialog bind:open={showClearDialog} 
    title="Clear all admin operations" 
    description="Are you sure you want to clear all admin operations? This cannot be undone." 
    buttons={[
        { label: "Cancel", variant: "cancel", onClick: handleCancel },
        { label: "Clear", variant: "action", onClick: clearAll },
    ]}
/>
