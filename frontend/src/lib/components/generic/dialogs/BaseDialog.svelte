<!-- 
@component
Generic dialog container that automatically switches between a dialog and a drawer on larger and smaller screens, respectively

Props:
    - `title` (`string`) - The title of the dialog
    - `description` (`string`) - The description of the dialog
    - `open` (`boolean`) - If the dialog is open or not
    - `onOpenChange` (`() => void`) - The function to call when the open state changes
    - `children` (`Snippet`) - Child components to display in the dialog

-->
<script lang="ts">
	import { browser } from "$app/environment";
	import { onMount, type Snippet } from "svelte";

	import * as Dialog from "$lib/components/ui/dialog/index.js";
    import * as Sheet from "$lib/components/ui/sheet/index.js";


    interface Props {
        title?: string
        description?: string
        open?: boolean
        onOpenChange?: () => void
        children: Snippet
    }
    let { 
        title = "", 
        description = "", 
        open = $bindable(false), 
        onOpenChange = $bindable(() => {}), 
        children 
    }: Props = $props();

    let isDesktop: boolean = $state(false);

    /**
     * Checks the current screen size. If it's smaller than tailwind-css' md breakpoint, return false
     */
    function checkScreenSize(): void {
        isDesktop = window.innerWidth >= 768;
    }

    /**
     * Check the screen size when the component initalizes
     * 
     * If the browser window resizes, check the screen size again
     */
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
