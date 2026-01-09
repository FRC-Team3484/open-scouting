<script lang="ts">
    import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
	import { Flask } from "phosphor-svelte";

    let { size = "md" } = $props();
</script>

<AlertDialog.Root>
    <AlertDialog.Trigger>
        <div class={`flex flex-row gap-1 items-center text-amber-500/80 bg-amber-500/30 rounded-md border border-amber-700 hover:bg-amber-500/20 transition-colors ${size === "md" ? "px-4 py-2" : "px-2 py-1"}`}>
            <Flask weight="bold" />
            <p class={`${size === "md" ? "text-md" : "text-sm"} font-bold`}>Experimental build</p>
        </div>
    </AlertDialog.Trigger>

    <AlertDialog.Content>
        <AlertDialog.Title>Open Scouting is experimental</AlertDialog.Title>
        <AlertDialog.Description>This is an experimental build. It may contain bugs or other issues. Any data added to the database will be cleared before stable, so do not use this build for real competition scouting.</AlertDialog.Description>
        <AlertDialog.Footer>
            <AlertDialog.Cancel type="button">Close</AlertDialog.Cancel>
        </AlertDialog.Footer>
    </AlertDialog.Content>
</AlertDialog.Root>