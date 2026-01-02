<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import BaseTeamFolder from "./BaseTeamFolder.svelte";
    
    let { others } = $props();
</script>

<BaseTeamFolder title="Other">
    <div class="flex flex-col gap-2 text-left">
        {#each others as other}
            <Card.Root>
                <Card.Content>
                    <p class="font-bold">{other.field_name}</p>
                    <ul class="list-disc list-inside">
                        {#each other.values as value}
                            <li class="text-sm">Match {value.match_number} - {value.value}</li>
                        {/each}
                    </ul>
                </Card.Content>
            </Card.Root>
        {/each}
    </div>
</BaseTeamFolder>