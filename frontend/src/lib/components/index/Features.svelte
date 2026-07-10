<!-- 
@component
Shows the features of Open Scouting on the index page
-->
<script lang="ts">
	import { ArrowRightIcon, BinocularsIcon, CloudSlashIcon, DotsThreeOutlineIcon, GithubLogoIcon, HardDrivesIcon, ScrewdriverIcon, UsersThreeIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";

    import match_scouting_1 from "$lib/assets/features/match_scouting_1.png";
    import pit_scouting_1 from "$lib/assets/features/pit_scouting_1.png";
    import data_view_1 from "$lib/assets/features/data_view_1.png";
    import more_1 from "$lib/assets/features/more_1.png";
	import FeatureCard from "./FeatureCard.svelte";
	import Button from "../ui/button/button.svelte";
</script>

<div class="flex flex-col gap-4 items-center">
    <p class="text-2xl font-bold">About Open Scouting</p>

    <div class="flex flex-row gap-4 items-center flex-wrap justify-center">
        <Card.Root>
            <Card.Content>
                <div class="flex flex-col gap-2 items-center w-16 md:w-20 aspect-square justify-center">
                    <GithubLogoIcon weight="bold" size={25} />
                    <p class="text-sm md:text-md">Open Source</p>
                </div>
            </Card.Content>
        </Card.Root>

        <Card.Root>
            <Card.Content>
                <div class="flex flex-col gap-2 items-center w-16 md:w-20 aspect-square justify-center">
                    <CloudSlashIcon weight="bold" size={25} />
                    <p class="text-sm md:text-md">Offline Support</p>
                </div>
            </Card.Content>
        </Card.Root>

        <Card.Root>
            <Card.Content>
                <div class="flex flex-col gap-2 items-center w-16 md:w-20 aspect-square justify-center">
                    <UsersThreeIcon weight="bold" size={25} />
                    <p class="text-sm md:text-md">Collaborative Scouting</p>
                </div>
            </Card.Content>
        </Card.Root>
    </div>

    <div class="flex flex-col lg:flex-row gap-4 items-center justify-center">
        <FeatureCard>
            {#snippet image()}
                <img src={match_scouting_1} alt="Match Scouting" class="w-32" />
            {/snippet}

            {#snippet title()}
                <BinocularsIcon weight="bold" />
                <p class="text-xl">Match Scouting</p>
            {/snippet}

            {#snippet content()}
                <ul class="list-disc list-inside">
                    <li>Scout robots at competitions, with clear sections and fields</li>
                    <li>If data is avaliable, team numbers can be autofilled from TBA's match schedule data</li>
                    <li>Match numbers are automatically incremented, and fields instantly reset after submitting a report</li>
                </ul>
            {/snippet}

            {#snippet footer()}
                <Button href="/start"><ArrowRightIcon weight="bold" /> Try Match Scouting</Button>
            {/snippet}
        </FeatureCard>

        <FeatureCard>
            {#snippet image()}
                <img src={pit_scouting_1} alt="Pit Scouting" class="w-32" />
            {/snippet}

            {#snippet title()}
                <ScrewdriverIcon weight="bold" />
                <p class="text-xl">Pit Scouting</p>
            {/snippet}

            {#snippet content()}
                <ul class="list-disc list-inside">
                    <li>Collaboratively scout team's pits at competitions, with automatic syncing between other scouts at the event</li>
                    <li>Quickly view what pits still need scouted</li>
                    <li>Supports image uploads, and optional pit scouting fields</li>
                </ul>
            {/snippet}

            {#snippet footer()}
                <Button href="/start"><ArrowRightIcon weight="bold" /> Try Pit Scouting</Button>
            {/snippet}
        </FeatureCard>
    </div>

    <div class="flex flex-col lg:flex-row gap-4 items-center justify-center">
        <FeatureCard>
            {#snippet image()}
                <img src={data_view_1} alt="Data View" class="w-32" />
            {/snippet}

            {#snippet title()}
                <HardDrivesIcon weight="bold" />
                <p class="text-xl">Data View</p>
            {/snippet}

            {#snippet content()}
                <ul class="list-disc list-inside">
                    <li>Quickly view match scouting data, with filters for seasons, events, and teams</li>
                    <li>View summaries for each team, and detailed charts for each stat</li>
                    <li>Compare data between teams, and view data for each team in one chart or table</li>
                    <li>JSON or CSV data export</li>
                </ul>
            {/snippet}

            {#snippet footer()}
                <Button href="/data"><ArrowRightIcon weight="bold" /> View Match Scouting Data</Button>
            {/snippet}
        </FeatureCard>

        <FeatureCard>
            {#snippet image()}
                <img src={more_1} alt="More" class="w-32" />
            {/snippet}

            {#snippet title()}
                <DotsThreeOutlineIcon weight="bold" />
                <p class="text-xl">And More</p>
            {/snippet}

            {#snippet content()}
                <ul class="list-disc list-inside">
                    <li>Custom event creation, in a filterable event list</li>
                    <li>Event page and live events display</li>
                    <li>User and profile mangement</li>
                    <li>Menu for quick navigation, local data magement, and the ability to disable data sync</li>
                    <li>Admin dashboaard for instant season setup</li>
                </ul>
            {/snippet}
        </FeatureCard>
    </div>
</div>