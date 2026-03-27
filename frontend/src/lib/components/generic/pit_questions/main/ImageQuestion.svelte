<script lang="ts">
	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
	import { db } from "$lib/utils/db";
    import Badge from "$lib/components/ui/badge/badge.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Alert from "$lib/components/ui/alert/index.js";
    import { ArrowBendDownRight, Calendar, Eye, Info, PlusCircle, UploadSimple, User, X } from "phosphor-svelte";
    import { slide } from "svelte/transition";
    import { pushFiles } from "$lib/utils/sync";

    let { pit, question, answers, user } = $props();

    type Mode = "none" | "view" | "add";
    let mode: Mode = $state("none");

    let value = $state("");
    let files: FileList | null = $state(null);

    function reset() {
        mode = "none";
        value = "";
        files = null;
    }

    async function uploadImage() {
        if (!files || files.length === 0) return;

        const uploadFile = Array.from(files);
        let imageUrls: string[] = [];

        for (const file of uploadFile) {
            const uuid = crypto.randomUUID();
            imageUrls.push("/uploads/" + uuid + ".png");

            db.files.add({
                uuid: uuid,
                data: file,
                url: "/uploads/" + uuid + ".png",
                synced: false
            });
        }

        mode = "none";
        await addAnswers(imageUrls);
        await pushFiles();
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
                <Button size="sm" onclick={uploadImage} disabled={files == null}>
                    <UploadSimple weight="bold" /> Upload
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
                        <Alert.Root class="items-left text-left max-w-128">
                            <Info weight="bold" />
                            <Alert.Title class="line-clamp-none">Images may not be immediately visible</Alert.Title>
                            <Alert.Description>Images are stored locally until they can be uploaded to the server. If an image is not visible yet, wait until you have connection before trying again.</Alert.Description>
                        </Alert.Root>

                        {#each answers as answer}
                            <div class="flex flex-col flex-wrap text-left">
                                <img src={answer.value} class="w-128 rounded-md bg-accent p-1" onerror={() => console.log("failed to load image ", answer.value)}>
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