<script lang="ts">
	import Badge from "$lib/components/ui/badge/badge.svelte";
    import Button from "$lib/components/ui/button/button.svelte";
    import * as Card from "$lib/components/ui/card/index.js";
	import { Calendar, Eye, PlusCircle, User, X } from "phosphor-svelte";
	import { slide } from "svelte/transition";

    let { question, answers, reset = $bindable(), children } = $props();

    type Mode = "none" | "view" | "add";

    let mode: Mode = $state("none");

    reset = () => {
        mode = "none";
    }
</script>

<Card.Root class="w-full">
    <Card.Header>
        <div class="flex flex-col gap-2 justify-between flex-wrap">
            <div class="flex flex-row gap-2 flex-wrap">
                <p class="font-bold">{question.name}</p>
                <Badge variant="outline">{answers.length} {answers.length == 1 ? "answer" : "answers"}</Badge>
            </div>

            {#if mode == "none"}
                <div class="flex flex-row gap-2 flex-wrap">
                    <Button onclick={() => mode = "add"}><PlusCircle weight="bold" /> Add Answer</Button>
                    <Button onclick={() => mode = "view"}><Eye weight="bold" /> View Answers</Button>
                </div>
            {:else if mode == "add" || mode == "view"}
                <div class="flex flex-row gap-2 flex-wrap">
                    <Button onclick={() => mode = "none"}><X weight="bold" /> Close</Button>
                </div>
            {/if}
        </div>
    </Card.Header>

    {#if mode == "add"}
        <Card.Content>
            <div class="flex flex-col gap-2 items-start w-full" transition:slide>
                {@render children()}
            </div>
        </Card.Content>

    {:else if mode == "view"}
        <Card.Content>
            <div class="flex flex-row gap-2 items-start w-full" transition:slide>
                {#if answers.length == 0}
                    <p class="text-muted-foreground">No answers yet</p>
                {:else}
                    <div class="flex flex-col gap-2">
                        {#each answers as answer}
                            <div class="flex flex-row items-end flex-wrap">
                                <p class="font-bold">{answer.value}</p>
                                <User weight="bold" class="text-muted-foreground ml-2 mr-1"/>
                                <p class="text-muted-foreground text-sm">{answer.username}</p>
                                <Calendar weight="bold" class="text-muted-foreground ml-2 mr-1"/>
                                <p class="text-muted-foreground text-sm">{new Intl.DateTimeFormat('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }).format(new Date(answer.created_at))}</p>
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>
        </Card.Content>
    {/if}
</Card.Root>