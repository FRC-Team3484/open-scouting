<script lang="ts">
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import { validateTokenOnline } from "$lib/utls/user";
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";
    import * as Card from "$lib/components/ui/card/index.js";
	import Button from "$lib/components/ui/button/button.svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";
	import OperationManager from "$lib/components/admin/OperationManager.svelte";
	import SeasonsManager from "$lib/components/admin/SeasonsManager.svelte";
	import AdminHeader from "$lib/components/admin/AdminHeader.svelte";

    let user = null;
    let page = $state("start");
    let operations = $state([]);

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

    function addOperation(name: string, description: string, operation: string, data: any): void {
        operations = [...operations, {name, description, operation, data}];
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
                    <Button disabled>Manage Match Scouting Fields</Button>
                    <Button disabled>Manage Pit Scouting Questions</Button>
                    <Separator orientation="horizontal" />
                    <Button disabled>Manage Users</Button>
                    <Button disabled>Manage Events</Button>
                    <Button disabled>Manage Match Data</Button>
                    <Button disabled>Manage Pit Scouting Data</Button>
                </div>
            </Card.Content>
        </Card.Root>

    {:else if page === "seasons"}
        <AdminHeader handleNavigate={handleNavigate}/>
        <SeasonsManager addOperation={addOperation} />
    {/if}

    <OperationManager bind:operations addOperation={addOperation} />
</PageContainer>