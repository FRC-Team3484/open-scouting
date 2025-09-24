<script lang="ts">
    import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte"
	import Label from "$lib/components/ui/label/label.svelte"
	import * as Card from "$lib/components/ui/card/index.js";
    import * as Avatar from "$lib/components/ui/avatar/index.js";
    import * as Select from "$lib/components/ui/select/index.js";

	import { ArrowRight, ArrowLeft, Building } from "phosphor-svelte";
	import { validateTokenOnline } from "$lib/user";
	import { onMount } from "svelte";

    let user;

    let value = "item-1";

    onMount(async () => {
        user = await validateTokenOnline();
    })

    export let handleNavigate: (next: string) => void;
</script>

<div class="flex flex-col gap-4">
    <Button onclick={() => handleNavigate("welcome")} class="max-w-fit" variant="ghost"><ArrowLeft weight="bold" /> Start Over</Button>

    <div class="flex flex-col md:flex-row gap-4">
        <Card.Root class="max-w-128 p-4">
            <Card.Header>
                <Card.Title>Continue Without Account</Card.Title>
                <Card.Description>Use Open Scouting without an account</Card.Description>
            </Card.Header>

            <Card.Content class="flex flex-col gap-2">
                <Label for="username">Username</Label>
                <Input id="username" type="text" placeholder="Username"/>

                <Label for="team_number">Team Number</Label>
                <Input id="team_number"type="text" placeholder="Team Number"/>
            </Card.Content>

            <Card.Footer>
                <Button><ArrowRight weight="bold" /> Continue</Button>
            </Card.Footer>
        </Card.Root>

        <Card.Root class="max-w-128 p-4">
            <Card.Header>
                <Card.Title>Authentication</Card.Title>
                <Card.Description>Sign in or create an account to use Open Scouting with</Card.Description>
            </Card.Header>

            <Card.Content class="flex flex-col gap-2">
                {#if user}
                    <p>Signed in as <strong>{user.username}</strong></p>

                    <p class="text-lg">Organizations</p>
                    <p class="text-muted-foreground text-sm">Organizations allow you to use custom match and pit scouting questions specific for your team</p>

                    <Label for="organization">Organization</Label>
                    <Select.Root type="single" name="organization" id="organization" bind:value>
                        <Select.Trigger>
                            {value}
                        </Select.Trigger>
                        <Select.Content>
                            <Select.Item value="item-1">Item 1 <span class="text-muted-foreground">Primary</span></Select.Item>
                            <Select.Item value="item-2">Item 2</Select.Item>
                            <Select.Item value="item-3">Item 3</Select.Item>
                        </Select.Content>
                    </Select.Root>

                {:else}
                    <p>Not signed in</p>
                {/if}
            </Card.Content>

            <Card.Footer class="flex flex-col gap-2">
                {#if user}
                    <Button>
                        <Avatar.Root>
                            <!-- TODO: Actually load avatar from user account -->
                            <Avatar.Image src={`https://github.com/${user.username}.png`} alt={user.username} />
                            <Avatar.Fallback>SC</Avatar.Fallback>
                        </Avatar.Root>
                        
                        Continue as {user.username} <ArrowRight weight="bold" /></Button>
                {/if}

            </Card.Footer>
        </Card.Root>
    </div>
</div>