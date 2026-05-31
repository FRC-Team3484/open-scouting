<!-- 
@component
The pit scouting question for image uploads

Props:
    - `pit` (`PitScoutingData`) - The parent pit for this question
    - `question` (`SeasonPitScoutingQuestion`) - The question
    - `answers` (`PitScoutingAnswer[]`) - Any answers for this question
    - `user` (`unknown`) - The user from the parent
-->
<script lang="ts">
    import { slide } from "svelte/transition";
	import { toast } from "svelte-sonner";
    import { ArrowBendDownRightIcon, CalendarIcon, EyeIcon, InfoIcon, PlusCircleIcon, UploadSimpleIcon, UserIcon, XIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
    import Badge from "$lib/components/ui/badge/badge.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Alert from "$lib/components/ui/alert/index.js";

    import { pushFiles } from "$lib/utils/sync";
	import { db, type PitScoutingAnswer, type PitScoutingData, type SeasonPitScoutingQuestion } from "$lib/utils/db";


    interface Props {
        pit: PitScoutingData
        question: SeasonPitScoutingQuestion
        answers: PitScoutingAnswer[]
        user: unknown
    }
    let { pit, question, answers, user }: Props = $props();
    
    type Mode = "none" | "view" | "add";
    let mode: Mode = $state("none");

    let files: FileList | null = $state(null);

    /**
     * Reset this question
     */
    function reset() {
        mode = "none";
        files = null;
    }

    /**
     * Place the image in the Files database store
     */
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
        await pushFiles().catch((error) => {
            console.warn("Failed to upload files to the server", error);
            toast.error("Failed to upload files to the server");
        });
    }

    /**
     * Add an answer to this question
     * 
     * @param imageUrls The image urls to upload as a pit scouting answer
     */
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
                <Button size="sm" onclick={() => mode = "add"}><PlusCircleIcon weight="bold" /> Add Answer</Button>
                <Button size="sm" variant="outline" onclick={() => mode = "view"}><EyeIcon weight="bold" /> View Answers</Button>
            </div>
        {:else if mode == "add" || mode == "view"}
            <div class="flex flex-row gap-2 flex-wrap">
                <Button size="sm" variant="outline" onclick={() => mode = "none"}><XIcon weight="bold" /> Close</Button>
            </div>
        {/if}
    </div>

    {#if mode == "add"}
        <Card.Content>
            <div class="flex flex-col gap-2 items-start w-full" transition:slide>
                <Input id="picture" type="file" bind:files={files} accept="image/*" multiple />
                <Button size="sm" onclick={uploadImage} disabled={files == null}>
                    <UploadSimpleIcon weight="bold" /> Upload
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
                            <InfoIcon weight="bold" />
                            <Alert.Title class="line-clamp-none">Images may not be immediately visible</Alert.Title>
                            <Alert.Description>Images are stored locally until they can be uploaded to the server. If an image is not visible yet, wait until you have connection before trying again.</Alert.Description>
                        </Alert.Root>

                        {#each answers as answer}
                            <div class="flex flex-col flex-wrap text-left">
                                <img src={answer.value} class="w-128 rounded-md bg-accent p-1" onerror={() => console.log("failed to load image ", answer.value)}>
                                <div class="flex flex-row flex-wrap items-center">
                                    <ArrowBendDownRightIcon weight="bold" class="text-muted-foreground ml-4 mr-1"/>
                                    <UserIcon weight="bold" class="text-muted-foreground ml-2 mr-1"/>
                                    <p class="text-muted-foreground text-sm">{answer.username}</p>
                                    <CalendarIcon weight="bold" class="text-muted-foreground ml-2 mr-1"/>
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