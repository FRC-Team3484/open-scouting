<script>
	import ThemeSwitcher from "$lib/components/generic/ThemeSwitcher.svelte";
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";

    onMount(() => {
        toast("Example toast", { description: "This is a description" })
        toast("Hello 2")
        toast("Hello 3")
    })
</script>

<ThemeSwitcher></ThemeSwitcher>
