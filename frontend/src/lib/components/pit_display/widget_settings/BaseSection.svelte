<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js"

    interface Props {
        section: "one" | "two"
        orientation: "horizontal" | "vertical"
        widgets: Object
    }
    let { section, orientation, widgets = $bindable() }: Props = $props();

    let relevantWidgets = $derived(
        widgets.filter((widget) => widget.section == section)
    )
</script>

<Card.Root>
    <Card.Content>
        <div class="flex flex-row gap-2 items-center">
            <p class="font-bold">
                {#if section == "one"}
                    {#if orientation == "horizontal"}
                        Left Section
                    {:else}
                        Top Section
                    {/if}
                {:else}
                    {#if orientation == "horizontal"}
                        Right Section
                    {:else}
                        Bottom Section
                    {/if}
                {/if}
            </p>
        </div>

        {#each relevantWidgets as widget}
            <p>{widget.id}</p>
        {/each}
    </Card.Content>
</Card.Root>