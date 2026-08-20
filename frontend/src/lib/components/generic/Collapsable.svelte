<!-- 
@component
A collapsable div with content, that uses CSS to hide content instead of a regular Svelte {#if}

This allows for slide animating the visibity of content without unrendering it

Props:
    - `open` (`boolean`) - Whether the content is open
    - `children` (`Snippet`) - Child components to display
-->
<script lang="ts">
	import type { Snippet } from "svelte";


    interface Props {
        open?: boolean
        children: Snippet
    }
    let { open = false, children }: Props = $props();

    let el: HTMLDivElement;
    let height = $state(0);

    $effect(() => {
        if (!el) return;

        height = el.scrollHeight;

        const observer = new ResizeObserver(() => {
            height = el.scrollHeight;
        });

        observer.observe(el);

        return () => observer.disconnect();
    });
</script>

<div 
    bind:this={el} 
    class="slide-container" 
    style:max-height={`${open ? height : 0}px`}
>
    {@render children()}
</div>

<style>
    .slide-container {
		overflow: hidden;
		transition: max-height 0.3s ease;
	}
</style>