<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { apiFetch } from "$lib/utls/api";
	import { CheckCircle, PlusCircle, X } from "phosphor-svelte";
	import { onMount } from "svelte";
	import Separator from "../ui/separator/separator.svelte";
    import Button from "../ui/button/button.svelte";

    let seasons = [];

    onMount(async () => {
        seasons = await apiFetch(`/seasons`);
    })
</script>

<Card.Root class="w-auto min-w-64">
    <Card.Header>
        <Card.Title>Seasons</Card.Title>
        <Card.Description>Manage seasons</Card.Description>
    </Card.Header>

    <Card.Content>
        <div class="flex flex-col gap-4">
            {#each seasons as season}
                <Card.Root>
                    <Card.Content>
                        <div class="flex flex-row gap-2 items-center">
                            {#if season.active}
                                <CheckCircle weight="bold" />
                            {/if}
                            <p>{season.year}</p>
                            <p>{season.label}</p>
                            <Separator orientation="vertical" />
                            <Button size="icon" variant="destructive" onclick={() => {}}><X weight="bold"/></Button>
                        </div>
                    </Card.Content>
                </Card.Root>
            {/each}

            <Button><PlusCircle weight="bold" /> Add Season</Button>
        </div>
    </Card.Content>
</Card.Root>