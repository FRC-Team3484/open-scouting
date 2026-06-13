<!-- 
@component
The profile section on the profile page, for editing user details

Props:
    - `user` (`UserResponse`) - The user
-->
<script lang="ts">
	import { PencilIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";
	import { Badge } from "$lib/components/ui/badge";

	import Section from "./BaseSection.svelte";
	import type { UserResponse } from "$lib/api/model";


    interface Props {
        user: UserResponse
    }
    let { user }: Props = $props();
</script>
<Section title="Profile" description="Your profile details">
    <div class="flex flex-col gap-2">
        <Card.Root>
            <Card.Content>
                <div class="flex flex-row gap-2">
                    <div class="group w-16 h-16 bg-muted rounded-full flex items-center justify-center relative overflow-hidden active:scale-90 transition-transform">
                        <p class="text-2xl text-white select-none">{user?.username.charAt(0)}</p>
                        <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity z-10"></div>
                        <PencilIcon weight="bold" class="absolute inset-0 m-auto text-white opacity-0 group-hover:opacity-100 transition-opacity z-20 text-3xl" />
                    </div>


                    <div class="flex flex-col gap-1 items-start">
                        <div class="flex flex-row gap-2">
                            <p class="font-bold text-lg">{user?.username}</p>

                            {#if user?.is_superuser}
                                <Badge class="bg-green-400/50">Superuser</Badge>
                            {/if}
                        </div>
                        <p class="text-md text-muted-foreground">{user?.email}</p>
                        <p class="text-md text-muted-foreground">Team: {user?.team_number}</p>
                    </div>
                </div>
            </Card.Content>
        </Card.Root>
    </div>
</Section>