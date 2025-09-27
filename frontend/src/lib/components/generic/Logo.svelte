<script lang="ts">
    import icon_rounded from "$lib/assets/icon_rounded.png"

    type Style = "small" | "normal";

    export let text: boolean = true;
    export let style: Style = "normal";
</script>

<div class="flex flex-row gap-4 items-center">
    <img
        src={icon_rounded}
        alt="Logo"
        class={style === "small" ? "w-16 h-16" : "w-24 h-24"}
    />

    {#if text}
        <p class={style === "small" ? "text-2xl font-bold font-mono" : "text-5xl font-bold font-mono"}>Open Scouting</p>
    {/if}
</div>