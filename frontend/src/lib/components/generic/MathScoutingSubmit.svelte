<script lang="ts">
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Dialog from "$lib/components/ui/dialog/index.js";
	import { CheckCircleIcon, TrashIcon, XCircleIcon } from "phosphor-svelte";
    import Button from "../ui/button/button.svelte";
	import { toast } from "svelte-sonner";

    function resetForm() {
        const form: HTMLFormElement | null = document.querySelector("#match-scouting-form");
        if (form) {
            form.reset();
            
            toast.success("Cleared scouting progress", { duration: 5000 });
            scrollTo({ top: 0, behavior: "smooth" });
        } else {
            toast.error("Failed to clear scouting progress", { duration: 5000, description: "Unable to select form element" });
        }
    }
</script>

<Card.Root class="w-auto min-w-64 my-4">
    <div class="flex flex-row gap-2 items-center justify-center">
        <Button class="px-8!" type="submit"><CheckCircleIcon weight="bold" /> Submit</Button>
        <Dialog.Root>
            <Dialog.Trigger>
                <Button variant="outline" size="icon"><TrashIcon weight="bold" /></Button>
            </Dialog.Trigger>

            <Dialog.Content>
                <Dialog.Title>
                    Clear scouting progress
                </Dialog.Title>
                <Dialog.Description>
                    Are you sure you want to clear all your scouting progress? This will fully reset the form.
                </Dialog.Description>

                <Dialog.Footer>
                    <Dialog.Close>
                        <Button type="reset" onclick={resetForm}><TrashIcon weight="bold" /> Clear</Button>
                        <Button variant="outline"><XCircleIcon weight="bold" /> Cancel</Button>
                    </Dialog.Close>
                </Dialog.Footer>
            </Dialog.Content>
        </Dialog.Root>
    </div>
</Card.Root>

