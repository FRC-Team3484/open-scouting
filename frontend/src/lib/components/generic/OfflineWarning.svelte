<!--
@component
A warning when the user is offline

Props:
    - `text` (`string`) - The text to display
    - `showHome` (`boolean`) - If the home button and error text should be shown
-->
<script lang="ts">
	import { slide } from "svelte/transition";
	import { HouseIcon, WifiSlashIcon } from "phosphor-svelte";

	import Button from "../ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";

    
    interface Props {
        text: string;
        showHome?: boolean
    }
    let { text, showHome }: Props = $props();
</script>

<div transition:slide>
    <Card.Root class="mt-4 max-w-full lg:max-w-[40vw]">
        <Card.Content>
            <div class="flex flex-col gap-2 items-center">
                <WifiSlashIcon size={32} weight="bold" />
                <p class="text-xl font-bold">You're Offline</p>
                <p class="text-md">{text}</p>
                {#if showHome}
                    <p class="text-md">Check your internet connection and try again.</p>
                    <Button variant="default" href="/"><HouseIcon weight="bold" /> Home</Button>
                {/if}
            </div>
        </Card.Content>
    </Card.Root>
</div>