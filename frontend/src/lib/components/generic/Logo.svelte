<script lang="ts">
    import icon_rounded from "$lib/assets/icon_rounded.png"

    export let text: boolean = true;
</script>

<div class="flex flex-row gap-4 items-center">
    <img src={icon_rounded} alt="Logo" class="w-24 h-24" />

    {#if text}
        <p class="text-5xl font-bold font-mono">Open Scouting</p>
    {/if}
</div>