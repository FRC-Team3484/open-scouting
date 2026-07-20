<!-- 
@component
Dialog used to report user submitted content for superuser review

Reportable content are match scouting submissions, match scouting answers, team pits, pit scouting answers, or events

Props:
    - `type` (`"match_scouting_submission" | "match_scouting_answer" | "team_pit" | "pit_scouting_answer" | "event"`) - The type of content to report
    - `open` (`boolean`) - Whether the dialog is open
    - `contentName` (`string`) - The name of the content to report
    - `contentUuid` (`string`) - The uuid of the content to report
    - `status` (`CreateReportStatus`) - The status of the report
        Other components can bind to this status to know when this component can be hidden again
-->
<script lang="ts" module>
    export type CreateReportStatus = "idle" | "success" | "cancel";
</script>

<script lang="ts">
	import { toast } from "svelte-sonner";

	import BaseDialog from "../dialogs/BaseDialog.svelte";
    import * as Select from "$lib/components/ui/select/index.js";
	import Textarea from "$lib/components/ui/textarea/textarea.svelte";
	import { Button } from "$lib/components/ui/button";
    
	import { createReportReportCreatePost } from "$lib/api/reports/reports";
	import type { CreateReportRequest, CreateReportRequestReportReason } from "$lib/api/model";
	import Separator from "$lib/components/ui/separator/separator.svelte";


    interface Props {
        type: "match_scouting_submission" | "match_scouting_answer" | "team_pit" | "pit_scouting_answer" | "event";
        open: boolean;
        contentName: string;
        contentUuid: string;
        status?: CreateReportStatus;
    }
    let { type, open = $bindable(false), contentName, contentUuid, status = $bindable() }: Props = $props();

    let reportReasonOptions = {
        "na": "Select Reason",
        "spam": "Spam",
        "innaccurate": "Innaccurate",
        "inappropriate": "Inappropriate",
        "offensive": "Offensive",
        "duplicate": "Duplicate",
        "other": "Other"
    }
    let reportReasonValue: CreateReportRequestReportReason | "na" = $state("na");
    let reportReasonLabel: string = $derived(reportReasonOptions[reportReasonValue]);

    let reportDetails: string = $state("");

    let submitting: boolean = $state(false);

    /**
     * Submit the report on the server for superuser review
     */
    async function submitReport() {
        submitting = true;

        if (reportReasonValue === "na") {
            toast.error("Please select a report reason", { duration: 5000 });
            submitting = false;
            return;
        }

        const createReportData: CreateReportRequest = {
            type: type,
            content_uuid: contentUuid,
            report_reason: reportReasonValue,
            report_details: reportDetails
        }

        await createReportReportCreatePost(createReportData).then((response) => {
            if (response.status === 200) {
                status = "success";
                open = false;
                toast.success("Report submitted", { duration: 5000 });
            }
        });

        submitting = false;
    }
</script>

<BaseDialog title="Report Content" description="Report content for superuser review" bind:open>
    <div class="flex flex-col gap-2">
        <p>Reporting an <span class="font-bold">{type.replace("_", " ").charAt(0).toUpperCase() + type.replace("_", " ").slice(1)}:</span></p>
        <p class="font-bold">{contentName}</p>

        <Separator class="my-2" />

        <p>Report Reason</p>
        <Select.Root type="single" required bind:value={reportReasonValue}>
            <Select.Trigger>
                {reportReasonLabel}
            </Select.Trigger>

            <Select.Content>
                <Select.Label>Report Reason</Select.Label>
                {#each Object.entries(reportReasonOptions) as [value, label]}
                    <Select.Item value={value} label={label} />
                {/each}
            </Select.Content>
        </Select.Root>
        <p class="text-xs text-muted-foreground mb-2">The reason for reporting this content</p>

        <p>Report Details</p>
        <Textarea placeholder="Report Details" bind:value={reportDetails} />
        <p class="text-xs text-muted-foreground mb-2">Additional details about the reason for reporting</p>

        <p class="my-2">Superusers will review your report and remove the content if necessary.</p>

        <div class="flex flex-row gap-2 w-full mt-4 justify-end">
            <Button variant="outline" onclick={() => open = false} disabled={submitting}>Cancel</Button>
            <Button onclick={() => {submitReport();}} disabled={submitting || reportReasonValue === "na"}>Submit Report</Button>
        </div>
    </div>
</BaseDialog>