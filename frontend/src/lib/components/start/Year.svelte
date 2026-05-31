<!-- 
@component
The year selector for the index page

TODO: Get the years locally, instead of from the server

Props:
    - `handleNavigate` (`(nextPage: string) => void`) - The function for changing the page
    - `setYear` (`(year: number) => void`) - The function for setting the year
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { ArrowRightIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
	import Label from "../ui/label/label.svelte";
	import Button from "../ui/button/button.svelte";

	import { getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";
	import type { SeasonResponse } from "$lib/api/model";


    interface Props {
        handleNavigate: (nextPage: string) => void;
        setYear: (year: number) => void;
    }
    let { handleNavigate, setYear }: Props = $props();

    let years: SeasonResponse[] = $state([]);
    let selected_year: {year: number, name: string, uuid: string} | null = $state(null);

    /**
     * Get all years from the server
     * 
     * TODO: Should this get the locally stored years?
     */
    onMount(async () => {
        await getSeasonsSeasonsGet().then((response) => {
            years = response.data
            const active_year = years.find(year => year.active);
            if (active_year) {
                selected_year = {year: active_year.year, name: active_year.name, uuid: active_year.uuid};
            }
        });
    });
</script>

<Card.Card class="text-left mt-4 max-w-64 w-full">
    <Card.Header>
        <Card.Title>Season</Card.Title>
        <Card.Description>Choose a season to scout or view data for</Card.Description>
    </Card.Header>

    {#if selected_year}
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
            <Button onclick={() => {setYear(selected_year.year); handleNavigate("events")}}><ArrowRightIcon weight="bold" /> Continue</Button>
        </Card.Footer>
    {/if}
</Card.Card>