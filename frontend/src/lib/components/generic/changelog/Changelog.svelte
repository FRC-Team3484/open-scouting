<script lang="ts">
	import { changelogDialogOpen, changelogDialogVersion } from "$lib/stores/dialog";
	import BaseDialog from "../dialogs/BaseDialog.svelte";
	import Button from "$lib/components/ui/button/button.svelte";
	import Checkbox from "$lib/components/ui/checkbox/checkbox.svelte";
	import Label from "$lib/components/ui/label/label.svelte";
	import { GithubLogo, List, XCircle } from "phosphor-svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";
	import { onMount, tick } from "svelte";

    let Changelog = $state(null);
    let showAllChangelogs = $state(false);

    let neverShow = $state(false);

    const changelogModules = import.meta.glob(
        "$lib/components/generic/changelog/logs/*.svelte",
        { eager: true }
    );
    let allChangelogs = $derived(
        Object.keys(changelogModules)
            .filter(
                key =>
                    key !==
                    "/src/lib/components/generic/changelog/logs/Generic.svelte"
            )
            .map(key =>
                key.replace(/^.*\/logs\//, "").replace(/\.svelte$/, "")
            )
            .reverse()
    );

    function close() {
        if (neverShow) {
            localStorage.setItem("showChangelogs", "false");
        } else {
            localStorage.setItem("showChangelogs", "true");
        }

        changelogDialogOpen.set(false);
    }

    $effect(async () => {
        if (!$changelogDialogVersion) {
            Changelog = null;
            return;
        }

        const module =
            changelogModules[
                `/src/lib/components/generic/changelog/logs/${$changelogDialogVersion}.svelte`
            ];

        Changelog = module?.default ?? null;
    });

    onMount(async () => {
        neverShow = localStorage.getItem("showChangelogs") === "false";
    })

</script>

<BaseDialog title="Changelog" description={`Changes in Open Scouting ${$changelogDialogVersion}`} bind:open={$changelogDialogOpen}>
    <Separator class="my-2"/>
    
    {#if Changelog}
        <svelte:component this={Changelog} />
    {:else}
        <p>No changelog found</p>
    {/if}

    <Separator class="my-2"/>

    <div class="flex flex-col gap-2">
        <div class="flex flex-row gap-2">
            <Button class="flex-1" variant="outline" href={`https://github.com/FRC-Team3484/open-scouting/releases/tag/${$changelogDialogVersion}`} target="_blank" rel="noopener noreferrer"><GithubLogo weight="bold" /> Full Release Notes</Button>
            <Button class="flex-1" variant="outline" onclick={() => showAllChangelogs = true}><List weight="bold" /> All Changelogs</Button>
        </div>
        
        <div class="flex flex-row gap-2 items-center">
            <Button class="flex-2" onclick={close}><XCircle weight="bold" /> Close</Button>
            <Checkbox bind:checked={neverShow} />
            <Label>Never show again</Label>
        </div>
    </div>

    {#if showAllChangelogs}
        <BaseDialog title="All Changelogs" description="Select a changelog to view" bind:open={showAllChangelogs}>
            {#each allChangelogs as log}
                <Button variant="outline" onclick={() => {showAllChangelogs = false; $changelogDialogVersion = log}} disabled={log === $changelogDialogVersion}>{log}</Button>
            {/each}

            <Separator class="my-2"/>

            <div class="flex flex-row gap-2">
                <Button variant="outline" class="flex-1" href="https://github.com/FRC-Team3484/open-scouting/releases" target="_blank" rel="noopener noreferrer"><GithubLogo weight="bold" /> All Release Notes</Button>
                <Button class="flex-1" onclick={() => showAllChangelogs = false}><XCircle weight="bold" /> Cancel</Button>
            </div>
        </BaseDialog>
    {/if}
</BaseDialog>