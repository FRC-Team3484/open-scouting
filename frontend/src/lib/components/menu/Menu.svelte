<script lang="ts">
	import { fade, slide } from "svelte/transition";
	import { toggleMode, mode } from "mode-watcher";

	import Button from "../ui/button/button.svelte";
	import Separator from "../ui/separator/separator.svelte";
    import { Archive, ArrowRight, Article, Bug, CheckCircle, CircleNotch, Clock, DiscordLogo, FloppyDisk, GithubLogo, House, List, Moon, Notepad, Sun, Warning, X, XCircleIcon } from "phosphor-svelte";

	import AboutDrawer from "./AboutDrawer.svelte";
	import ManageDataDrawer from "./ManageDataDrawer.svelte";
    import * as Sheet from "$lib/components/ui/sheet";

	import { menuState } from "$lib/stores/menu";
	import User from "../generic/User.svelte";
	import { online } from "svelte/reactivity/window";
	import { toast } from "svelte-sonner";
	import { changelogDialogOpen } from "$lib/stores/dialog";
	import SyncingToggleDrawer from "./SyncingToggleDrawer.svelte";

    let user = null;

    let menu_open: boolean = $state(false);
    let wasOnline = $state(online.current);

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

    $effect(() => {
        const now = online.current;

        if (!wasOnline && now) {
            toast.success("You're back online", { description: "All features are now available" });
        } else if (wasOnline && !now) {
            toast.error("You are now offline", { description: "Some features may be unavailable and data may be out of date. Reconnect to the internet to sync data" });
        }

        wasOnline = now;
    });
</script>

{#if !menu_open}
    <Button
        variant="outline"
        class={`fixed bottom-2 right-2 z-999 !aspect-square !rounded-full md:!w-16 md:!h-16 !w-10 !h-10 backdrop-blur-lg ${$menuState.state === "warning" ? "!bg-amber-500/30 !border-amber-700" : ""}`}
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
{/if}


<Sheet.Root bind:open={menu_open}>
    <Sheet.Content class="max-h-[80vh] overflow-y-scroll lg:mx-64 2xl:mx-128 border-1 p-4 rounded-t-lg" side="bottom">
        <div class="flex flex-col gap-4 mt-4 overflow-y-scroll pr-2">
            <div class="flex flex-row gap-4 justify-between items-center">
                <div class="flex flex-row gap-2 items-center">
                    <User show_text={true} />
                </div>
            </div>

            {#if $menuState.status}
                <div class="flex flex-row gap-2 items-center justify-between flex-wrap" transition:slide>
                    <div class="flex flex-row gap-2 items-center">
                        {#if $menuState.state === "ready"}
                            <CheckCircle weight="bold"/>
                        {:else if $menuState.state === "loading"}
                            <CircleNotch weight="bold" class="animate-spin"/>
                        {:else if $menuState.state === "warning"}
                            <Warning weight="bold"/>
                        {/if}
                        <p>{$menuState.status}</p>
                    </div>
                    <Button variant="outline" size="sm" onclick={() => menuState.set({state: "ready", status: "", close: true})}><XCircleIcon weight="bold" /> Hide</Button>
                </div>
            {/if}

            <Separator orientation="horizontal" />

            <div class="flex flex-row gap-2 flex-wrap">
                <Button variant="outline" onclick={toggleMode}>
                    {#if mode.current === "dark"}
                        <Sun class="h-[1.2rem] w-[1.2rem]"/>
                        <span>Light Mode</span>
                    {:else}
                        <Moon class="h-[1.2rem] w-[1.2rem]"/>
                        <span>Dark Mode</span>
                    {/if}
                </Button>

                <SyncingToggleDrawer />
            </div>

            <Separator orientation="horizontal" />

            <div class="flex flex-row gap-2 flex-wrap">
                <Sheet.Close><Button href="/start"><ArrowRight weight="bold" /> Start</Button></Sheet.Close>
                <Sheet.Close><Button variant="outline" href="/"><House weight="bold" /> Home</Button></Sheet.Close>
            </div>

            <div class="flex flex-row gap-2 flex-wrap">
                <Button variant="outline" href="https://discord.gg/M3wESZUP35"><DiscordLogo weight="bold" /> Discord</Button>
                <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting"><GithubLogo weight="bold" /> Source Code</Button>
                <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting/issues"><Bug weight="bold" /> Issues</Button>
                <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting/releases"><Article weight="bold" /> Releases</Button>
                <Button variant="outline" href="https://open-scouting-legacy.nfoert.dev"><Archive weight="bold" /> Legacy v1</Button>
            </div>

            <Separator orientation="horizontal" />

            <div class="flex flex-col gap-4 mb-12">
                <Button variant="outline" onclick={() => {$changelogDialogOpen = true; menu_open = false}}><Notepad weight="bold" /> Changelog</Button>
                <ManageDataDrawer/>
                <AboutDrawer />
            </div>
        </div>
    </Sheet.Content>
</Sheet.Root>