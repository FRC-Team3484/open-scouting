<!-- 
@component
A header for different setting sections

Props:
    - `name` (`string`) - The name of the section
-->
<script lang="ts">
    interface Props {
        name: string
    }
    let { name }: Props = $props();
</script>

<p class="font-bold">{name}</p>