<!-- 
@component
The pit scouting question for image uploads

Props:
    - `pit` (`PitScoutingData`) - The parent pit for this question
    - `question` (`SeasonPitScoutingQuestion`) - The question
    - `answers` (`PitScoutingAnswer[]`) - Any answers for this question
    - `user` (`unknown`) - The user from the parent

TODO: This could be refactored
TODO: Make a full screen camera dialog instead of just a preview in a dialog?
-->
<script lang="ts">
	import { onDestroy, onMount } from "svelte";
    import { slide } from "svelte/transition";
	import { toast } from "svelte-sonner";
    import { ArrowBendDownRightIcon, ArrowLeftIcon, CalendarIcon, CameraIcon, EyeIcon, FileIcon, InfoIcon, PlusCircleIcon, TrashIcon, UploadSimpleIcon, UserIcon, XIcon } from "phosphor-svelte";

	import Button from "$lib/components/ui/button/button.svelte";
	import Input from "$lib/components/ui/input/input.svelte";
    import Badge from "$lib/components/ui/badge/badge.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
    import * as Alert from "$lib/components/ui/alert/index.js";
    import * as Select from "$lib/components/ui/select/index.js";

    import { pushFiles } from "$lib/utils/sync";
	import { db, type PitScoutingAnswer, type PitScoutingData, type SeasonPitScoutingQuestion } from "$lib/utils/db";
	import BaseDialog from "../../dialogs/BaseDialog.svelte";


    interface Props {
        pit: PitScoutingData
        question: SeasonPitScoutingQuestion
        answers: PitScoutingAnswer[]
        user: unknown
    }
    let { pit, question, answers, user }: Props = $props();
    
    type Mode = "none" | "view" | "add";
    let mode: Mode = $state("none");

    type AddMode = "choose" | "device" | "camera";
    let addMode: AddMode = $state("choose");

    let files: FileList | null = $state(null);

    let stream: MediaStream | null = null;
    let video: HTMLVideoElement;
    let capturedFiles: File[] = $state([]);
    let currentSession = 0;

    let cameras: MediaDeviceInfo[] = $state([]);
    let selectedCameraId: string | null = $state(null);
    let cameraSelectLabel: string = $derived(
        cameras.find(c => c.deviceId === selectedCameraId)?.label ?? "Select Camera",
    )

    let uploadImageDialogOpen: boolean = $state(false);
    let picturePreviewOpen: boolean = $state(false);
    let picturePreviewData: File | null = $state(null);

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
    async function uploadImages(files: File[]) {
        if (!files || files.length === 0) return;

        let imageUrls: string[] = [];

        for (const file of files) {
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

    /**
     * Start the camera
     */
    async function startCamera() {
        await stopCamera();

        const session = ++currentSession;

        const newStream = await navigator.mediaDevices.getUserMedia({
            video: {
                deviceId: selectedCameraId
            },
            audio: false
        });

        if (session !== currentSession) {
            newStream.getTracks().forEach(t => t.stop());
            return;
        }

        stream = newStream;
        video.srcObject = stream;
    }

    /**
     * Stop the camera
     */
    function stopCamera() {
        if (video) {
            video.pause();
            video.srcObject = null;
        }

        stream?.getTracks().forEach(track => track.stop());

        stream = null;
    }

    /**
     * Restart the camera
     */
    async function restartCamera() {
        await stopCamera();
        await startCamera();
    }

    /**
     * Take a picture using the camera
     */
    async function takePicture() {
        const canvas = document.createElement("canvas");

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext("2d")!;
        ctx.drawImage(video, 0, 0);

        const blob = await new Promise<Blob>((resolve) =>
            canvas.toBlob((blob) => resolve(blob!), "image/png")
        );

        const file = new File(
            [blob],
            `photo-${Date.now()}.png`,
            { type: "image/png" }
        );

        capturedFiles.push(file);
    }

    /**
     * Get the available cameras
     */
    async function getCameras() {
        const devices = await navigator.mediaDevices.enumerateDevices();

        const cameras = devices.filter(
            d => d.kind === "videoinput"
        );

        return cameras;
    }

    /**
     * Depending on the camera dialog open state, change the mode
     */
    function imageUploadDialogOpenChange() {
        if (uploadImageDialogOpen) {
            mode = "add";
        } else {
            mode = "none";
            stopCamera();
        }
    }

    /**
     * When the mode changes, open or close the camera dialog
     */
    $effect(() => {
        if (mode == "add") {
            uploadImageDialogOpen = true;
        } else {
            uploadImageDialogOpen = false;
            stopCamera();
        }
    });

    /**
     * When the add mode changes, start or stop the camera
     */
    $effect(() => {
        if (addMode == "camera" && uploadImageDialogOpen) {
            startCamera();
        } else {
            stopCamera();
        }
    });

    /**
     * When the selected camera changes, restart the camera
     */
    $effect(() => {
        selectedCameraId;

        if (uploadImageDialogOpen && addMode == "camera") {
            restartCamera();
        }
    })

    /**
     * On mount, get the available cameras
     */
    onMount(async () => {
        cameras = await getCameras().then((cameras) => {
            selectedCameraId = cameras[0]?.deviceId ?? null;
            return cameras;
        });

        navigator.mediaDevices.addEventListener(
            "devicechange",
            getCameras
        );
    })

    /**
     * On destroy, stop the camera
     */
    onDestroy(() => {
        stopCamera();
    })
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

<BaseDialog title="Image Upload" description="Take a picture, or upload one from your device" bind:open={uploadImageDialogOpen} onOpenChange={imageUploadDialogOpenChange}>
    <div class="flex flex-col gap-2">
        {#if addMode == "choose"}
            <p class="font-bold">Choose how to add an image</p>
            <Button onclick={() => addMode = "camera"}>Take Picture</Button>
            <Button onclick={() => addMode = "device"}>Upload from Device</Button>

        {:else if addMode == "camera"}
            <Button onclick={() => addMode = "choose"} size="sm" variant="outline" class="w-fit"><ArrowLeftIcon weight="bold" /> Back</Button>
            <p class="font-bold mb-2">Take Picture</p>

            <video
                bind:this={video}
                autoplay
                playsinline
                muted
                class="rounded-md w-full"
            />

            {#if cameras.length > 0}
                <Select.Root type="single" bind:value={selectedCameraId}>
                    <Select.Trigger class="w-full">
                        {cameraSelectLabel}
                    </Select.Trigger>

                    <Select.Content>
                        <Select.Label>Cameras</Select.Label>
                        {#each cameras as camera}
                            <Select.Item value={camera.deviceId}>
                                {camera.label}
                            </Select.Item>
                        {/each}
                    </Select.Content>
                </Select.Root>
            {/if}

            <Button size="sm" onclick={takePicture}><CameraIcon weight="bold" /> Take Picture</Button>

            {#if capturedFiles.length > 0}
                <div class="flex flex-row justify-between gap-2 items-center" transition:slide>
                    <div class="flex flex-col gap-2">
                        <p class="mt-2">{capturedFiles.length} picture{capturedFiles.length > 1 ? "s" : ""} taken</p>
                        <p class="text-sm text-muted-foreground">Tap or click image to expand</p>
                    </div>
                    <Button size="sm" variant="outline" onclick={() => capturedFiles = []}><TrashIcon weight="bold" /> Delete All</Button>
                </div>

                <div class="flex flex-row gap-2 overflow-x-scroll">
                    {#each capturedFiles as file}
                        <div class="flex flex-col gap-2 min-w-32">
                            <img src={URL.createObjectURL(file)} class="w-32 rounded-md bg-accent p-1" onclick={() => {picturePreviewOpen = true; picturePreviewData = file}}>
                            <Button size="sm" onclick={() => {capturedFiles = capturedFiles.filter(f => f != file)}} variant="destructive"><TrashIcon weight="bold" /> Delete</Button>
                        </div>
                    {/each}
                </div>
    
                <Button onclick={() => {uploadImages(capturedFiles)}}><UploadSimpleIcon weight="bold" /> Upload {capturedFiles.length} Image{capturedFiles.length > 1 ? "s" : ""}</Button>
            {/if}


        {:else if addMode == "device"}
            <Button onclick={() => addMode = "choose"} size="sm" variant="outline" class="w-fit"><ArrowLeftIcon weight="bold" /> Back</Button>
            <p class="font-bold mb-2">Upload from Device</p>

            <Input id="picture" type="file" bind:files={files} accept="image/*" multiple />
            <Button size="sm" onclick={() => {uploadImages(Array.from(files))}} disabled={files == null}>
                <UploadSimpleIcon weight="bold" /> Upload
            </Button>
        {/if}
    </div>
</BaseDialog>

<BaseDialog title="" description="" bind:open={picturePreviewOpen}>
    <img src={URL.createObjectURL(picturePreviewData)} class="w-128 rounded-md bg-accent p-1">
</BaseDialog>