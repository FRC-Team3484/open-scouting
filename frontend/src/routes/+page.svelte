<script>
	import Button from "$lib/components/ui/button/button.svelte";
	import { ModeWatcher, toggleMode } from "mode-watcher";

    import Sun from "phosphor-svelte/lib/Sun";
    import Moon from "phosphor-svelte/lib/Moon";

</script>

<ModeWatcher></ModeWatcher>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>


<Button>Button</Button>

<Button onclick={toggleMode} variant="outline" size="icon">
    <Sun
    class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 !transition-all dark:-rotate-90 dark:scale-0"
  />
  <Moon
    class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 !transition-all dark:rotate-0 dark:scale-100"
  />
  <span class="sr-only">Toggle theme</span>
</Button>