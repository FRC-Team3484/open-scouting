<!-- 
The profile page

Allows for editing profile details, changing password, and updating settings
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { toast } from "svelte-sonner";
	import { GearIcon, PencilIcon, SignOutIcon, UserIcon } from "phosphor-svelte";
    
    import * as Card from "$lib/components/ui/card/index.js";
    import Button from "$lib/components/ui/button/button.svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";
    
    import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import Logo from "$lib/components/generic/Logo.svelte";
	import Section from "$lib/components/profile/Section.svelte";

	import { getAuthenticationStatus, getUser, signOut } from "$lib/utils/user";
	import { type UserResponse } from "$lib/api/model";
	import Badge from "$lib/components/ui/badge/badge.svelte";

    
    let section: "profile" | "settings" = $state("profile");

    let user: UserResponse | null = getUser();
    let authenticated: boolean = getAuthenticationStatus();

    onMount(() => {
        if (!authenticated) {
            goto("/");
            toast.error("You must be signed in to view this page.");
        }
    })
</script>

<PageContainer>
    <div class="flex flex-row gap-4 h-[75vh] w-[75vw]">
        <div class="flex flex-col gap-4">
            <Card.Root>
                <Card.Content>
                    <div class="flex flex-row gap-4 items-center">
                        <Logo text={false} style="tiny" href="/" />
                        <p class="font-bold text-lg text-left">Profile <br>Management</p>
                    </div>
                </Card.Content>
            </Card.Root>

            <Card.Root class="flex-2">
                <Card.Content>
                    <div class="flex flex-col gap-2">
                        <Card.Root class="p-2">
                            <Card.Content class="p-2">
                                <div class="flex flex-row gap-2 items-center">
                                    <div class="w-8 h-8 bg-muted rounded-full flex items-center justify-center">{user?.username.charAt(0)}</div>

                                    <div class="flex flex-col gap-1 items-start">
                                        <p class="font-bold">{user?.username}</p>
                                        <p class="text-sm text-muted-foreground">{user?.email}</p>
                                    </div>
                                </div>
                            </Card.Content>
                        </Card.Root>

                        <Button variant="outline" onclick={() => signOut()}><SignOutIcon weight="bold" /> Sign Out</Button>

                        <Separator class="my-2" />

                        <Button variant={section == "profile" ? "outline" : "default"} disabled={section == "profile"} onclick={() => section = "profile"}><UserIcon weight="bold" /> Profile</Button>
                        <Button variant={section == "settings" ? "outline" : "default"} disabled={section == "settings"} onclick={() => section = "settings"}><GearIcon weight="bold" /> Settings</Button>
                    </div>
                </Card.Content>
            </Card.Root>
        </div>

        <Card.Root class="flex-2 items-start">
            <Card.Content class="text-left w-full h-full">
                {#if section == "profile"}
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

                {:else if section == "settings"}
                    <Section title="Settings" description="Your settings">
                        <div class="flex flex-col gap-2">
                            <p>Theme</p>
                            <p>Language</p>
                        </div>
                    </Section>
                {/if}
            </Card.Content>
        </Card.Root>
    </div>
</PageContainer>