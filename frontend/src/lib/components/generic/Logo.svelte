<script lang="ts">
    import icon_rounded from "$lib/assets/icon_rounded.png"

    type Style = "tiny" | "small" | "normal";
    type alignment = "column" | "row" | "auto";

    export let text: boolean = true;
    export let style: Style = "normal";
    export let href: string | null = null;
    export let alignment: alignment = "auto";
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