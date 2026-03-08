<script lang="ts">
    import icon_rounded from "$lib/assets/icon_rounded.png"
	import { VERSION } from "$lib/utils/constants";

    import * as Sheet from "$lib/components/ui/sheet";
	import { DotsThreeOutline, XCircle } from "phosphor-svelte";
	import Button from "../ui/button/button.svelte";
	import { Separator } from "../ui/separator";
</script>

<Sheet.Root>
    <Sheet.Trigger>
        <Button variant="outline" class="w-full"><DotsThreeOutline weight="bold" /> About Open Scouting</Button>
    </Sheet.Trigger>
    <Sheet.Content class="max-h-[80vh] overflow-y-scroll lg:mx-64 border-1 p-4 rounded-t-lg" side="bottom">
        <div class="flex flex-col gap-4 mt-6 overflow-y-scroll pr-2">
            <div class="flex flex-col gap-2 items-center text-center mx-8">
                <img src={icon_rounded} alt="Logo" class="w-24 h-24 aspect-square" />
                <p class="text-2xl font-mono font-bold">Open Scouting</p>
                <p>An open source application for easier scouting at FIRST robotics competitions</p>
                <p>Version <span class="font-mono">{VERSION}</span></p>
            </div>

            <Separator orientation="horizontal" />

            <div class="flex flex-col gap-1">
                <p class="text-lg font-bold">Credits</p>
                <p class="text-md opacity-70">Made by <a href="https://github.com/FRC-Team3484" class="underline">FRC 3484 Short Circuit</a></p>
                <p class="text-md opacity-70">Started by <a href="https://github.com/nfoert" class="underline">nfoert</a></p>
                <p class="text-md opacity-70">Powered by <a href="https://www.thebluealliance.com/" class="underline">The Blue Alliance</a></p>
            </div>

            <Sheet.Footer>
                <Sheet.Close>
                    <Button variant="outline" class="w-full"><XCircle weight="bold" /> Close</Button>
                </Sheet.Close>
            </Sheet.Footer>
        </div>
    </Sheet.Content>
</Sheet.Root>