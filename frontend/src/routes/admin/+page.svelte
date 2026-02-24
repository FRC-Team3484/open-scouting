<script lang="ts">
    import { env } from "$env/dynamic/public";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import { validateTokenOnline } from "$lib/utils/user";
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";
    import * as Card from "$lib/components/ui/card/index.js";
	import Button from "$lib/components/ui/button/button.svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";
	import SeasonsManager from "$lib/components/admin/SeasonsManager.svelte";
	import AdminHeader from "$lib/components/admin/AdminHeader.svelte";
	import Dialog from "$lib/components/generic/Dialog.svelte";
	import MatchScoutingFieldsManager from "$lib/components/admin/MatchScoutingFieldsManager.svelte";
	import PitScoutingQuestionsManager from "$lib/components/admin/PitScoutingQuestionsManager.svelte";
	import UsersManager from "$lib/components/admin/UsersManager.svelte";
	import EventManager from "$lib/components/admin/EventsManager.svelte";
	import MatchScoutingSubmissionsManager from "$lib/components/admin/MatchScoutingSubmissionsManager.svelte";

    let user = null;
    let page = $state("start");
    let show_warning_dialog = $state(!(env.PUBLIC_MODE == "dev"));

    onMount(async () => {
        user = await validateTokenOnline();
        if (!user.is_superuser) {
            toast.error("403: Forbidden", { duration: 5000 });
            window.location.href = "/";
        }
    });

    function handleNavigate(nextPage: string): void {
        page = nextPage;
    }

    function closeWarningDialog(): void {
        show_warning_dialog = false;
    }
</script>

<PageContainer>
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
        <h1>Pit Scouting</h1>

    {/if}
</PageContainer>

<Dialog 
    open={show_warning_dialog} 
    title="Open Scouting Administration" 
    description="By continuing, understand that changes made here are irreversible, and may cause unintended consequences. Know what you're doing and proceed with caution." 
    cancel_text=""
    submit_text="Continue"
    onSubmit={closeWarningDialog}
/>