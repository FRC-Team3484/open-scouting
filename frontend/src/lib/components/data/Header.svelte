<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
	import Logo from "../generic/Logo.svelte";
    import * as Select from "$lib/components/ui/select/index.js";
	import Label from "../ui/label/label.svelte";

    let { mode = $bindable() } = $props();
</script>

<Card.Root>
    <Card.Content>
        <div class="flex flex-row gap-2 items-center">
            <Logo text={false} style="tiny" href="/" />

            <div class="flex flex-col gap-2">
                <p class="text-lg font-bold">View Match Scouting Data</p>
                <Select.Root type="single" bind:value={mode}>
                    <Select.Trigger>{mode.charAt(0).toUpperCase() + mode.slice(1)}</Select.Trigger>

                    <Select.Content>
                        <Select.Label>Mode</Select.Label>

                        <Select.Item value="all" label="All" />
                        <Label class="ml-2 text-xs text-muted-foreground mb-2">View all data with filters</Label>

                        <Select.Item value="compare" label="Compare" />
                        <Label class="ml-2 text-xs text-muted-foreground">Compare data between teams</Label>
                    </Select.Content>
                </Select.Root>
            </div>
        </div>
    </Card.Content>
</Card.Root>
