<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
	import { DotsThree, Pencil, Trash } from "phosphor-svelte";

    let { question, editable = false, getQuestions = () => {}, children } = $props();

    async function deleteQuestion() {}
    function editQuestion() {}
</script>

<Card.Root class="w-auto min-w-64">
    <Card.Header>
        <div class="flex flex-row gap-2 items-center justify-between flex-wrap">
            <div class="flex flex-row gap-2 items-center">
                <p>
                    {question.name}
                </p>
                {#if editable}
                    <p class="text-sm opacity-80">{question.field_type}</p>
                {/if}
            </div>

            {#if editable}
                <DropdownMenu.Root>
                    <DropdownMenu.Trigger>
                        <Button size="icon" variant="outline"><DotsThree weight="bold" /></Button>
                    </DropdownMenu.Trigger>

                    <DropdownMenu.Content class="w-56" align="start">
                        <DropdownMenu.Label>Field Options</DropdownMenu.Label>
                        <DropdownMenu.Group>
                            <DropdownMenu.Item onclick={editQuestion}><Pencil weight="bold" /> Edit</DropdownMenu.Item>
                            <DropdownMenu.Item onclick={deleteQuestion}><Trash weight="bold" /> Delete</DropdownMenu.Item>
                        </DropdownMenu.Group>
                    </DropdownMenu.Content>
                </DropdownMenu.Root>
            {/if}
        </div>
    </Card.Header>

    <Card.Content>
        {@render children()}
    </Card.Content>
</Card.Root>