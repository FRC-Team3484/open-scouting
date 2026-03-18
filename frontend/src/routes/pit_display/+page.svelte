<script lang="ts">
	import Logo from "$lib/components/generic/Logo.svelte";
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";
	import { db } from "$lib/utils/db";
	import type Dexie from "dexie";
    import QR from '@svelte-put/qr/svg/QR.svelte';
	import { onMount } from "svelte";
	import { CalendarBlank, MapPin } from "phosphor-svelte";

    let year: string = $state("");
    let event_code: string = $state("");

    let event: null | Dexie.Table = $state(null);

    async function getUrlInfo() {
        let url = new URL(window.location.href);
        year = url.searchParams.get("year");
        event_code = url.searchParams.get("event_code");
    }

    async function getEventInfo() {
        event = await db.event.filter(ev => ev.year === parseInt(year) && ev.event_code === event_code).first();

        
    }

    onMount(async () => {
        await getUrlInfo();
        await getEventInfo();
    })
</script>

<PageContainer>
    <div class="flex flex-row">
        {#if event}
            <div class="flex flex-col gap-4 text-right items-end w-[50vw] p-8">
                <div class="flex flex-row gap-4 items-center">
                    <Logo text={false} style="tiny" href="/" />
                    <p class="text-4xl font-mono font-bold">Open Scouting</p>
                </div>
                <p class="text-xl flex-wrap">An open source application for easier scouting at FIRST robotics competitions</p>

                <p class="text-lg flex-wrap">Created by 3484 Short Circuit</p>

                <p class="text-md text-muted-foreground">github.com/FRC-Team3484/open-scouting</p>
            </div>

            <Separator orientation="vertical" class="mx-6 print:border-black print:border" />
            
            <div class="flex flex-col gap-4 text-left items-left w-[50vw] p-8">
                <p class="text-4xl font-bold">{event.name}</p>
                <div class="flex flex-row gap-2 items-center">
                    <MapPin weight="bold" /> 
                    <p>{event.type} - {event.city}, {event.country}</p>
                </div>
                <div class="flex flex-row gap-2 items-center">
                    <CalendarBlank weight="bold" />
                    <p> {event.start_date} - {event.end_date}</p>
                </div>

                <div class="flex flex-row gap-2">
                    <div class="flex flex-col gap-2 items-center">
                        <QR data={`${window.location.origin}/data?year=${year}&event_codes=${event.event_code}`} width={200} height={200} />
                        <p>View data for this event</p>
                    </div>

                    <div class="flex flex-col gap-2 items-center">
                        <QR data={`${window.location.origin}/start?year=${year}&event_code=${event.event_code}&event_name=${event.name}`} width={200} height={200} />
                        <p>Scout at this event</p>
                    </div>
                </div>

            </div>
        {:else}
            <p>No event found</p>
        {/if}
    </div>
</PageContainer>