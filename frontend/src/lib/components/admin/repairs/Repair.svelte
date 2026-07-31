<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";

	import type { RepairResponse } from "$lib/api/model";
	import Badge from "../../ui/badge/badge.svelte";
	import { TrashIcon } from "phosphor-svelte";
	import { Button } from "$lib/components/ui/button";


    interface Props {
        repair: RepairResponse
        selectedRepairs?: RepairResponse[]
    }
    let { repair, selectedRepairs = $bindable([]) }: Props = $props();
</script>

<Card.Root>
    <Card.Content>
        <div class="flex flex-row gap-2 items-center">
            <input type="checkbox" bind:group={selectedRepairs} value={repair} />

            <div class="flex flex-col gap-2 items-start">
                <div class="flex flex-row gap-2 flex-wrap">
                    <Badge>{repair.data_type.charAt(0).toUpperCase() + repair.data_type.replaceAll("_", " ").slice(1)}</Badge>
                    <p class="text-left">{repair.name}</p>
                </div>
                <p class="text-muted-foreground">Data Created: {new Date(repair.data_created_at).toLocaleString()}</p>
                <div class="flex flex-row gap-2 flex-wrap">
                    <Button size="sm" variant="destructive"><TrashIcon weight="bold" /> Delete Content</Button>
                </div>
            </div>
        </div>
    </Card.Content>
</Card.Root>