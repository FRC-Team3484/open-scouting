<script lang="ts">
    import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte"
	import Label from "$lib/components/ui/label/label.svelte"
	import * as Card from "$lib/components/ui/card/index.js";

	import { ArrowRight, ArrowLeft } from "phosphor-svelte";

    export let handleNavigate: (next: string) => void;
</script>

<div class="flex flex-col gap-4">
    <Button onclick={() => handleNavigate("welcome")} class="max-w-fit" variant="ghost"><ArrowLeft weight="bold" /> Start Over</Button>

    <div class="flex flex-col md:flex-row gap-4">
        <Card.Root class="min-w-64 p-4">
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

        <Card.Root class="min-w-64 p-4">
            <Card.Header>
                <Card.Title>Authentication</Card.Title>
                <Card.Description>Sign in or create an account to use Open Scouting with</Card.Description>
            </Card.Header>
        </Card.Root>
    </div>
</div>