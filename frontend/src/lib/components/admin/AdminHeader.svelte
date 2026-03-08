<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { ArrowLeft } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";

    export let handleNavigate: (nextPage: string) => void;
</script>

<Card.Root class="w-auto min-w-64 mb-4">
    <Card.Content>
        <div class="flex flex-col gap-2">
            <p class="font-bold">Server Administration</p>
            <Button variant="outline" onclick={() => handleNavigate("start")}><ArrowLeft weight="bold" /> Back</Button>
        </div>
    </Card.Content>
</Card.Root>