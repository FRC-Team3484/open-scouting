<!--
@component
A warning when the user is offline

Props:
    - `text` (`string`) - The text to display
-->
<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { HouseIcon, WifiSlashIcon } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
    
    interface Props {
        text: string;
    }
    let { text }: Props = $props();
</script>
<Card.Root class="mt-4">
    <Card.Content>
        <div class="flex flex-col gap-2 items-center">
            <WifiSlashIcon size={32} weight="bold" />
            <p class="text-xl font-bold">You're Offline</p>
            <p class="text-md">{text}</p>
            <p class="text-md">Check your internet connection and try again.</p>
            <Button variant="default" href="/"><HouseIcon weight="bold" /> Home</Button>
        </div>
    </Card.Content>
</Card.Root>