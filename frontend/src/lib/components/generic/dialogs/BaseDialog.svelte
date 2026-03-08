<script lang="ts">
	import { browser } from "$app/environment";
	import { onMount } from "svelte";
	import * as Dialog from "$lib/components/ui/dialog/index.js";
    import * as Sheet from "$lib/components/ui/sheet/index.js";

    let { title = "", description = "", open = $bindable(false), onOpenChange = $bindable(() => {}), children } = $props();

    let isDesktop = $state(false);

    function checkScreenSize() {
        // tailwind-css' md breakpoint is 768 pixels
        isDesktop = window.innerWidth >= 768;
    }

    onMount(() => {
        if (browser) {
            checkScreenSize();
            window.addEventListener("resize", checkScreenSize);
            return () => window.removeEventListener("resize", checkScreenSize);
        }
    })
</script>

{#snippet content()}
    <div class="flex flex-col gap-2 overflow-y-scroll max-h-[80vh]">
        {@render children()}
    </div>
{/snippet}

{#if isDesktop}
    <Dialog.Root bind:open onOpenChangeComplete={onOpenChange}>
        <Dialog.Content>
            <Dialog.Header>
                <Dialog.Title>{title}</Dialog.Title>
                <Dialog.Description>{description}</Dialog.Description>
            </Dialog.Header>

            {@render content()}

        </Dialog.Content>
    </Dialog.Root>
{:else}
    <Sheet.Root bind:open onOpenChangeComplete={onOpenChange}>
        <Sheet.Content class="max-h-[80vh] overflow-y-scroll lg:mx-64 border-1 p-4 rounded-t-lg" side="bottom">
            <Sheet.Header>
                <Sheet.Title>{title}</Sheet.Title>
                <Sheet.Description>{description}</Sheet.Description>
            </Sheet.Header>
            
            {@render content()}
        </Sheet.Content>
    </Sheet.Root>
{/if}
