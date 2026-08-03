<!-- 
@component
Alert dialog for more details on why emails are disabled
-->
<script lang="ts">
	import { QuestionIcon } from "phosphor-svelte";

    import * as AlertDialog from "$lib/components/ui/alert-dialog";
    import Button from "$lib/components/ui/button/button.svelte";
</script>

<AlertDialog.Root>
    <AlertDialog.Trigger>
        <Button variant="outline"><QuestionIcon weight="bold" /> Why am I seeing this?</Button>
    </AlertDialog.Trigger>
    <AlertDialog.Content>
        <AlertDialog.Title>Why am I seeing this?</AlertDialog.Title>

        <AlertDialog.Description>
            <p>Having a reliable way to send emails to users, and getting them to deliver without being marked as spam can be expensive.</p>
            <p>Free tier email sending services are often limited and deliver marked as spam.</p>
            <br>
            <p>This may be due to a effort to keep Open Scouting's hosting costs as low as possible.</p>
            <p>If you are seeing this in the offseason, we may also be reducing costs due to low usage.</p>
        </AlertDialog.Description>
        <AlertDialog.Footer>
            <AlertDialog.Cancel type="button">Close</AlertDialog.Cancel>
        </AlertDialog.Footer>
    </AlertDialog.Content>
</AlertDialog.Root>