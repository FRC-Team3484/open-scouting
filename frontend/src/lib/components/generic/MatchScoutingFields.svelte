<script lang="ts">
	import { apiFetch } from "$lib/utls/api";
	import { onMount } from "svelte";
	import Skeleton from "../ui/skeleton/skeleton.svelte";

    let fields = [];

    export let season_uuid: string = "";
    export let editable: boolean = false;

    async function get_fields() {
        if (!season_uuid) return;
        fields = await apiFetch(`/fields/season/${season_uuid}`);
    }

    onMount(async () => {
        get_fields();
    });
</script>

<div class="flex flex-col gap-4">
    {#if season_uuid === ""}
        <Skeleton class="w-128 h-32" />
        <Skeleton class="w-128 h-32" />
        <Skeleton class="w-128 h-32" />
    {:else}
        {#each fields as field}
            <p>field</p>
        {/each}
    {/if}
</div>