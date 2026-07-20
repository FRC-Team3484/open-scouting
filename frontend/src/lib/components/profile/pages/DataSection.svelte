<!-- 
@component
The data section on the profile page, for viewing and deleting the user's submitted data

TODO: Data here should probably be paginated
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { slide } from "svelte/transition";
	import { ArrowClockwiseIcon, ClockIcon, InfoIcon, TrashIcon } from "phosphor-svelte";
	import { toast } from "svelte-sonner";

    import * as Alert from "$lib/components/ui/alert";
	import Button from "$lib/components/ui/button/button.svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";
    import * as Card from "$lib/components/ui/card";
    import * as Select from "$lib/components/ui/select";
	import Badge from "$lib/components/ui/badge/badge.svelte";
    import * as AlertDialog from "$lib/components/ui/alert-dialog";

	import Section from "./BaseSection.svelte";
	import type { MyDataResponse } from "$lib/api/model";
	import { deleteMyDataProfileDeleteTypeUuidDelete, getMyDataProfileMyDataGet } from "$lib/api/profile/profile";
    

    let data: MyDataResponse[] = $state([]);

    let filteredData: MyDataResponse[] = $derived.by(() => {
        return data.filter((f) => filteredTypes.includes(f.type)).sort((a, b) => {
            if (sortValue === "newestToOldest") {
                return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
            } else {
                return new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
            }
        });
    });

    let sortOptions = [
        {
            value: "newestToOldest",
            label: "Newest to Oldest"
        },
        {
            value: "oldestToNewest",
            label: "Oldest to Newest"
        }
    ]
    let sortValue = $state("newestToOldest");
    let sortLabel = $derived(
        sortOptions.find((f) => f.value === sortValue)?.label ?? "Newest to Oldest"
    )

    let types = [
        { value: "match_scouting_submission", label: "Match Scouting Submission" },
        { value: "match_scouting_answer", label: "Match Scouting Answer" },
        { value: "team_pit", label: "Team Pit" },
        { value: "pit_scouting_answer", label: "Pit Scouting Answer" },
        { value: "event", label: "Event" }
    ]
    let filteredTypes = $state(["match_scouting_submission", "match_scouting_answer", "team_pit", "pit_scouting_answer", "event"]);

    let selected: string[] = $state([]);

    /**
     * Get all of the user's data from the server
     */
    async function getData() {
        await getMyDataProfileMyDataGet().then((response) => {
            if (response.status === 200) {
                data = response.data
            } else {
                toast.error("Failed to get data", { duration: 5000 });
            }
        })
    }

    /**
     * Delete data from the server
     * 
     * @param uuid The uuid of the data
     * @param multiple If true, don't show a toast
     */
    async function deleteData(uuid: string, multiple: boolean = false) {
        const data_item = data.filter((f) => f.uuid === uuid)[0];
        if (data_item === undefined) {
            toast.error("Failed to delete data", { duration: 5000 });
            return;
        }
        await deleteMyDataProfileDeleteTypeUuidDelete(data_item.type, data_item.uuid).then((response) => {
            if (response.status === 200) {
                if (!multiple) {
                    toast.success("Deleted " + data_item.type, { duration: 5000 });
                    getData();
                }
            }
        })
    }

    /**
     * Delete all selected data from the server
     */
    async function deleteSelected() {
        for (const item of selected) {
            await deleteData(item, true);
        }

        toast.success("Deleted " + selected.length + " items", { duration: 5000 });
        getData();
    }

    onMount(() => {
        getData();
    })
</script>

