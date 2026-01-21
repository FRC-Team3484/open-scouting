<script lang="ts">
	import * as Field from "$lib/components/ui/field";
	import Input from "$lib/components/ui/input/input.svelte";
	import * as Select from "$lib/components/ui/select";
	import * as Dialog from "$lib/components/ui/dialog";

	import { createCustomEventDialogOpen } from "$lib/stores/dialog";
	import { apiFetch } from "$lib/utils/api";
	import { onMount } from "svelte";
	import BaseDialog from "./BaseDialog.svelte";
	import { get } from "svelte/store";
	import Button from "$lib/components/ui/button/button.svelte";

	let seasons: any = $state([]);
	let selectedSeasonLabel = $derived(
		seasons.find((s) => s.uuid === selectedSeason)?.name ?? "Select Season"
	)
	const eventTypes = [
		{ value: "district", label: "District" },
		{ value: "regional", label: "Regional" },
		{ value: "preseason", label: "Preseason" },
		{ value: "offseason", label: "Offseason" },
		{ value: "other", label: "Other" },
	]
	let selectedEventTypeLabel = $derived(
		eventTypes.find((et) => et.value === eventType)?.label ?? "Select Event Type"
	)

    let selectedSeason = $state("");
	let eventName = $state("");
	let eventType = $state("");
	let eventCity = $state("");
	let eventCountry = $state("");
	let eventStartDate = $state("");
	let eventEndDate = $state("");

	async function getYears() {
		const response = await apiFetch(`/seasons`);

        seasons = response;
        const active_year = seasons.find(year => year.active);
        if (active_year) {
            selectedSeason = {year: active_year.year, name: active_year.name, uuid: active_year.uuid};
        }
	}

	async function createCustomEvent(event: Event) {
		event.preventDefault();

		const form = event.currentTarget as HTMLFormElement;
		const formData = new FormData(form);

		formData.append("event_code", crypto.randomUUID());

		console.log(formData)

		const response = await apiFetch(`/event/custom/${selectedSeason}/create`, {
			method: "POST",
			data: formData,
		});

		console.log(response);
	}

	onMount(async () => {
		await getYears();
	})
</script>

<BaseDialog title={"Create Custom Event"} description={"Create a cuustom event when an event is missing on The Blue Alliance"} bind:open={$createCustomEventDialogOpen}>
	<form method="post" onsubmit={createCustomEvent} class="flex flex-col gap-4">
		<Field.Group class="gap-4">
			<Field.Set class="flex flex-col gap-2">
				<Field.Label>Season</Field.Label>
				<Select.Root type="single" name="season" label="Season" required bind:value={selectedSeason}>
					<Select.Trigger>
						{selectedSeasonLabel}
					</Select.Trigger>
					<Select.Content>
						<Select.Label>Seasons</Select.Label>
						{#each seasons as season}
							<Select.Item value={season.uuid} label={season.year + " - " + season.name} />
						{/each}
					</Select.Content>
				</Select.Root>
				<Field.Description>The season for when the event is held</Field.Description>

				<Field.Label>Event Name</Field.Label>
				<Input type="text" name="event_name" placeholder="Event Name" bind:value={eventName} />
				<Field.Description>The name of the event</Field.Description>

				<Field.Label>Event Type</Field.Label>
				<Select.Root type="single" name="event_type" label="Event Type" required bind:value={eventType}>
					<Select.Trigger>
						{selectedEventTypeLabel}
					</Select.Trigger>
					<Select.Content>
						<Select.Label>Event Types</Select.Label>
						{#each eventTypes as type}
							<Select.Item value={type.value} label={type.label} />
						{/each}
					</Select.Content>
				</Select.Root>
				<Field.Description>The type of event</Field.Description>
			</Field.Set>

			<Field.Set class="flex flex-col gap-2">
				<Field.Label>Country</Field.Label>
				<Input type="text" name="event_country" placeholder="Country" bind:value={eventCountry} />
				<Field.Description>The country where the event is located</Field.Description>

				<Field.Label>City</Field.Label>
				<Input type="text" name="event_city" placeholder="City" bind:value={eventCity} />
				<Field.Description>The city where the event is located</Field.Description>

				<Field.Label>Start Date</Field.Label>
				<Input type="date" name="event_start_date" placeholder="Start Date" bind:value={eventStartDate} />
				<Field.Description>The start date of the event</Field.Description>

				<Field.Label>End Date</Field.Label>
				<Input type="date" name="event_end_date" placeholder="End Date" bind:value={eventEndDate} />
				<Field.Description>The end date of the event</Field.Description>
			</Field.Set>
		</Field.Group>

		<Dialog.Footer>
			<Button type="button" variant="outline">Cancel</Button>
			<Button type="submit">Create Event</Button>
		</Dialog.Footer>
	</form>
</BaseDialog>