<script lang="ts">
	import Button from "../ui/button/button.svelte";
	import Logo from "./Logo.svelte";
	import { ArrowRight, List } from "phosphor-svelte";
	import Separator from "../ui/separator/separator.svelte";
	import User from "./User.svelte";
	import ExperimentalWarning from "./ExperimentalWarning.svelte";
    import * as Sheet from "$lib/components/ui/sheet/index.js";
</script>

<div class="hidden md:flex fixed top-0 left-0 right-0 w-full h-24 flex-row justify-between items-center border-1 bg-card/50 border-accent rounded-b-lg backdrop-blur-lg p-2 z-10 print:hidden">
    <div class="flex flex-row gap-4 items-center">
        <Logo text={true} style="tiny" href="/" />
        <ExperimentalWarning />

        <Button variant="outline" href="/" class="ml-4">Home</Button>
        <Button variant="outline" href="/data">View Data</Button>
        <!-- <Button variant="outline" href="/" disabled>Events</Button> -->
    </div>

    <div class="flex flex-row gap-4 items-center">
    </div>

    <div class="flex flex-row gap-4 items-center">
        <Button variant="default" href="/start"><ArrowRight weight="bold" /> Get Started</Button>

        <User show_text={false} />
    </div>
</div>

<div class="flex md:hidden fixed top-0 left-0 right-0 w-full h-16 flex-row justify-between items-center border-1 bg-background/50 border-accent rounded-b-lg backdrop-blur-lg p-2 z-10 print:hidden">
    <div class="flex flex-row gap-2 items-center">
        <Sheet.Root>
            <Sheet.Trigger class="p-2 text-md border-1 border-border rounded-md bg-input/30">
                <List weight="bold"/>
            </Sheet.Trigger>
            <Sheet.Content class="flex flex-col gap-4 p-4 justify-between" side="left">
                <div class="flex flex-col gap-4">
                    <div class="flex flex-row gap-4 items-center justify-between">
                        <Logo text={false} style="tiny" href="/" />
                    </div>
                    <div class="flex flex-row gap-4 items-center">
                        <User show_text={true} />
                    </div>
                    <Separator orientation="horizontal" />
                    <Sheet.Close><Button variant="outline" href="/" class="w-full">Home</Button></Sheet.Close>
                    <Sheet.Close><Button variant="outline" href="/data" class="w-full">View Data</Button></Sheet.Close>
                    <!-- <Sheet.Close><Button variant="outline" href="/" class="w-full" disabled>Events</Button></Sheet.Close> -->
                </div>

                <ExperimentalWarning/>
            </Sheet.Content>
        </Sheet.Root>
        <ExperimentalWarning size="sm" />
    </div>

    <Button variant="default" href="/start"><ArrowRight weight="bold" /> Get Started</Button>
</div>