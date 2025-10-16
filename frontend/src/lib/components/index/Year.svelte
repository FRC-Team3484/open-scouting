<script lang="ts">
	import { apiFetch } from "$lib/utls/api";
	import { onMount } from "svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
	import Label from "../ui/label/label.svelte";
	import Button from "../ui/button/button.svelte";
	import { ArrowRight } from "phosphor-svelte";

    let years: any = null;
    let selected_year = {year: null, name: null, uuid: null};

    onMount(async () => {
        const response = await apiFetch(`/seasons`);

        years = response;
        const active_year = years.find(year => year.active);
        if (active_year) {
            selected_year = {year: active_year.year, name: active_year.name, uuid: active_year.uuid};
        }
    });

    export let handleNavigate: (nextPage: string) => void;
    export let setYear: (year: number) => void;
</script>

<Card.Card class="w-auto min-w-64">
    <Card.Header>
        <Card.Title>Season</Card.Title>
        <Card.Description>Choose a season to scout or view data for</Card.Description>
    </Card.Header>

    <Card.Content>
        <Label for="year">Season</Label>
        <Select.Root type="single" id="year" name="year" bind:value={selected_year}>
            <Select.Trigger>
                {selected_year.year}
            </Select.Trigger>
            <Select.Content>
                <Select.Label>Seasons</Select.Label>
                {#each years as year}
                    <Select.Item value={{"year":year.year, "name":year.name, "uuid":year.uuid}} label={year.year} />
                {/each}
            </Select.Content>
        </Select.Root>
    </Card.Content>

    <Card.Footer>
        <Button onclick={() => {setYear(selected_year.year); handleNavigate("events")}}><ArrowRight weight="bold" /> Continue</Button>
    </Card.Footer>
</Card.Card>