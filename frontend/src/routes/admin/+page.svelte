<!-- 
The admin page

This page is only accessible to superusers. Allows for managing seasons, match scouting fields, pit scouting questions, users, events, match scouting data, and pit scouting data.
Presents a warning dialog to the user when in production.
-->
<script lang="ts">
	import { onMount, tick } from "svelte";
    import { env } from "$env/dynamic/public";
    import { overrideItemIdKeyNameBeforeInitialisingDndZones } from "svelte-dnd-action";
    import { CircleNotchIcon } from "phosphor-svelte";
	import { goto, pushState } from "$app/navigation";

    import * as Card from "$lib/components/ui/card/index.js";
	import Button from "$lib/components/ui/button/button.svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";
    import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
	import Badge from "$lib/components/ui/badge/badge.svelte";
    
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import SeasonsManager from "$lib/components/admin/SeasonsManager.svelte";
	import AdminHeader from "$lib/components/admin/AdminHeader.svelte";
	import MatchScoutingFieldsManager from "$lib/components/admin/MatchScoutingFieldsManager.svelte";
	import PitScoutingQuestionsManager from "$lib/components/admin/PitScoutingQuestionsManager.svelte";
	import UsersManager from "$lib/components/admin/UsersManager.svelte";
	import EventManager from "$lib/components/admin/EventsManager.svelte";
	import MatchScoutingSubmissionsManager from "$lib/components/admin/MatchScoutingSubmissionsManager.svelte";
	import PitScoutingDataManager from "$lib/components/admin/PitScoutingDataManager.svelte";
	import { getReportsCountReportsGetCountGet } from "$lib/api/reports/reports";
	import ReportsManager from "$lib/components/admin/ReportsManager.svelte";
	import { getRepairCountRepairsGetCountGet } from "$lib/api/repairs/repairs";
	import RepairsManager from "$lib/components/admin/RepairsManager.svelte";
	import { user } from "$lib/utils/auth";


    type Page = "start" | "seasons" | "match_fields" | "pit_scouting_questions" | "users" | "events" | "match_scouting" | "pit_scouting" | "reports" | "repairs";
    let page: Page = $state("start");
    let show_warning_dialog: boolean = $state(!(env.PUBLIC_MODE == "dev"));
    let reportCount: number | null = $state(null);
    let repairCount: number | null = $state(null);

    overrideItemIdKeyNameBeforeInitialisingDndZones("uuid");
    
    /**
     * Navigates to the given page
     * 
     * @param nextPage The page to navigate to
     */
    function handleNavigate(nextPage: string): void {
        page = <Page>nextPage;
    }

    /**
     * Get the number of reports that need to be reviewed
     */
    async function getReportCount() {
        await getReportsCountReportsGetCountGet().then((response) => {
            if (response.status === 200) {
                reportCount = response.data;
            }
        })
    }

    /**
     * Get the number of repairs that need to be completed
     */
    async function getRepairCount() {
        await getRepairCountRepairsGetCountGet().then((response) => {
            if (response.status === 200) {
                repairCount = response.data;
            }
        })
    }

    /**
     * Sets the page in the URL params
     * @param page
     */
    function setPageInUrl(page: Page) {
        const url = new URL(window.location.href);

        url.searchParams.set("page", page);

        tick().then(() => {
            pushState(url, {});
        })
    }

    /**
     * Get the page from the URL params
     */
    function getPageFromUrl(): Page {
        const url = new URL(window.location.href);

        return url.searchParams.get("page") as Page ?? "start";
    }

    /**
     * When the component mounts, check if the user is authenticated. 
     * If they're not a superuser, redirect them back to the index page.
     */
    onMount(async () => {
        if (!$user.authenticated || !$user.user?.is_superuser) {
            await goto("/");
        } else {
            getReportCount();
            getRepairCount();
    
            page = getPageFromUrl();
        }
    });

    $effect(() => {
        setPageInUrl(page);
    })
</script>

<PageContainer>
    {#if $user.authenticated && $user.user?.is_superuser}
        {#if page === "start"}
            <Card.Root class="w-auto min-w-64">
                <Card.Header>
                    <Card.Title>Server Administration</Card.Title>
                    <Card.Description>Manage the server's seasons, fields, users, and events</Card.Description>
                </Card.Header>

                <Card.Content>
                    <div class="flex flex-col gap-4">
                        <Button id="seasons" onclick={() => page = "seasons"}>Manage Seasons</Button>

                        <Separator orientation="horizontal" />

                        <Button onclick={() => page = "match_fields"}>Manage Match Scouting Fields</Button>
                        <Button onclick={() => page = "pit_scouting_questions"}>Manage Pit Scouting Questions</Button>

                        <Separator orientation="horizontal" />

                        <Button onclick={() => page = "users"}>Manage Users</Button>
                        <Button onclick={() => page = "events"}>Manage Events</Button>
                        <Button onclick={() => page = "match_scouting"}>Manage Match Scouting Data</Button>
                        <Button onclick={() => page = "pit_scouting"}>Manage Pit Scouting Data</Button>

                        <Separator orientation="horizontal" />

                        <Button onclick={() => page = "reports"}>
                            Manage Reports
                            {#if reportCount}
                                <Badge variant="secondary">{reportCount}</Badge>
                            {:else}
                                <CircleNotchIcon weight="bold" class="animate-spin" />
                            {/if}
                        </Button>
                        <Button onclick={() => page = "repairs"}>
                            Manage Repairs
                            {#if repairCount}
                                <Badge variant="secondary">{repairCount}</Badge>
                            {:else}
                                <CircleNotchIcon weight="bold" class="animate-spin" />
                            {/if}
                        </Button>
                    </div>
                </Card.Content>
            </Card.Root>

        {:else if page === "seasons"}
            <AdminHeader handleNavigate={handleNavigate}/>
            <SeasonsManager />

        {:else if page === "match_fields"}
            <AdminHeader handleNavigate={handleNavigate}/>
            <MatchScoutingFieldsManager />

        {:else if page === "pit_scouting_questions"}
            <AdminHeader handleNavigate={handleNavigate}/>
            <PitScoutingQuestionsManager/>

        {:else if page === "users"}
            <AdminHeader handleNavigate={handleNavigate}/>
            <UsersManager />

        {:else if page === "events"}
            <AdminHeader handleNavigate={handleNavigate}/>
            <EventManager />

        {:else if page === "match_scouting"}
            <AdminHeader handleNavigate={handleNavigate}/>
            <MatchScoutingSubmissionsManager />

        {:else if page === "pit_scouting"}
            <AdminHeader handleNavigate={handleNavigate}/>
            <PitScoutingDataManager />

        {:else if page === "reports"}
            <AdminHeader handleNavigate={handleNavigate}/>
            <ReportsManager />

        {:else if page === "repairs"}
            <AdminHeader handleNavigate={handleNavigate}/>
            <RepairsManager />

        {/if}
    {:else}
        <CircleNotchIcon weight="bold" class="animate-spin" size={32} />
    {/if}
</PageContainer>

<AlertDialog.Root open={show_warning_dialog}>
    <AlertDialog.Content>
        <AlertDialog.Title>Open Scouting Administration</AlertDialog.Title>
        <AlertDialog.Description>By continuing, understand that changes made here are irreversible, and may cause unintended consequences. Know what you're doing and proceed with caution.</AlertDialog.Description>
        
        <AlertDialog.Footer>
            <AlertDialog.Action onclick={() => {show_warning_dialog = false}}>Continue</AlertDialog.Action>
        </AlertDialog.Footer>
    </AlertDialog.Content>
</AlertDialog.Root>