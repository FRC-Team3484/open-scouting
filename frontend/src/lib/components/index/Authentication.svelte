<script lang="ts">
    import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte"
	import Label from "$lib/components/ui/label/label.svelte"
	import * as Card from "$lib/components/ui/card/index.js";
    import * as Avatar from "$lib/components/ui/avatar/index.js";
    import * as Select from "$lib/components/ui/select/index.js";
    import * as Tabs from "$lib/components/ui/tabs";

	import { ArrowRight, ArrowLeft, Building, SignOut, SignIn } from "phosphor-svelte";
	import { signOut, validateTokenOnline } from "$lib/utils/user";
	import { onMount } from "svelte";
	import { apiFetch, theBlueAllianceApiFetch } from "$lib/utils/api";
	import Skeleton from "../ui/skeleton/skeleton.svelte";
	import Separator from "../ui/separator/separator.svelte";

    let { handleNavigate, setUser } = $props();

    let user: any = $state(null);
    let organizations: any = $state(null);

    let organization_value = {"name":"default", "id":"0"};

    let username = $state("");
    let teamNumber = $state("");
    let canContinue = $state(false);

    $effect(() => {
        canContinue = username.trim() !== "" && teamNumber.trim() !== "";
    });

    function continueForward() {
        setUser(username, parseInt(teamNumber), null);
        handleNavigate("year");
    };

    onMount(async () => {
        try {
            user = await validateTokenOnline();
            if (user) {
                const response = await apiFetch(`/organization/me/list`, {
                    token: await localStorage.getItem("access_token"),
                });
                organizations = response;
            }
        } catch (error) {
            console.error(error);
        }
    });
</script>

<div class="flex flex-col gap-4 mt-4">
    <div class="flex flex-col md:flex-row gap-4">
        <Card.Root class="max-w-128 p-4 min-w-64 text-left">
            <Card.Header>
                <Card.Title>Continue Without Account</Card.Title>
                <Card.Description>Use Open Scouting without an account</Card.Description>
            </Card.Header>

            <Card.Content class="flex flex-col gap-2">
                <Label for="username">Username</Label>
                <Input id="username" type="text" placeholder="Username" bind:value={username} />

                <Label for="team_number">Team Number</Label>
                <Input id="team_number" type="text" placeholder="Team Number" bind:value={teamNumber} />
            </Card.Content>

            <Card.Footer>
                <Button disabled={!canContinue} onclick={continueForward}>
                    <ArrowRight weight="bold" /> Continue
                </Button>
            </Card.Footer>
        </Card.Root>

        <Card.Root class="max-w-128 p-4 min-w-64 text-left">
            <Card.Header>
                <Card.Title>Authentication</Card.Title>
                <Card.Description>Use Open Scouting with an account</Card.Description>
            </Card.Header>

            <Card.Content class="flex flex-col gap-2">
                {#if user === null}
                    <Skeleton class="w-1/2" />
                {:else if user}
                    <p class="text-lg">Signed in as <strong>{user.username}</strong></p>

                    {#if organizations === null}
                        <Skeleton class="w-1/2" />
                    {:else if organizations.length === 0}

                    {:else}
                        <div class="flex flex-row gap-2 items-center">
                            <div class="flex flex-col gap-2">
                                <p>Organization</p>
                                <p class="text-muted-foreground text-sm">Organizations allow you to use custom match and pit scouting questions specific for your team</p>
                            </div>

                            <Select.Root type="single" name="organization" id="organization" bind:value={organization_value}>
                                <Select.Trigger>
                                    {organization_value.name}
                                </Select.Trigger>
                                <Select.Content>
                                    <Select.Label>Organizations</Select.Label>
                                    <Select.Item value={{"name":"default", "id":"0"}} label="None" />
                                    {#each organizations as organization}
                                        <Select.Item value={{"name":organization.name, "id":organization.id}} label={organization.name} />
                                    {/each}
                                </Select.Content>
                            </Select.Root>
                        </div>
                    {/if}
                {:else}
                    <p>Not signed in</p>
                {/if}
            </Card.Content>

            <Card.Footer class="flex flex-row gap-2 mt-auto">
                {#if user}
                    <Button variant="outline" onclick={async () => {await signOut(); window.location.reload()}}>
                        <SignOut weight="bold" />
                        Sign Out
                    </Button>
                    <Button onclick={() => {setUser(user.username, user.team_number, user.uuid); handleNavigate("year")}}>
                        <Avatar.Root>
                            <!-- TODO: Actually load avatar from user account -->
                            <Avatar.Image src={`https://github.com/${user.username}.png`} alt={user.username} />
                            <Avatar.Fallback>SC</Avatar.Fallback>
                        </Avatar.Root>
                        
                        Continue as {user.username} <ArrowRight weight="bold" />
                    </Button>
                {:else}
                    <Button href="/authentication">Sign In <SignIn weight="bold" /></Button>
                {/if}
            </Card.Footer>
        </Card.Root>
    </div>
</div>
