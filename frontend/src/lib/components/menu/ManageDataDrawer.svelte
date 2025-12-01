<script lang="ts">
    import icon_rounded from "$lib/assets/icon_rounded.png"
    import DrawerHeader from "$lib/components/generic/drawers/DrawerHeader.svelte";
    import { PUBLIC_VERSION } from "$env/static/public";

    import * as Drawer from "$lib/components/ui/drawer";
	import { FloppyDisk } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import { Separator } from "../ui/separator";
	import { onMount } from "svelte";

    let { setState } = $props();

</script>

<Drawer.NestedRoot>
    <Drawer.Trigger>
        <Button variant="outline" class="w-full"><FloppyDisk weight="bold" /> Manage Local Data</Button>
    </Drawer.Trigger>
    <Drawer.Portal>
        <Drawer.Content class="h-auto lg:mx-64 border-1 p-4">
            <DrawerHeader title="Manage Local Data" description="View and manage data stored locally on your device" />
            <Separator orientation="horizontal" />


        </Drawer.Content>
        <Drawer.Overlay />
    </Drawer.Portal>
</Drawer.NestedRoot>