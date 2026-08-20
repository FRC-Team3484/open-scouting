<!-- 
@component
Drawer header component, generally used by menu drawers

Props:
    - `title` (`string`) - The title of the drawer header
    - `description` (`string`) - The description of the drawer header
-->
<script lang="ts">
    interface Props {
        title: string
        description: string
    }
    let { title, description }: Props = $props();
</script>

<div class="flex flex-row gap-2 justify-between my-4">
    <div class="flex flex-col gap-2">
        <p class="text-lg font-bold">{title}</p>
        <p class="text-sm text-muted-foreground">{description}</p>
    </div>
</div>