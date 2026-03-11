<script lang="ts">
    import DrawerHeader from "$lib/components/generic/drawers/DrawerHeader.svelte";

    import * as Sheet from "$lib/components/ui/sheet";
	import { FloppyDisk } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import { Separator } from "../ui/separator";
	import { onMount } from "svelte";
	import Progress from "../ui/progress/progress.svelte";
	import { db } from "$lib/utils/db";
	import Badge from "../ui/badge/badge.svelte";
    import * as Dialog from "../ui/dialog";
	import { toast } from "svelte-sonner";
	import { fetchEventData, fetchSeasonData, pushMatchScoutingData } from "$lib/utils/sync";

    let totalSpace = $state(0);
    let usedSpace = $state(0);

    let events = $state(0);
    let seasonData = $state(0);
    let matchScoutingData = $state(0);
    let matchScoutingDataUnsynced = $state(0);
    let pitScoutingData = $state(0);
    let pitScoutingDataUnsynced = $state(0);

    function getSpaceUsed() {
        const quota = navigator.storage.estimate();
        quota.then((result) => {
            totalSpace = (result.quota / (1024 * 1024)).toFixed(2);
            usedSpace = (result.usage / (1024 * 1024)).toFixed(2);
        });
    }

    async function getAmount() {
        events = await db.event.count();
        seasonData = await db.season_data.count();
        matchScoutingData = await db.match_scouting.count();
        matchScoutingDataUnsynced = await db.match_scouting.filter(m => m.synced === false).count();
        pitScoutingData = await db.pit_scouting.count();
        pitScoutingDataUnsynced = await db.pit_scouting.filter(m => m.synced === false).count();
    }

    onMount(() => {
        getSpaceUsed();
        getAmount();
    })
</script>

