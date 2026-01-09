<script lang="ts">
	import { onMount } from "svelte";
	import Button from "../ui/button/button.svelte";
	import Logo from "./Logo.svelte";
	import { signOut, validateTokenOnline } from "$lib/utils/user";
	import * as Avatar from "../ui/avatar/index.js";
	import Skeleton from "../ui/skeleton/skeleton.svelte";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
    import * as Drawer from "$lib/components/ui/drawer/index.js";
	import { ArrowRight, List, X } from "phosphor-svelte";
	import Separator from "../ui/separator/separator.svelte";
	import User from "./User.svelte";
	import ExperimentalWarning from "./ExperimentalWarning.svelte";
</script>

<div class="hidden md:flex fixed top-0 left-0 right-0 w-full h-24 flex-row justify-between items-center border-1 bg-card/50 border-accent rounded-b-lg backdrop-blur-lg p-2 z-10">
    <div class="flex flex-row gap-4 items-center">
        <Logo text={true} style="tiny" href="/" />
        <ExperimentalWarning />

        <Button variant="outline" href="/" class="ml-4">Home</Button>
        <Button variant="outline" href="/" disabled>View Data</Button>
        <Button variant="outline" href="/" disabled>Events</Button>
    </div>

    <div class="flex flex-row gap-4 items-center">
    </div>

    <div class="flex flex-row gap-4 items-center">
        <Button variant="default" href="/start"><ArrowRight weight="bold" /> Get Started</Button>

        <User show_text={false} />
    </div>
</div>

<div class="flex md:hidden fixed top-0 left-0 right-0 w-full h-16 flex-row justify-between items-center border-1 bg-background/50 border-accent rounded-b-lg backdrop-blur-lg p-2 z-10">
    <div class="flex flex-row gap-2 items-center">
        <Drawer.Root shouldScaleBackground={false} direction="left">
            <Drawer.Trigger class="p-2 text-md border-1 border-border rounded-md bg-input/30">
                <List weight="bold"/>
            </Drawer.Trigger>
            <Drawer.Content class="flex flex-col gap-4 p-4 justify-between">
                <div class="flex flex-col gap-4">
                    <div class="flex flex-row gap-4 items-center justify-between">
                        <Logo text={false} style="tiny" href="/" />
                        <Drawer.Close><Button variant="outline" size="icon"><X weight="bold"/></Button></Drawer.Close>
                    </div>
                    <div class="flex flex-row gap-4 items-center">
                        <User show_text={true} />
                    </div>
                    <Separator orientation="horizontal" />
                    <Button variant="outline" href="/">Home</Button>
                    <Button variant="outline" href="/" disabled>View Data</Button>
                    <Button variant="outline" href="/" disabled>Events</Button>
                </div>

                <ExperimentalWarning/>
            </Drawer.Content>
        </Drawer.Root>
        <ExperimentalWarning size="sm" />
    </div>

    <Button variant="default" href="/start"><ArrowRight weight="bold" /> Get Started</Button>
</div>