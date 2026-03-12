<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
	import { ArrowClockwise, CircleNotch, Export, FileCsv, FileText } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import TeamData from "./TeamData.svelte";
	import { toast } from "svelte-sonner";
	import Separator from "../ui/separator/separator.svelte";
	import { getDataDataGetGet } from "$lib/api/data/data";
	import type { GetDataDataGetGetParams } from "$lib/api/model";
	import CompareTable from "./CompareTable.svelte";

    let { filters, fields = $bindable() } = $props();

    let data = $state(null);
    let loadConfirmed = $state(false);


    async function loadData() {
        if (filters.year > 0) {
            const params: GetDataDataGetGetParams = {
                year: filters.year,
                event_codes: "",
                team_numbers: ""
            }

            if (filters.event_codes.length) {
                params.event_codes = filters.event_codes.join(",");
            }

            if (filters.team_numbers.length) {
                params.team_numbers = filters.team_numbers.join(",");
            }
            
            // TODO: This needs a proper response schema
            await getDataDataGetGet(params).then((response) => {
                if (response.status === 200) {
                    data = response.data;
                    fields = getFields(data);
                } else {
                    data = "error";
                    toast.error("Error loading data", { duration: 5000 });
                    fields = [];
                }
            }).catch((error) => {
                console.error(error);
                data = "error";
                toast.error("Error loading data", { duration: 5000 });
                fields = [];
            });
        }
    }

    /**
     * Get all unique fields from the data
     * 
     * @param data
     * @returns Array<{ name: string; value: string }>
     */
    function getFields(data) {
        const fields = new Map();

        for (const team of data) {
            for (const item of team.summary) {
                if (!fields.has(item.field_uuid)) {
                    fields.set(item.field_uuid, {
                        value: item.field_uuid,
                        name: item.field_name
                    });
                }
            }
        }

        return Array.from(fields.values());
    }

    function exportAsJson() {
        const jsonData = JSON.stringify(data);
        const blob = new Blob([jsonData], {type: 'application/json'});
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `open-scouting-data-${filters.year}.json`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    }

    export function exportAsCsv() {
        if (!Array.isArray(data) || data.length === 0) return;

        const rows: string[][] = [];

        rows.push([
            "team_number",
            "nickname",
            "section",
            "game_piece",
            "field_name",
            "field_type",
            "stat_type",
            "min",
            "max",
            "avg",
            "values"
        ]);

        for (const team of data) {
            const teamNumber = team.team_number ?? "";
            const nickname = team.nickname ?? "";

            // Teleop and Auton
            for (const section of ["teleop", "auton"]) {
            const bucket = team[section];
            if (!bucket) continue;

            for (const [gamePiece, fields] of Object.entries(bucket)) {
                for (const field of fields as any[]) {
                rows.push([
                    String(teamNumber),
                    nickname,
                    section,
                    gamePiece,
                    field.field_name ?? "",
                    field.field_type ?? "",
                    field.stat_type ?? "",
                    field.min ?? "",
                    field.max ?? "",
                    field.avg ?? "",
                    JSON.stringify(field.values ?? [])
                ]);
                }
            }
            }

            // Capabilities
            if (Array.isArray(team.capability)) {
            for (const field of team.capability) {
                rows.push([
                String(teamNumber),
                nickname,
                "capability",
                "",
                field.field_name ?? "",
                field.field_type ?? "",
                "capability",
                "",
                "",
                "",
                JSON.stringify(field.percentages ?? [])
                ]);
            }
            }

            // Other
            if (Array.isArray(team.other)) {
            for (const field of team.other) {
                rows.push([
                String(teamNumber),
                nickname,
                "other",
                "",
                field.field_name ?? "",
                field.field_type ?? "",
                "other",
                "",
                "",
                "",
                JSON.stringify(field.values ?? [])
                ]);
            }
            }
        }

        // Generate
        const csvContent = rows
            .map(row =>
            row
                .map(cell =>
                `"${String(cell).replace(/"/g, '""')}"`
                )
                .join(",")
            )
            .join("\n");

        // Download
        const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.download = `open-scouting-data-${filters.year}.csv`;
        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    $effect(() => {
        // Don't load data unless a filter has been selected, because unfiltered data may take a long time to render
        if (filters.year != 0 && filters.event_codes.length > 0 || filters.team_numbers.length > 0) {
            loadConfirmed = true;
            loadData();
        } else {
            loadConfirmed = false;
        }
    });
</script>

{#if !loadConfirmed && filters.year != 0}
    <Card.Root class="my-4 items-center">
        <Card.Content class="max-w-64">
            <div class="flex flex-col gap-2">
                <p class="font-bold">Load data?</p>
                <p class="text-sm text-muted-foreground">All data (with no filters) may take a long time to load, so it's not loaded by default.</p>
                <Button onclick={() => {loadData(); loadConfirmed = true}}>Load Anyway</Button>
            </div>
        </Card.Content>
    </Card.Root>
{:else if filters.year != 0}
    {#if data == null}
        <CircleNotch weight="bold" class="animate-spin my-4" size={24} />
    {:else if data.length == 0}
        <div class="flex flex-col gap-1 my-4 flex-wrap max-w-64">
            <p class="text-muted-foreground">No data found</p>
            <p class="text-muted-foreground text-sm">Please check your filters and try again</p>
        </div>
    {:else if data == "error"}
        <div class="flex flex-col gap-1 my-4 flex-wrap max-w-64">
            <p class="text-muted-foreground">Error loading data</p>
            <p class="text-muted-foreground text-sm">Recieved an invalid response from the backend. Please check your filters and try again</p>
        </div>
    {:else}
        <div class="flex flex-col gap-4 my-4">
            <Card.Root>
                <Card.Content>
                    <div class="flex flex-row gap-2 items-center">
                        <p class="text-sm text-muted-foreground">Loaded {data.length} {data.length == 1 ? "team" : "teams"} with data</p>
                        <Button size="sm" variant="outline" onclick={() => loadData()}><ArrowClockwise weight="bold" /> Refresh</Button>
                        <!-- <DropdownMenu.Root>
                            <DropdownMenu.Trigger>
                                <Button size="sm" variant="outline"><Export weight="bold" /> Export</Button>
                            </DropdownMenu.Trigger>

                            <DropdownMenu.Content class="w-56" align="start">
                                <DropdownMenu.Label>Export as...</DropdownMenu.Label>
                                <DropdownMenu.Group>
                                    <DropdownMenu.Item onclick={exportAsJson}>
                                        <FileText weight="bold" /> JSON
                                    </DropdownMenu.Item>
                                    <DropdownMenu.Item onclick={exportAsCsv}>
                                        <FileCsv weight="bold" /> CSV
                                    </DropdownMenu.Item>
                                </DropdownMenu.Group>
                            </DropdownMenu.Content>
                        </DropdownMenu.Root> -->
                    </div>
                </Card.Content>
            </Card.Root>

            <Separator orientation="horizontal" />

            <CompareTable data={data} filters={filters} fields={fields} />
        </div>
    {/if}
{/if}