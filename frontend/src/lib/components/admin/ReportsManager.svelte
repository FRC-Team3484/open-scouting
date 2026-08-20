<!-- 
@component
Management page for reports on the admin page
-->
<script lang="ts">
	import { onMount } from "svelte";
	import { toast } from "svelte-sonner";
	import { TrashIcon, XCircleIcon } from "phosphor-svelte";

    import * as Card from "$lib/components/ui/card/index.js";
	import Badge from "../ui/badge/badge.svelte";
	import Separator from "../ui/separator/separator.svelte";
	import Button from "../ui/button/button.svelte";
    import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";

	import type { EventReportDetails, MatchScoutingAnswerReportDetails, MatchScoutingSubmissionReportDetails, PitScoutingAnswerReportDetails, ReportResponse, TeamPitReportDetails } from "$lib/api/model";
	import { deleteReportContentReportContentDeleteReportUuidDelete, deleteReportReportDeleteReportUuidDelete, getReportsReportsGetGet } from "$lib/api/reports/reports";


    let reports: ReportResponse[] = [];

    /**
     * Get all reports from the server
     */
    async function getReports() {
        await getReportsReportsGetGet().then((response) => {
            if (response.status === 200) {
                reports = response.data;
            } else {
                toast.error("Failed to get reports", { duration: 5000 });
            }
        })
    }

    /**
     * Delete a report from the server, without deleting the associated content
     * 
     * @param reportUuid The UUID of the report
     */
    async function deleteReport(reportUuid: string) {
        await deleteReportReportDeleteReportUuidDelete(reportUuid).then((response) => {
            if (response.status === 200) {
                toast.success("Report deleted", { duration: 5000 });
                getReports();
            }
        })
    }

    /**
     * Delete a report from the server, along with the associated content
     * 
     * @param reportUuid The UUID of the report
     */
    async function deleteReportAndContent(reportUuid: string) {
        await deleteReportContentReportContentDeleteReportUuidDelete(reportUuid).then((response) => {
            if (response.status === 200) {
                toast.success("Report and content deleted", { duration: 5000 });
                getReports();
            }
        })
    }

    onMount(() => {
        getReports();
    })
</script>

