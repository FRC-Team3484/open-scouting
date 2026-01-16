<script lang="ts">
	import { createCustomEventDialogOpen } from "$lib/stores/dialog";
	import BaseDialog from "./BaseDialog.svelte";

	
</script>

<BaseDialog title={"Create Custom Event"} description={"Create a cuustom event when an event is missing on The Blue Alliance"} bind:open={$createCustomEventDialogOpen}>
    <p>create custom event</p>
</BaseDialog>