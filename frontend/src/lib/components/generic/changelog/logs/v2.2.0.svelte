<script lang="ts">
	import { BroomIcon, FlagIcon, KeyIcon, LockIcon, StarIcon, UserIcon, WrenchIcon } from "phosphor-svelte";
	import MajorFeature from "../MajorFeature.svelte";
	import Generic from "./Generic.svelte";
</script>

{#snippet summary()}
    <p>This feature release of Open Scouting improves all aspects of user authentication and profile management. It also adds user session tracking, content reporting, repair mode on the admin page, and includes a major frontend cleanup.</p>
{/snippet}

{#snippet features()}
    <MajorFeature text="Frontend Cleanup">
        {#snippet icon()}
            <BroomIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Session and Authentication Tokens">
        {#snippet icon()}
            <KeyIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Authentication Improvements">
        {#snippet icon()}
            <LockIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Profile Page">
        {#snippet icon()}
            <UserIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Feature Page">
        {#snippet icon()}
            <StarIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Content Reporting">
        {#snippet icon()}
            <FlagIcon weight="bold" />
        {/snippet}
    </MajorFeature>

    <MajorFeature text="Repair Mode">
        {#snippet icon()}
            <WrenchIcon weight="bold" />
        {/snippet}
    </MajorFeature>
{/snippet}

{#snippet details()}    
    <ul class="list-disc list-inside ml-4">
        <li>Session tokens track user submitted content</li>
        <li>Authentication has been fully rewritten, with support for email verification and passkeys</li>
        <li>User profile page allows for editing user and profile information</li>
        <li>Content reporting and database repair mode on the admin page</li>
    </ul>
{/snippet}

<Generic summary={summary} features={features} details={details} />