<!-- 
@component
Generic component for showing the Open Scouting logo

Props:
    - `text` (`boolean`) - If "Open Scouting" logo text should be shown
    - `style` (`"tiny" | "small" | "normal"`) - The style of logo to show
    - `href` (`string | null`) - The link to open when clicked. If null, it's not clickable
    - `alignment` (`"column" | "row" | "auto"`) - The alignment of the component
-->
<script lang="ts">
    import icon_rounded from "$lib/assets/icon_rounded.png"


    interface Props {
        text?: boolean
        style?: "tiny" | "small" | "normal"
        href?: string | null
        alignment?: "column" | "row" | "auto"
    }
    let { text = true, style = "normal", href = null, alignment = "auto"}: Props = $props();
</script>

<div class={`flex items-center ${alignment === "auto" ? "flex-col md:flex-row" : (alignment === "row" ? "flex-row" : "flex-col")} gap-4`}>
    {#if href}
        <a href={href} class="hover:scale-105 transition-transform aspect-square">
            <img
                src={icon_rounded}
                alt="Logo"
                class={
                    style === "tiny" ? "w-12 h-12 aspect-square"
                    : style === "small" ? "w-16 h-16 aspect-square"
                    : "w-24 h-24 aspect-square"
                }
            />
        </a>
    {:else}
        <img
            src={icon_rounded}
            alt="Logo"
            class={
                    style === "tiny" ? "w-12 h-12 aspect-square"
                    : style === "small" ? "w-16 h-16 aspect-square"
                    : "w-24 h-24 aspect-square"
                }
        />
    {/if}

    {#if text}
        <p class={
            style === "tiny" ? "text-lg font-bold font-mono" 
            : style === "small" ? "text-2xl font-bold font-mono" 
            : "text-3xl md:text-5xl font-bold font-mono"
        }>Open Scouting</p>
    {/if}
</div>