<Section title="Data Management" description="Manage all your submitted data on the server">
    <div class="flex flex-col gap-2">
        <Alert.Root>
            <InfoIcon weight="bold" />
            <Alert.Title>Local data will not be shown</Alert.Title>
            <Alert.Description>Only data submitted to the server will be shown here. Data that has not yet been uploaded from your device will not be visible here.</Alert.Description>
        </Alert.Root>

        <Alert.Root>
            <ClockIcon weight="bold" />
            <Alert.Title>Older data may not be shown</Alert.Title>
            <Alert.Description>
                <p>Data submitted prior to <span class="font-mono">v2.2.0</span> did not track who submitted it. This data will not be shown here.</p>
            </Alert.Description>
        </Alert.Root>

        <div class="flex flex-row gap-2 items-center">
            <Button onclick={() => {getData()}} size="sm"><ArrowClockwiseIcon weight="bold" /> Reload</Button>
            <p>Viewing {filteredData.length} items</p>
        </div>

        
        <div class="flex flex-row gap-2 items-center flex-wrap">
            <Select.Root type="single" bind:value={sortValue}>
                <Select.Trigger>{sortLabel}</Select.Trigger>
    
                <Select.Content>
                    <Select.Label>Sort</Select.Label>
                    {#each sortOptions as option}
                        <Select.Item value={option.value}>{option.label}</Select.Item>
                    {/each}
                </Select.Content>
            </Select.Root>

            {#each types as type}
                <Button variant={filteredTypes.includes(type.value) ? "default" : "outline"} size="sm" onclick={() => {
                    if (filteredTypes.includes(type.value)) {
                        filteredTypes = filteredTypes.filter((f) => f !== type.value);
                    } else {
                        filteredTypes = [...filteredTypes, type.value];
                    }
                }}>{type.label}</Button>
            {/each}
        </div>

        {#if selected.length > 0}
            <div class="flex flex-col gap-2" transition:slide>
                <Separator class="my-2" />

                <div class="flex flex-row gap-2 items-center flex-wrap">
                    <p>Selected {selected.length} item{selected.length > 1 ? "s" : ""}</p>
                    <Button variant="outline" size="sm" onclick={() => {selected = []}}>Deselect All</Button>

                    <AlertDialog.Root>
                        <AlertDialog.Trigger>
                            <Button variant="destructive" size="sm" onclick={() => {}}>Delete All</Button>
                        </AlertDialog.Trigger>

                        <AlertDialog.Content>
                            <AlertDialog.Title>Delete {selected.length} items?</AlertDialog.Title>
                            <AlertDialog.Description>Are you sure you want to delete {selected.length} items? This action cannot be undone.</AlertDialog.Description>
                            <AlertDialog.Footer>
                                <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                <AlertDialog.Action type="button" onclick={() => {deleteSelected()}}>Delete</AlertDialog.Action>
                            </AlertDialog.Footer>
                        </AlertDialog.Content>
                    </AlertDialog.Root>
                </div>
            </div>
        {/if}

        <Separator class="my-2" />

        {#each filteredData as item}
            <Card.Root>
                <Card.Content>
                    <div class="flex flex-row gap-2 items-center justify-between">
                        <div class="flex flex-row gap-2 items-center">
                            <input type="checkbox" bind:group={selected} value={item.uuid} />
                            
                            <div class="flex flex-col gap-2 items-start">
                                <div class="flex flex-row gap-2 items-center flex-wrap">
                                    <Badge variant="secondary">{item.type.charAt(0).toUpperCase() + item.type.replaceAll("_", " ").slice(1)}</Badge>
                                    <p class="text-wrap">{item.name}</p>
                                </div>
                                <p class="text-sm text-muted-foreground">Created: {new Date(item.created_at).toLocaleString()}</p>
                            </div>
                        </div>

                        <AlertDialog.Root>
                            <AlertDialog.Trigger>
                                <Button variant="destructive" size="icon"><TrashIcon weight="bold" /></Button>
                            </AlertDialog.Trigger>

                            <AlertDialog.Content>
                                <AlertDialog.Title>Delete "{item.name}"?</AlertDialog.Title>
                                <AlertDialog.Description>Are you sure you want to delete this data from the server? This action cannot be undone.</AlertDialog.Description>
                                <AlertDialog.Footer>
                                    <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                    <AlertDialog.Action type="button" onclick={() => deleteData(item.uuid)}>Delete</AlertDialog.Action>
                                </AlertDialog.Footer>
                            </AlertDialog.Content>
                        </AlertDialog.Root>
                    </div>
                </Card.Content>
            </Card.Root>
        {/each}
    </div>
</Section>