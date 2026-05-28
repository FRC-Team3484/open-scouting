<!-- 
@component
The authentication section on the start page

TODO: Implement organization support
TODO: Actually load profile picture from server

Props:
    - `handleNavigate` (function) - The function for changing the authentication page
    - `setUser` (function) - The function for setting the user
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { ArrowRightIcon, SignOutIcon, SignInIcon } from "phosphor-svelte";

    import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte"
	import Label from "$lib/components/ui/label/label.svelte"
	import * as Card from "$lib/components/ui/card/index.js";
    import * as Avatar from "$lib/components/ui/avatar/index.js";
	import Skeleton from "../ui/skeleton/skeleton.svelte";

	import { signOut, validateTokenOnline } from "$lib/utils/user";
	import { getUserOrganizationsOrganizationsMeListGet } from "$lib/api/organizations/organizations";


    interface Props {
        handleNavigate: (nextPage: string) => void;
        setUser: (username: string, team_number: number, uuid: string | null) => void;
    }
    let { handleNavigate, setUser }: Props = $props();

    let user: any = $state(null);
    let organizations: any = $state(null);

    let organization_value = {"name":"default", "id":"0"};

    let username = $state("");
    let teamNumber = $state("");

    /**
     * Continues to the next page
     */
    function continueForward() {
        setUser(username, parseInt(teamNumber), null);
        handleNavigate("year");
    };
    
    /**
     * When the component mounts, get the user's information
     */
    onMount(async () => {
        try {
            user = await validateTokenOnline();
            // if (user) {
                //     organizations = await getUserOrganizationsOrganizationsMeListGet();
                // }
        } catch (error) {
            console.error(error);
        }
    });
</script>

<div class="flex flex-col gap-4 my-4">
    <div class="flex flex-col md:flex-row gap-4">
        <Card.Root class="text-left min-w-64">
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
                <Button disabled={username.trim() !== "" && teamNumber.trim() !== ""} onclick={continueForward}>
                    <ArrowRightIcon weight="bold" /> Continue
                </Button>
            </Card.Footer>
        </Card.Root>

        <p class="block md:hidden font-bold">Or...</p>

        <Card.Root class="text-left min-w-64">
            <Card.Header>
                <Card.Title>Sign In</Card.Title>
                <Card.Description>Use Open Scouting with an account</Card.Description>
            </Card.Header>

            <Card.Content class="flex flex-col gap-2">
                {#if user === null}
                    <Skeleton class="w-1/2" />
                {:else if user}
                    <p class="text-lg">Signed in as <strong>{user.username}</strong></p>

                    <!-- {#if organizations === null}
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
                    {/if} -->
                {:else}
                    <p>Not signed in</p>
                {/if}
            </Card.Content>

            <Card.Footer class="flex flex-row gap-2 mt-auto flex-wrap">
                {#if user}
                    <Button variant="outline" onclick={async () => {await signOut(); window.location.reload()}}>
                        <SignOutIcon weight="bold" />
                        Sign Out
                    </Button>
                    <Button onclick={() => {setUser(user.username, user.team_number, user.uuid); handleNavigate("year")}}>
                        <Avatar.Root>
                            <!-- TODO: Actually load avatar from user account -->
                            <!-- <Avatar.Image src={`https://github.com/${user.username}.png`} alt={user.username} /> -->
                            <Avatar.Fallback>{user.username.substring(0, 1)}</Avatar.Fallback>
                        </Avatar.Root>
                        
                        Continue as {user.username} <ArrowRightIcon weight="bold" />
                    </Button>
                {:else}
                    <Button href="/authentication">Sign In <SignInIcon weight="bold" /></Button>
                {/if}
            </Card.Footer>
        </Card.Root>
    </div>
</div>
