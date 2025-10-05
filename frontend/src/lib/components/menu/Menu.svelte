<script lang="ts">
    import * as Drawer from "$lib/components/ui/drawer";
	import { Article, Bug, Clock, GithubLogo, House, List, Moon, Sun, X } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import ThemeSwitcherIcon from "../generic/ThemeSwitcherIcon.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import { toggleMode, mode } from "mode-watcher";
</script>

<Drawer.Root shouldScaleBackground={false}>
    <Drawer.Trigger class="absolute bottom-2 right-2">
        <Button variant="outline" class="!aspect-square !rounded-full md:!w-16 md:!h-16 !w-10 !h-10 backdrop-blur-lg">
            <List weight="bold" class="md:!w-8 md:!h-8 !w-6 !h-6"/>
        </Button>
    </Drawer.Trigger>
    <Drawer.Content class="h-auto lg:mx-64 border-1 p-4 pb-16">
        <div class="flex flex-col gap-4 mt-4">
            <div class="flex flex-row gap-4 justify-between items-center">
                <div class="flex flex-row gap-2 items-center">
                    <Clock weight="bold"/>
                    <p class="text-lg font-bold">{new Intl.DateTimeFormat('en-US', { hour: '2-digit', minute: '2-digit' }).format(new Date())}</p>
                </div>

                <Drawer.Close><Button variant="outline" size="icon" class="!p-6 rounded-full"><X weight="bold" class="!w-6 !h-6"/></Button></Drawer.Close>
            </div>

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

            <div class="flex flex-row gap-4 flex-wrap">
                <Button variant="outline" href="/"><House weight="bold" /> Home</Button>
                <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting"><GithubLogo weight="bold" /> Source Code</Button>
                <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting/issues"><Bug weight="bold" /> Issues</Button>
                <Button variant="outline" href="https://github.com/FRC-Team3484/open-scouting/releases"><Article weight="bold" /> Releases</Button>
            </div>
        </div>
    </Drawer.Content>
</Drawer.Root>