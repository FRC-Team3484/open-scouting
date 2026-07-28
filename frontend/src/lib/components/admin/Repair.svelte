<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";

	import type { RepairResponse } from "$lib/api/model";


    interface Props {
        repair: RepairResponse
    }
    let { repair }: Props = $props();
</script>

<Card.Root>
    <Card.Content>
        {repair.name}
    </Card.Content>
</Card.Root>