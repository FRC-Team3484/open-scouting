<!-- 
@component
Wrapper component for rendering each authentication page with a consistent style and header text

Props:
    - `title` (`string`) - The title of the page
    - `icon` (`Snippet`) - The icon to display
    - `content` (`Snippet`) - The content of the page
    - `onBackButtonClick` (`() => void`) - The function to call when the back button is clicked
    - `onCancelButtonClick` (`() => void`) - The function to call when the cancel button is clicked
-->
<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
	import { ArrowLeftIcon, XCircleIcon } from "phosphor-svelte";
	import type { Snippet } from "svelte";
	import { slide } from "svelte/transition";


    interface Props {
        title: string
        icon?: Snippet
        content?: Snippet
        onBackButtonClick?: () => void
        onCancelButtonClick?: () => void
    }
    let { title, icon, content, onBackButtonClick, onCancelButtonClick }: Props = $props();
</script>

<div class="flex flex-col gap-2 text-left" transition:slide>
    {#if onBackButtonClick}
        <Button variant="outline" size="sm" onclick={onBackButtonClick} class="w-fit"><ArrowLeftIcon weight="bold" /> Back</Button>
    {/if}

    {#if onCancelButtonClick}
        <Button variant="outline" size="sm" onclick={onCancelButtonClick} class="w-fit"><XCircleIcon weight="bold" /> Cancel</Button>
    {/if}

    <div class="flex flex-row gap-2 items-center">
        {@render icon?.()}
        <p class="font-bold">{title}</p>
    </div>

    {@render content?.()}
</div>