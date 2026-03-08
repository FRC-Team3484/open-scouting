<script lang="ts">
    let { title, description } = $props();
</script>

<div class="flex flex-row gap-2 justify-between my-4">
    <div class="flex flex-col gap-2">
        <p class="text-lg font-bold">{title}</p>
        <p class="text-sm text-muted-foreground">{description}</p>
    </div>
</div>