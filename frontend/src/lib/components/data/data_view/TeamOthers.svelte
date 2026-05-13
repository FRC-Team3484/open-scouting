<!-- 
@component
The other section for each team on the default data view page

Props:
    - `others` (`unknown`) - All other fields for the team
-->
<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import BaseTeamFolder from "./BaseTeamFolder.svelte";
    

    // TODO: `data` from DataManager needs a proper response schema
    interface Props {
        others: unknown
    }
    let { others }: Props = $props();
</script>

<BaseTeamFolder title="Other">
    <div class="flex flex-col gap-2 text-left">
        {#each others as other}
            <Card.Root>
                <Card.Content>
                    <p class="font-bold">{other.field_name}</p>
                    <ul class="list-disc list-inside">
                        {#each other.values as value}
                            {#if value.value != ""}
                                <li class="text-sm">Match {value.match_number} - {value.value}</li>
                            {/if}
                        {/each}
                    </ul>
                </Card.Content>
            </Card.Root>
        {/each}
    </div>
</BaseTeamFolder>