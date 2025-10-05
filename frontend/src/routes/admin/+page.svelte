<script lang="ts">
	import PageContainer from "$lib/components/layout/PageContainer.svelte";
	import { validateTokenOnline } from "$lib/utls/user";
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";

    let user = null;

    onMount(async () => {
        user = await validateTokenOnline();
        if (!user.is_superuser) {
            toast.error("403: Forbidden", { duration: 5000 });
            window.location.href = "/";
        }
    })
</script>

<PageContainer>
    <p>Admin</p>
</PageContainer>