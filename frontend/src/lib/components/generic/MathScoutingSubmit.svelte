<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import { CheckCircle, DotsThree } from "phosphor-svelte";
    import Button from "../ui/button/button.svelte";
</script>

<Card.Root class="w-auto min-w-64 my-4">
    <div class="flex flex-row gap-2 items-center justify-center">
        <Button class="px-8!" type="submit"><CheckCircle weight="bold" /> Submit</Button>
        <Button variant="outline" size="icon"><DotsThree weight="bold" /></Button>
    </div>
</Card.Root>

