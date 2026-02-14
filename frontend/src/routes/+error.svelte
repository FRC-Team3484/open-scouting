<script lang="ts">
    import "../app.css";
	import { page } from "$app/state";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import Button from "$lib/components/ui/button/button.svelte";
	import { Bug, House, SmileySad } from "phosphor-svelte";


</script>

<PageContainer>
    <div class="flex flex-col gap-2 items-center">
        <p class="text-8xl font-mono">{page.status}</p>
        <p class="mb-2 text-lg">{page.error?.message}</p>
        
        {#if page.status === 404}
            <p>The page you're looking for doesn't exist</p>
            <p>Please check the URL and try again</p>
        {:else}
            <p>This probably wasn't supposed to happen</p>
        {/if}
        <div class="flex flex-row gap-2 mb-8">
            <Button href="/"><House weight="bold" /> Home</Button>
            <Button href="https://github.com/FRC-Team3484/open-scouting/issues" variant="outline"><Bug weight="bold" /> Issues</Button>
        </div>

        <SmileySad weight="bold" size={48} />
    </div>
</PageContainer>