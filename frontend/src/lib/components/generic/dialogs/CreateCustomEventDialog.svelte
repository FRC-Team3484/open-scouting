<script lang="ts">
	import { onMount } from "svelte";
	import { superForm } from "sveltekit-superforms";
	import { zod4Client } from "sveltekit-superforms/adapters";
	import { toast } from "svelte-sonner";

	import Input from "$lib/components/ui/input/input.svelte";
	import * as Select from "$lib/components/ui/select";
	import * as Dialog from "$lib/components/ui/dialog";
	import * as Form from "$lib/components/ui/form";
	import Label from "$lib/components/ui/label/label.svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";
	
	import { CreateCustomEventEventCustomSeasonUuidCreatePostBody } from "$lib/zod/events/events";
	import { getSeasonsSeasonsGet } from "$lib/api/seasons/seasons";
	import type { SeasonResponse } from "$lib/api/model";
	import { createCustomEventEventCustomSeasonUuidCreatePost } from "$lib/api/events/events";

	import BaseDialog from "./BaseDialog.svelte";
	import { db } from "$lib/utils/db";

	let { open = $bindable(false) } = $props();

	let seasons: SeasonResponse[] = $state([]);
	let selectedSeasonLabel: string = $derived(
		seasons.find((s) => s.uuid === $formData.season_uuid)?.name ?? "Select Season"
	)
	const eventTypes = [
		{ value: "district", label: "District" },
		{ value: "regional", label: "Regional" },
		{ value: "preseason", label: "Preseason" },
		{ value: "offseason", label: "Offseason" },
		{ value: "other", label: "Other" },
	]
	let selectedEventTypeLabel = $derived(
		eventTypes.find((et) => et.value === $formData.event_type)?.label ?? "Select Event Type"
	)

	const defaultValues = {
		season_uuid: "",
		event_code: "",
		event_name: "",
		event_type: "",
		event_city: "",
		event_country: "",
		event_start_date: "",
		event_end_date: "",
	}

	const form = superForm(defaultValues, {
		SPA: true,
		validators: zod4Client(CreateCustomEventEventCustomSeasonUuidCreatePostBody),
		async onUpdate({ form }) {
			if (form.valid) {
				form.data.event_code = crypto.randomUUID();

				await createCustomEventEventCustomSeasonUuidCreatePost(form.data.season_uuid, form.data).then(async (response) => {
					if (response.status !== 200) {
						toast.error("Failed to create event", { duration: 5000 });
					} else {
						await db.event.put({
							uuid: response.data.uuid,
							year: seasons.find((s) => s.uuid === form.data.season_uuid).year,
							event_code: form.data.event_code,
							name: form.data.event_name,
							type: form.data.event_type,
							city: form.data.event_city,
							country: form.data.event_country,
							start_date: form.data.event_start_date,
							end_date: form.data.event_end_date,
							custom: true,
							fetch_time: new Date()
						});

						open = false;
						toast.success("Custom event created", { duration: 5000 });
					}
				})
			}
		}
	});

	const { form: formData, enhance } = form

	async function getYears() {
		const response = (await getSeasonsSeasonsGet()).data

        seasons = response;
        const active_year = seasons.find(year => year.active);
        if (active_year) {
            $formData.season_uuid = active_year.uuid;
        }
	}

	onMount(async () => {
		await getYears();
	})
</script>

<BaseDialog title={"Create Custom Event"} description={"Create a custom event when an event is missing on The Blue Alliance"} bind:open={open}>
	<form method="post" use:enhance class="flex flex-col gap-4">
		<Form.Field {form} name="season_uuid">
			<Form.Control>
				{#snippet children({ props })}
					<Label>Season</Label>
					<Select.Root type="single" name="season" required bind:value={$formData.season_uuid}>
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
				{/snippet}
			</Form.Control>
			<Form.Description>The season for when the event is held</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Form.Field {form} name="event_name">
			<Form.Control>
				{#snippet children({ props })}
					<Label>Name</Label>
					<Input {...props} bind:value={$formData.event_name} />
				{/snippet}
			</Form.Control>
			<Form.Description>The name of the event</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Form.Field {form} name="event_type">
			<Form.Control>
				{#snippet children({ props })}
					<Label>Type</Label>
					<Select.Root type="single" name="event_type" required bind:value={$formData.event_type}>
						<Select.Trigger>
							{selectedEventTypeLabel}
						</Select.Trigger>
						<Select.Content>
							<Select.Label>Event Types</Select.Label>
							{#each eventTypes as eventType}
								<Select.Item value={eventType.value} label={eventType.label} />
							{/each}
						</Select.Content>
					</Select.Root>
				{/snippet}
			</Form.Control>
			<Form.Description>The type of the event</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Separator orientation="horizontal" />

		<Form.Field {form} name="event_country">
			<Form.Control>
				{#snippet children({ props })}
					<Label>Country</Label>
					<Input {...props} bind:value={$formData.event_country} />
				{/snippet}
			</Form.Control>
			<Form.Description>The country of the event</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Form.Field {form} name="event_city">
			<Form.Control>
				{#snippet children({ props })}
					<Label>City</Label>
					<Input {...props} bind:value={$formData.event_city} />
				{/snippet}
			</Form.Control>
			<Form.Description>The city of the event</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Form.Field {form} name="event_start_date">
			<Form.Control>
				{#snippet children({ props })}
					<Label>Start Date</Label>
					<Input {...props} type="date" bind:value={$formData.event_start_date} />
				{/snippet}
			</Form.Control>
			<Form.Description>The start date of the event</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Form.Field {form} name="event_end_date">
			<Form.Control>
				{#snippet children({ props })}
					<Label>End Date</Label>
					<Input {...props} type="date" bind:value={$formData.event_end_date} />
				{/snippet}
			</Form.Control>
			<Form.Description>The end date of the event</Form.Description>
			<Form.FieldErrors />
		</Form.Field>

		<Separator orientation="horizontal" />

		<Dialog.Footer>
			<Form.Button type="submit">Create</Form.Button>
			<Dialog.Close>
				<Form.Button type="button" variant="outline">Cancel</Form.Button>
			</Dialog.Close>
		</Dialog.Footer>
	</form>
</BaseDialog>