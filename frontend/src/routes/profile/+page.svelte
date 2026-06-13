<!-- 
The profile page

Allows for editing profile details, changing password, and updating settings
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { goto } from "$app/navigation";
	import { toast } from "svelte-sonner";
	import { GearIcon, SignOutIcon, UserIcon } from "phosphor-svelte";
    
    import * as Card from "$lib/components/ui/card/index.js";
    import Button from "$lib/components/ui/button/button.svelte";
	import Separator from "$lib/components/ui/separator/separator.svelte";
    
    import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import Logo from "$lib/components/generic/Logo.svelte";

	import { getAuthenticationStatus, getSettings, getUser, signOut } from "$lib/utils/user";
	import { type UserResponse, type UserSetting } from "$lib/api/model";
	import { getUserSettingsUsersMeGetSettingsGet } from "$lib/api/auth/auth";
	import ProfileSection from "$lib/components/profile/pages/ProfileSection.svelte";
	import SettingsSection from "$lib/components/profile/pages/SettingsSection.svelte";


    let section: "profile" | "settings" = $state("profile");

    let user: UserResponse | null = getUser();
    let authenticated: boolean = getAuthenticationStatus();
    let settings: {[key: string]: UserSetting[]} = $state(parseSettings(getSettings()));

    /**
     * Parses the settings into sections
     * 
     * @param settings The settings to parse
     */
    function parseSettings(settings: UserSetting[]): Record<string, UserSetting[]> {
        return settings.reduce((acc, setting) => {
            const section = setting.section ?? "Uncategorized";

            if (!acc[section]) {
                acc[section] = [];
            }

            acc[section].push(setting);
            return acc;
        }, {} as Record<string, UserSetting[]>);
    }

    /**
     * Gets the current settings from the server
     */
    async function getNewSettings() {
        await getUserSettingsUsersMeGetSettingsGet().then((response) => {
            if (response.status === 200) {
                settings = parseSettings(response.data);
            }
        })
    }

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
                {#if section == "profile" && user}
                    <ProfileSection user={user} />

                {:else if section == "settings"}
                    <SettingsSection settings={settings} getNewSettings={getNewSettings} />
                {/if}
            </Card.Content>
        </Card.Root>
    </div>
</PageContainer>