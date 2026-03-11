<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
	import { db } from "$lib/utils/db";
    import Badge from "$lib/components/ui/badge/badge.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import { ArrowBendDownRight, ArrowBendLeftUp, Calendar, CircleNotch, Eye, PlusCircle, UploadSimple, User, X } from "phosphor-svelte";
    import { slide } from "svelte/transition";
	import { uploadImagesUploadImagesPost } from "$lib/api/uploads/uploads";
	import type { BodyUploadImagesUploadImagesPost, BodyUploadImageUploadImagePost } from "$lib/api/model";
	import { toast } from "svelte-sonner";
	import { env } from "$env/dynamic/public";

    let { pit, question, answers, user } = $props();

    type Mode = "none" | "view" | "add";
    let mode: Mode = $state("none");

    let value = $state("");
    let files: FileList | null = $state(null);
    let uploading: boolean = $state(false);

    function reset() {
        mode = "none";
        value = "";
        files = null;
    }

    async function uploadImage() {
        if (!files || files.length === 0) return;

        const uploadFile = Array.from(files);

        const body: BodyUploadImagesUploadImagesPost = {
            files: uploadFile
        }

        uploading = true;
        await uploadImagesUploadImagesPost(body).then(async (response) => {
            if (response.status !== 200) {
                toast.error("Failed to upload image", { duration: 5000, description: response.data.detail });
            } else {
                toast.success(`Uploaded ${response.data.count} images`, { duration: 5000 });

                await addAnswers(response.data.files.map((f) => f.url));
            }
        });
        uploading = false;
    }

    async function addAnswers(imageUrls: string[]) {
        const newAnswers = imageUrls.map(imageUrl => ({
            uuid: crypto.randomUUID(),
            value: imageUrl,
            username: user?.username ?? "guest",
            field_uuid: question.uuid,
            created_at: new Date().toISOString()
        }));

        await db.pit_scouting.update(pit.uuid, {
            answers: [...pit.answers, ...newAnswers],
            synced: false
        });

        value = "";
        reset();
    }
</script>

<Card.Root class="w-full items-start px-4">
    <div class="flex flex-col gap-2 justify-between flex-wrap">
        <div class="flex flex-col md:flex-row gap-2 flex-wrap items-start">
            <p class="font-bold text-left">{question.name}</p>
            <Badge variant="outline">{answers.length} {answers.length == 1 ? "image" : "images"}</Badge>
        </div>

        {#if mode == "none"}
            <div class="flex flex-row gap-2 flex-wrap">
                <Button size="sm" onclick={() => mode = "add"}><PlusCircle weight="bold" /> Add Answer</Button>
                <Button size="sm" variant="outline" onclick={() => mode = "view"}><Eye weight="bold" /> View Answers</Button>
            </div>
        {:else if mode == "add" || mode == "view"}
            <div class="flex flex-row gap-2 flex-wrap">
                <Button size="sm" variant="outline" onclick={() => mode = "none"}><X weight="bold" /> Close</Button>
            </div>
        {/if}
    </div>

    {#if mode == "add"}
        <Card.Content>
            <div class="flex flex-col gap-2 items-start w-full" transition:slide>
                <Input id="picture" type="file" bind:files={files} accept="image/*" multiple />
                <Button size="sm" onclick={uploadImage} disabled={files == null || uploading}>
                    {#if uploading}
                        <CircleNotch class="animate-spin" size={22} />
                    {:else}
                        <UploadSimple weight="bold" /> Upload
                    {/if}
                </Button>
            </div>
        </Card.Content>

    {:else if mode == "view"}
        <Card.Content>
            <div class="flex flex-row gap-2 w-full" transition:slide>
                {#if answers.length == 0}
                    <p class="text-muted-foreground">No answers yet</p>
                {:else}
                    <div class="flex flex-col gap-2">
                        {#each answers as answer}
                            <div class="flex flex-col flex-wrap text-left">
                                <img src={answer.value} class="w-128 aspect-square rounded-md bg-accent p-1" onerror={() => console.log("failed to load image")}>
                                <div class="flex flex-row flex-wrap items-center">
                                    <ArrowBendDownRight weight="bold" class="text-muted-foreground ml-4 mr-1"/>
                                    <User weight="bold" class="text-muted-foreground ml-2 mr-1"/>
                                    <p class="text-muted-foreground text-sm">{answer.username}</p>
                                    <Calendar weight="bold" class="text-muted-foreground ml-2 mr-1"/>
                                    <p class="text-muted-foreground text-sm">{new Intl.DateTimeFormat('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }).format(new Date(answer.created_at))}</p>
                                </div>
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>
        </Card.Content>
    {/if}
</Card.Root>