<!-- 
@component
Header text for the admin page

Props:
    - `handleNavigate` (function) - The function for changing the admin page
-->
<script lang="ts">
	import { ArrowLeftIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";
	import Button from "../ui/button/button.svelte";
    

    interface Props {
        handleNavigate: (nextPage: string) => void;
    }
    let { handleNavigate }: Props = $props();
</script>

<Card.Root class="w-auto min-w-64 mb-4">
    <Card.Content>
        <div class="flex flex-col gap-2">
            <p class="font-bold">Server Administration</p>
            <Button variant="outline" onclick={() => handleNavigate("start")}><ArrowLeftIcon weight="bold" /> Back</Button>
        </div>
    </Card.Content>
</Card.Root>