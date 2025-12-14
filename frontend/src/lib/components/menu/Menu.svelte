<script lang="ts">
	import { fade, slide } from "svelte/transition";
	import { toggleMode, mode } from "mode-watcher";

	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";
    import { ArrowRight, Article, Bug, CheckCircle, CircleNotch, Clock, DiscordLogo, FloppyDisk, GithubLogo, House, List, Moon, Sun, Warning, X } from "phosphor-svelte";

	import AboutDrawer from "./AboutDrawer.svelte";
	import ManageDataDrawer from "./ManageDataDrawer.svelte";
    import * as Drawer from "$lib/components/ui/drawer";

	import { menuState } from "$lib/stores/menu";
	import User from "../generic/User.svelte";

    let user = null;

    let menu_open: boolean = false;

    menuState.subscribe((value) => {
        if (value.close) {
            setTimeout(() => {
                menuState.set({
                    state: "ready",
                    status: "",
                    close: false
                });
            }, 3000)
        }
    });
</script>

<Button
    variant="outline"
    class={`fixed bottom-2 right-2 !aspect-square !rounded-full md:!w-16 md:!h-16 !w-10 !h-10 backdrop-blur-lg ${$menuState.state === "warning" ? "!bg-amber-500/30 !border-amber-700" : ""}`}
    onclick={() => menu_open = true}
>
    {#key $menuState.state}
        <div transition:fade|local={{ duration: 150 }}>
            {#if $menuState.state === "ready"}
                <List weight="bold" class="md:!w-8 md:!h-8 !w-6 !h-6" />
            {:else if $menuState.state === "loading"}
                <CircleNotch weight="bold" class="animate-spin md:!w-6 md:!h-6 !w-4 !h-4" />
            {:else if $menuState.state === "warning"}
                <Warning weight="bold" class="animate-pulse md:!w-6 md:!h-6 !w-4 !h-4" />
            {/if}
        </div>
    {/key}
</Button>


<Drawer.Root shouldScaleBackground={false} bind:open={menu_open}>
    <Drawer.Content class="h-auto lg:mx-64 border-1 p-4 pb-16">
        <div class="flex flex-col gap-4 mt-4">
            <div class="flex flex-row gap-4 justify-between items-center">
                <div class="flex flex-row gap-2 items-center">
                    <User show_text={true} />
                </div>

                <Drawer.Close><Button variant="outline" size="icon" class="!p-6 rounded-full"><X weight="bold" class="!w-6 !h-6"/></Button></Drawer.Close>
            </div>

            {#if $menuState.status}
                <div class="flex flex-row gap-2 items-center" transition:slide>
                    {#if $menuState.state === "ready"}
                        <CheckCircle weight="bold"/>
                    {:else if $menuState.state === "loading"}
                        <CircleNotch weight="bold" class="animate-spin"/>
                    {:else if $menuState.state === "warning"}
                        <Warning weight="bold"/>
                    {/if}
                    <p>{$menuState.status}</p>
                </div>
            {/if}

            <Separator orientation="horizontal" />

            <div class="flex flex-row gap-4 flex-wrap">
                <Button variant="outline" onclick={toggleMode}>
                    {#if mode.current === "dark"}
                        <Sun class="h-[1.2rem] w-[1.2rem]"/>
                        <span>Light Mode</span>
                    {:else}
                        <Moon class="h-[1.2rem] w-[1.2rem]"/>
                        <span>Dark Mode</span>
                    {/if}
                </Button>
            </div>

            <Separator orientation="horizontal" />

            <div class="flex flex-row gap-2 flex-wrap">
                <Button href="/start"><ArrowRight weight="bold" /> Start</Button>
                <Button variant="outline" href="/"><House weight="bold" /> Home</Button>
                <Button variant="outline" href="https://discord.gg/M3wESZUP35"><DiscordLogo weight="bold" /> Discord</Button>
                <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting"><GithubLogo weight="bold" /> Source Code</Button>
                <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting/issues"><Bug weight="bold" /> Issues</Button>
                <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting/releases"><Article weight="bold" /> Releases</Button>
            </div>

            <Separator orientation="horizontal" />

            <div class="flex flex-col gap-4">
                <ManageDataDrawer/>
                <AboutDrawer />
            </div>
        </div>
    </Drawer.Content>
</Drawer.Root>