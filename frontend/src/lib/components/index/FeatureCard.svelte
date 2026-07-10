<!-- 
@component
A card for a feature, given an image, title, content, and footer

Props:
    - `image` (`Snippet`) - The component to use as the image
    - `title` (`Snippet`) - The component to use as the title
    - `content` (`Snippet`) - The component to use as the content
    - `footer` (`Snippet`) - The component to use as the footer
-->
<script lang="ts">
	import type { Snippet } from "svelte";

    import * as Card from "$lib/components/ui/card/index.js";

    
    interface Props {
        image: Snippet
        title: Snippet
        content: Snippet
        footer?: Snippet
    }
    let { image, title, content, footer }: Props = $props();
</script>

<Card.Root>
    <Card.Content>
        <div class="flex flex-col-reverse lg:flex-row pl-0 lg:pl-8 gap-8 items-center lg:items-start w-[80vw] md:w-[60vw] lg:w-[40vw]">
            {@render image?.()}
            
            <div class="flex flex-1 flex-col justify-between self-stretch text-left">
                <div>
                    <div class="flex flex-row gap-2 items-center">
                        {@render title?.()}
                    </div>

                    {@render content?.()}
                </div>

                {#if footer}
                    <div class="pt-6">
                        {@render footer()}
                    </div>
                {/if}
            </div>
        </div>
    </Card.Content>
</Card.Root>