<div class="flex flex-col gap-2">
    <Card.Root class="w-auto">
        <Card.Header>
            <Card.Title>Content Reports</Card.Title>
            <Card.Description>Manage and take action on content reports</Card.Description>
        </Card.Header>

        <Card.Content>
            <p>Found {reports.length} reports</p>
        </Card.Content>
    </Card.Root>

    <Card.Root>
        <Card.Content>
            <div class="flex flex-col gap-2">
                {#each reports as report}
                    <Card.Root>
                        <Card.Content>
                            <div class="flex flex-col gap-2 items-start text-left">
                                <p class="text-lg font-bold">{report.type.charAt(0).toUpperCase() + report.type.replaceAll("_", " ").slice(1)}</p>
                                <p class="text-muted-foreground text-sm">(<span class="font-mono">{report.content_uuid}</span>)</p>

                                <p><Badge>{report.report_reason}</Badge> {report.report_details}</p>

                                <p>Reported: {report.created_at}</p>

                                <Separator orientation="horizontal" class="my-2" />

                                {#if report.type == "match_scouting_submission"}
                                    {@const details = report.content_details as MatchScoutingSubmissionReportDetails}

                                    <p>Event: <span class="font-mono">{details.event_uuid}</span></p>
                                    <p>Season: <span class="font-mono">{details.season_uuid}</span></p>
                                    <p>Team Number: {details.team_number}</p>
                                    <p>Match Number: {details.match_number}</p>
                                    <p>Match Type: {details.match_type}</p>
                                    <p>{details.answers_count} answers:</p>
                                    {#if details.answers.length > 0}
                                        {#each details.answers as answer}
                                            <Card.Root>
                                                <Card.Content>
                                                    <div class="flex flex-col text-sm items-start w-full">
                                                        <p>Field: <span class="font-mono">{answer.field_uuid}</span></p>
                                                        <p>Value: {answer.value}</p>
                                                        <p>Created: {answer.created_at}</p>
                                                    </div>
                                                </Card.Content>
                                            </Card.Root>
                                        {/each}
                                    {/if}
                                {:else if report.type == "match_scouting_answer"}
                                    {@const details = report.content_details as MatchScoutingAnswerReportDetails}
                                    
                                    <p>Field: <span class="font-mono">{details.field_uuid}</span></p>
                                    <p>Value: {details.value}</p>
                                    <p>Created: {details.created_at}</p>

                                {:else if report.type == "team_pit"}
                                    {@const details = report.content_details as TeamPitReportDetails}

                                    <p>Team Number: {details.team_number}</p>
                                    <p>Nickname: {details.nickname}</p>
                                    <p>Season: <span class="font-mono">{details.season_uuid}</span></p>
                                    <p>Event: <span class="font-mono">{details.event_uuid}</span></p>

                                {:else if report.type == "pit_scouting_answer"}
                                    {@const details = report.content_details as PitScoutingAnswerReportDetails}

                                    <p>Field: <span class="font-mono">{details.field_uuid}</span></p>
                                    <p>Value: {details.value}</p>
                                    <p>Team Pit: <span class="font-mono">{details.team_uuid}</span></p>
                                    <p>Team Number: {details.team_number}</p>
                                    <p>Created: {details.created_at}</p>

                                {:else if report.type == "event"}
                                    {@const details = report.content_details as EventReportDetails}

                                    <p>Season: <span class="font-mono">{details.season_uuid}</span></p>
                                    <p>Event Code: <span class="font-mono">{details.event_code}</span></p>
                                    <p>Name: {details.name}</p>
                                    <p>Type: {details.type}</p>
                                    <p>City: {details.city}</p>
                                    <p>Country: {details.country}</p>
                                    <p>Start Date: {details.start_date}</p>
                                    <p>End Date: {details.end_date}</p>
                                    <p>Custom: {details.custom}</p>
                                    <p>Created: {details.created_at}</p>
                                {/if}

                                <Separator orientation="horizontal" class="my-2" />

                                <div class="flex flex-row gap-2 justify-end w-full flex-wrap">

                                    <AlertDialog.Root>
                                        <AlertDialog.Trigger>
                                            <Button variant="outline"><XCircleIcon weight="bold" /> Delete Report</Button>
                                        </AlertDialog.Trigger>

                                        <AlertDialog.Content>
                                            <AlertDialog.Title>Delete Report</AlertDialog.Title>
                                            <AlertDialog.Description>
                                                Are you sure you want to delete this report? This action cannot be undone, and the content relating to this report will remain on the server.
                                            </AlertDialog.Description>
                                            <AlertDialog.Footer>
                                                <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                                <AlertDialog.Action type="button" onclick={() => {deleteReport(report.uuid)}}>Delete</AlertDialog.Action>
                                            </AlertDialog.Footer>
                                        </AlertDialog.Content>
                                    </AlertDialog.Root>

                                    <AlertDialog.Root>
                                        <AlertDialog.Trigger>
                                            <Button><TrashIcon weight="bold" /> Delete Both Content and Report</Button>
                                        </AlertDialog.Trigger>

                                        <AlertDialog.Content>
                                            <AlertDialog.Title>Delete Report and Content</AlertDialog.Title>
                                            <AlertDialog.Description>
                                                Are you sure you want to delete this report and the content it relates to? This action cannot be undone.
                                            </AlertDialog.Description>
                                            <AlertDialog.Footer>
                                                <AlertDialog.Cancel type="button">Cancel</AlertDialog.Cancel>
                                                <AlertDialog.Action type="button" onclick={() => {deleteReportAndContent(report.uuid)}}>Delete</AlertDialog.Action>
                                            </AlertDialog.Footer>
                                        </AlertDialog.Content>
                                    </AlertDialog.Root>
                                </div>
                            </div>
                        </Card.Content>
                    </Card.Root>
                {/each}
            </div>
        </Card.Content>
    </Card.Root>
</div>