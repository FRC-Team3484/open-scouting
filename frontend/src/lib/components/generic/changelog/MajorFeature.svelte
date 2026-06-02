<!-- 
@component
Small highlighted section with icon for showcasing a major feature

Props:
    - `icon` (`Snippet`) - The component to use as the icon
    - `text` (`string`) - The text of the feature
-->
<script lang="ts">
	import type { Snippet } from "svelte";


    interface Props {
        icon: Snippet
        text: string
    }
    let { icon, text }: Props = $props();
</script>

<div class="flex flex-col gap-2 justify-center rounded-sm shadow-sm bg-secondary border-card-foreground border p-2">
    <div class="flex flex-row gap-2 items-center">
        {@render icon?.()}
        <p class="text-sm">{text}</p>
    </div>
</div>