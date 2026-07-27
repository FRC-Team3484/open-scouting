<!-- 
@component
Management page for repairs on the admin page
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";

    import * as Card from "$lib/components/ui/card/index.js";

	import type { RepairResponse } from "$lib/api/model";
	import { getRepairsRepairsGetGet } from "$lib/api/repairs/repairs";


    let repairs: RepairResponse[] = [];

    async function getRepairs() {
        await getRepairsRepairsGetGet().then((response) => {
            if (response.status === 200) {
                repairs = response.data
            } else {
                toast.error("Failed to get repairs", { duration: 5000 });
            }
        })
    }

    onMount(() => {
        getRepairs();
    })
</script>

<div class="flex flex-col gap-2">
    <Card.Root class="w-auto">
        <Card.Header>
            <Card.Title>Server Repairs</Card.Title>
            <Card.Description>Fix broken database relations for content on the server</Card.Description>
        </Card.Header>

        <Card.Content>
            <p>Found {repairs.length} repairs</p>
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Content>
            <div class="flex flex-col gap-2">

            </div>
        </Card.Content>
    </Card.Root>
</div>