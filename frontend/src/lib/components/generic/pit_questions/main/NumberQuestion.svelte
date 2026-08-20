<!-- 
@component
The pit scouting question for a number

Props:
    - `pit` (`PitScoutingData`) - The parent pit for this question
    - `question` (`SeasonPitScoutingQuestion`) - The question
    - `answers` (`PitScoutingAnswer[]`) - Any answers for this question
    - `user` (`UserResponse | null`) - The user from the parent
-->
<script lang="ts">
	import Button from '$lib/components/ui/button/button.svelte';
	import Input from '$lib/components/ui/input/input.svelte';
	
	import {
		db,
		type PitScoutingAnswer,
		type PitScoutingData,
		type SeasonPitScoutingQuestion
	} from '$lib/utils/db';
	import BaseQuestion from './BaseQuestion.svelte';
	import { type UserResponse } from '$lib/api/model';

	interface Props {
		pit: PitScoutingData;
		question: SeasonPitScoutingQuestion;
		answers: PitScoutingAnswer[];
		user: UserResponse | null;
	}
	let { pit, question, answers, user }: Props = $props();

	let value = $state(0);
	let resetBase;

	/**
	 * Add the typed answer to this question
	 */
	async function addAnswer() {
		const newAnswer = {
			uuid: crypto.randomUUID(),
			value: value,
			username: user?.username ?? 'guest',
			field_uuid: question.uuid,
			created_at: new Date().toISOString()
		};
		await db.pit_scouting.update(pit.uuid, {
			answers: [...pit.answers, newAnswer],
			synced: false
		});

		value = 0;
		resetBase();
	}
</script>

<BaseQuestion {question} {answers} bind:reset={resetBase}>
	<div class="flex flex-row items-center gap-2">
		<Input type="number" placeholder={question.name} bind:value />
		<Button onclick={addAnswer}>Save</Button>
	</div>
</BaseQuestion>
