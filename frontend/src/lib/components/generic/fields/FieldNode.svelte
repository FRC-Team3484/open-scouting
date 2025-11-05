<script lang="ts">
    import FieldNode from "./FieldNode.svelte";

	export let node;
	export let editable = false;
	export let getStructure;

	// import { dndzone } from '@thisux/sveltednd';

	function handleDrop({ detail }) {
		// Update local order + persist via API
	}
</script>

<div>
	{#if node.type === 'section'}
		<div class="p-2 border rounded mb-2">
			<h3 class="font-bold">{node.name}</h3>

			{#each node.children as child (child.id)}
				<FieldNode {child} editable={editable} {getStructure} />
			{/each}
		</div>
	{:else if node.type === 'field'}
		<!-- Render your field types here -->
		<p>{node.name}</p>
	{/if}
</div>