<Sheet.Root>
    <Sheet.Trigger>
        <Button variant="outline" class="w-full"><FloppyDisk weight="bold" /> Manage Local Data</Button>
    </Sheet.Trigger>

    <Sheet.Content class="max-h-[80vh] overflow-y-scroll lg:mx-64 2xl:mx-128 border-1 p-4 rounded-t-lg" side="bottom">
        <div class="overflow-y-scroll pr-2">
            <DrawerHeader title="Manage Local Data" description="View and manage data stored locally on your device" />
            <Separator orientation="horizontal" />
            <div class="flex flex-col gap-4 my-6">
                <div class="flex flex-row gap-2 items-center">
                    <p>Used</p>
                    <p class="font-bold">~{usedSpace} MB</p>
                    <p>of</p>
                    <p class="font-bold">{totalSpace} MB</p>
                    <p>({((usedSpace / totalSpace) * 100).toFixed(2)}%)</p>
                </div>
                <Progress value={usedSpace} max={totalSpace} />
                <p class="text-sm text-muted-foreground">The total space allocated for Open Scouting's storage by your browser. If your device is low on storage, the avaliable space may be very low, and your browser may delete some of Open Scouting's data to save on space.</p>
                <p class="text-sm text-muted-foreground">Database changes may not be fully reflected until the page is reloaded.</p>
            </div>
            <Separator orientation="horizontal" />
            <div class="flex flex-col gap-4 my-6">
                <div class="flex flex-col gap-2">
                    <div class="flex flex-row gap-2 items-center flex-wrap">
                        <p class="font-bold">{events} Event(s)</p>
                        <Dialog.Root>
                            <Dialog.Trigger>
                                <Button variant="outline">Delete</Button>
                            </Dialog.Trigger>
                            <Dialog.Content>
                                <Dialog.Title>Are you sure?</Dialog.Title>
                                <Dialog.Description>Are you sure you want to delete all event data? This cannot be undone.</Dialog.Description>
                                <Dialog.Footer>
                                    <Dialog.Close>
                                        <Button variant="outline">Cancel</Button>
                                    </Dialog.Close>
                                    <Dialog.Close>
                                        <Button type="submit" onclick={async () => { await db.event.clear(); await getAmount(); getSpaceUsed(); await toast.success("Event cache cleared"); }}>Delete</Button>
                                    </Dialog.Close>
                                </Dialog.Footer>
                            </Dialog.Content>
                        </Dialog.Root>
                        <Dialog.Root>
                            <Dialog.Trigger>
                                <Button variant="outline">Rebuild</Button>
                            </Dialog.Trigger>
                            <Dialog.Content>
                                <Dialog.Title>Are you sure?</Dialog.Title>
                                <Dialog.Description>Are you sure you want to rebuild the event cache?</Dialog.Description>
                                <Dialog.Footer>
                                    <Dialog.Close>
                                        <Button variant="outline">Cancel</Button>
                                    </Dialog.Close>
                                    <Dialog.Close>
                                        <Button type="submit" onclick={async () => { await fetchEventData(); await getAmount(); getSpaceUsed(); await toast.success("Event cache rebuilt"); }}>Rebuild</Button>
                                    </Dialog.Close>
                                </Dialog.Footer>
                            </Dialog.Content>
                        </Dialog.Root>
                    </div>
                    <p class="text-sm text-muted-foreground">The TBA events for all years, stored locally for offline use and faster loading</p>
                </div>
                <div class="flex flex-col gap-2">
                    <div class="flex flex-row gap-2 items-center flex-wrap">
                        <p class="font-bold">{seasonData} Season Data</p>
                        <Dialog.Root>
                            <Dialog.Trigger>
                                <Button variant="outline">Delete</Button>
                            </Dialog.Trigger>
                            <Dialog.Content>
                                <Dialog.Title>Are you sure?</Dialog.Title>
                                <Dialog.Description>Are you sure you want to delete all season data? This cannot be undone.</Dialog.Description>
                                <Dialog.Footer>
                                    <Dialog.Close>
                                        <Button variant="outline">Cancel</Button>
                                    </Dialog.Close>
                                    <Dialog.Close>
                                        <Button type="submit" onclick={async () => { await db.season_data.clear(); await getAmount(); getSpaceUsed(); await toast.success("Season data cleared"); }}>Delete</Button>
                                    </Dialog.Close>
                                </Dialog.Footer>
                            </Dialog.Content>
                        </Dialog.Root>
                        <Dialog.Root>
                            <Dialog.Trigger>
                                <Button variant="outline">Rebuild</Button>
                            </Dialog.Trigger>
                            <Dialog.Content>
                                <Dialog.Title>Are you sure?</Dialog.Title>
                                <Dialog.Description>Are you sure you want to rebuild the season data cache?</Dialog.Description>
                                <Dialog.Footer>
                                    <Dialog.Close>
                                        <Button variant="outline">Cancel</Button>
                                    </Dialog.Close>
                                    <Dialog.Close>
                                        <Button type="submit" onclick={async () => { await fetchSeasonData(); await getAmount(); getSpaceUsed(); await toast.success("Season data cache rebuilt"); }}>Rebuild</Button>
                                    </Dialog.Close>
                                </Dialog.Footer>
                            </Dialog.Content>
                        </Dialog.Root>
                    </div>
                    <p class="text-sm text-muted-foreground">The season data for each year, including the fields and game pieces for that year</p>
                </div>
                <div class="flex flex-col gap-2">
                    <div class="flex flex-row gap-2 items-center flex-wrap">
                        <p class="font-bold">{matchScoutingData} Match Scouting Submissions</p>
                        {#if matchScoutingDataUnsynced > 0}
                            <Badge variant="destructive">{matchScoutingDataUnsynced} Unsynced</Badge>
                            <Dialog.Root>
                                <Dialog.Trigger>
                                    <Button>Sync</Button>
                                </Dialog.Trigger>
                                <Dialog.Content>
                                    <Dialog.Title>Are you sure?</Dialog.Title>
                                    <Dialog.Description>Are you sure you want to sync match scouting data?</Dialog.Description>
                                    <Dialog.Footer>
                                        <Dialog.Close>
                                            <Button variant="outline">Cancel</Button>
                                        </Dialog.Close>
                                        <Dialog.Close>
                                            <Button type="submit" onclick={async () => { await pushMatchScoutingData(); await getAmount(); getSpaceUsed(); await toast.success("Match scouting data synced"); }}>Sync</Button>
                                        </Dialog.Close>
                                    </Dialog.Footer>
                                </Dialog.Content>
                            </Dialog.Root>
                        {/if}
                        <Dialog.Root>
                            <Dialog.Trigger>
                                <Button variant="outline">Delete</Button>
                            </Dialog.Trigger>
                            <Dialog.Content>
                                <Dialog.Title>Are you sure?</Dialog.Title>
                                <Dialog.Description>Are you sure you want to delete all match scouting data? This cannot be undone, and any unsynced data will be completely lost.</Dialog.Description>
                                <Dialog.Footer>
                                    <Dialog.Close>
                                        <Button variant="outline">Cancel</Button>
                                    </Dialog.Close>
                                    <Dialog.Close>
                                        <Button type="submit" onclick={async () => { await db.match_scouting.clear(); await getAmount(); getSpaceUsed(); await toast.success("Match scouting data cleared"); }}>Delete</Button>
                                    </Dialog.Close>
                                </Dialog.Footer>
                            </Dialog.Content>
                        </Dialog.Root>
                    </div>
                    <p class="text-sm text-muted-foreground">Match scouting data stored locally, in case of poor connection requiring reports to be submitted later</p>
                </div>
                <div class="flex flex-col gap-2">
                    <div class="flex flex-row gap-2 items-center flex-wrap">
                        <p class="font-bold">{pitScoutingData} Team Pits</p>
                        {#if pitScoutingDataUnsynced > 0}
                            <Badge variant="destructive">{pitScoutingDataUnsynced} Unsynced</Badge>
                            <!-- <Dialog.Root>
                                <Dialog.Trigger>
                                    <Button>Sync</Button>
                                </Dialog.Trigger>
                                <Dialog.Content>
                                    <Dialog.Title>Are you sure?</Dialog.Title>
                                    <Dialog.Description>Are you sure you want to sync match scouting data?</Dialog.Description>
                                    <Dialog.Footer>
                                        <Dialog.Close>
                                            <Button variant="outline">Cancel</Button>
                                        </Dialog.Close>
                                        <Dialog.Close>
                                            <Button type="submit" onclick={async () => { await pushMatchScoutingData(); await getAmount(); getSpaceUsed(); await toast.success("Match scouting data synced"); }}>Sync</Button>
                                        </Dialog.Close>
                                    </Dialog.Footer>
                                </Dialog.Content>
                            </Dialog.Root> -->
                        {/if}
                        <Dialog.Root>
                            <Dialog.Trigger>
                                <Button variant="outline">Delete</Button>
                            </Dialog.Trigger>
                            <Dialog.Content>
                                <Dialog.Title>Are you sure?</Dialog.Title>
                                <Dialog.Description>Are you sure you want to delete all pit scouting data? This cannot be undone, and any unsynced data will be completely lost.</Dialog.Description>
                                <Dialog.Footer>
                                    <Dialog.Close>
                                        <Button variant="outline">Cancel</Button>
                                    </Dialog.Close>
                                    <Dialog.Close>
                                        <Button type="submit" onclick={async () => { await db.pit_scouting.clear(); await getAmount(); getSpaceUsed(); await toast.success("Pit scouting data cleared"); }}>Delete</Button>
                                    </Dialog.Close>
                                </Dialog.Footer>
                            </Dialog.Content>
                        </Dialog.Root>
                    </div>
                    <p class="text-sm text-muted-foreground">Pit scouting data for each team at each event in each season that you've loaded. Used to manage the live pit scouting page, and keep you and the other scouts up to date.</p>
                </div>
            </div>
        </div>
    </Sheet.Content>
</Sheet.Root>