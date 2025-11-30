<script lang="ts">
	import { Button } from "$lib/components/ui/button";
    import * as Drawer from "$lib/components/ui/drawer";
	import { X } from "phosphor-svelte";

    let { title, description } = $props();
</script>

<div class="flex flex-row gap-2 justify-between my-4">
    <div class="flex flex-col gap-2">
        <Drawer.Title>{title}</Drawer.Title>
        <Drawer.Description>{description}</Drawer.Description>
    </div>

    <Drawer.Close>
        <Button variant="outline" size="icon"><X weight="bold"/></Button>
    </Drawer.Close>
</div>