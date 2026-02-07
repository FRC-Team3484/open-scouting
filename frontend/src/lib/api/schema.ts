import { makeApi, Zodios, type ZodiosOptions } from "@zodios/core";
import { z } from "zod";




const SignupRequest = z.object({ username: z.string(), email: z.string().email(), password: z.string(), confirm_password: z.string(), team_number: z.number().int(), display_name: z.string() }).passthrough();
const TokenResponse = z.object({ access_token: z.string(), token_type: z.string().optional().default("bearer") }).passthrough();
const ValidationError = z.object({ loc: z.array(z.union([z.string(), z.number()])), msg: z.string(), type: z.string() }).passthrough();
const HTTPValidationError = z.object({ detail: z.array(ValidationError) }).partial().passthrough();
const Body_login_for_access_token_token_post = z.object({ grant_type: z.union([z.string(), z.null()]).optional(), username: z.string(), password: z.string(), scope: z.string().optional().default(""), client_id: z.union([z.string(), z.null()]).optional(), client_secret: z.union([z.string(), z.null()]).optional() }).passthrough();
const UserResponse = z.object({ uuid: z.string().uuid(), username: z.string(), email: z.string().email(), is_superuser: z.boolean(), created_at: z.string().datetime({ offset: true }) }).passthrough();
const MessageResponse = z.object({ message: z.string() }).passthrough();
const BaseSettings = z.object({ favorite_events: z.array(z.string()) }).passthrough();
const OrganizationRequest = z.object({ name: z.string(), description: z.string() }).passthrough();
const OrganizationResponse = z.object({ uuid: z.string().uuid(), name: z.string(), description: z.string(), created_at: z.string().datetime({ offset: true }) }).passthrough();
const OrganizationMemberResponse = z.object({ uuid: z.string().uuid(), organization: z.string().uuid(), user: z.string().uuid(), role: z.string(), created_at: z.string().datetime({ offset: true }) }).passthrough();
const SeasonResponse = z.object({ year: z.number().int(), name: z.string(), active: z.boolean(), uuid: z.string().uuid(), created_at: z.string().datetime({ offset: true }) }).passthrough();
const SeasonCreate = z.object({ year: z.number().int(), name: z.string(), active: z.boolean() }).passthrough();
const GamepieceResponse = z.object({ uuid: z.string().uuid(), season: z.string().uuid(), name: z.string(), created_at: z.string().datetime({ offset: true }) }).passthrough();
const GamepieceRequest = z.object({ season_uuid: z.string().uuid(), name: z.string() }).passthrough();
const MatchScoutingFieldRequest = z.object({ name: z.string(), season_uuid: z.string().uuid(), field_type: z.string(), stat_type: z.string(), required: z.boolean(), order: z.number().int(), organization_uuid: z.union([z.string(), z.null()]).optional(), parent_uuid: z.union([z.string(), z.null()]).optional(), options: z.union([z.array(z.unknown()), z.null()]).optional(), game_piece_uuid: z.union([z.string(), z.null()]).optional() }).passthrough();
const MatchScoutingFieldResponse = z.object({ uuid: z.union([z.string(), z.null()]).optional(), name: z.string(), field_type: z.string(), stat_type: z.string(), game_piece_id: z.union([z.string(), z.null()]).optional(), required: z.boolean(), options: z.union([z.array(z.unknown()), z.null()]).optional(), order: z.number().int(), organization_id: z.union([z.string(), z.null()]).optional() }).passthrough();
const MatchScoutingRequest = z.object({ submission_uuid: z.string().uuid(), fields: z.object({}).partial().passthrough(), user_uuid: z.union([z.string(), z.string()]), year: z.number().int(), team_number: z.number().int(), match_number: z.number().int(), match_type: z.string(), event_code: z.string(), event_name: z.string(), event_type: z.string(), event_city: z.string(), event_country: z.string(), event_start_date: z.string(), event_end_date: z.string() }).passthrough();
const MatchScoutingResponse = z.object({ uuid: z.string().uuid(), user: z.union([z.string(), z.null()]), event: z.string().uuid(), team_number: z.number().int(), match_number: z.number().int(), match_type: z.string(), created_at: z.string().datetime({ offset: true }) }).passthrough();
const PitFieldResponse = z.object({ uuid: z.string().uuid(), season: z.string().uuid(), name: z.string(), field_type: z.string(), options: z.array(z.unknown()), order: z.number().int(), organization: z.union([z.string(), z.null()]), created_at: z.string().datetime({ offset: true }) }).passthrough();
const CreatePitFieldRequest = z.object({ season_uuid: z.string().uuid(), name: z.string(), field_type: z.string(), options: z.string(), order: z.number().int(), organization_uuid: z.string().uuid() }).passthrough();
const EditPitFieldRequest = z.object({ season_uuid: z.string().uuid(), name: z.string(), field_type: z.string(), options: z.string(), order: z.number().int(), organization_uuid: z.string().uuid(), field_uuid: z.string().uuid() }).passthrough();
const GetPitsForSeasonRequest = z.object({ season_uuid: z.string().uuid(), event_code: z.string(), event_name: z.string(), event_type: z.string(), event_city: z.string(), event_country: z.string(), event_start_date: z.string(), event_end_date: z.string() }).passthrough();
const SubmitPitFieldAnswerRequest = z.object({ season_uuid: z.string().uuid(), team_number: z.number().int(), event_code: z.string(), event_name: z.string(), event_type: z.string(), event_city: z.string(), event_country: z.string(), event_start_date: z.string(), event_end_date: z.string(), answers: z.object({}).partial().passthrough(), nickname: z.string() }).passthrough();
const EventResponse = z.object({ uuid: z.string().uuid(), season: z.string().uuid(), event_code: z.string(), name: z.string(), type: z.string(), city: z.string(), country: z.string(), start_date: z.string().datetime({ offset: true }), end_date: z.string().datetime({ offset: true }), pits_generated: z.boolean(), custom: z.boolean(), created_at: z.string().datetime({ offset: true }) }).passthrough();
const CustomEventRequest = z.object({ season_uuid: z.string().uuid(), event_code: z.string(), event_name: z.string(), event_type: z.string(), event_city: z.string(), event_country: z.string(), event_start_date: z.string(), event_end_date: z.string() }).passthrough();

export const schemas = {
	SignupRequest,
	TokenResponse,
	ValidationError,
	HTTPValidationError,
	Body_login_for_access_token_token_post,
	UserResponse,
	MessageResponse,
	BaseSettings,
	OrganizationRequest,
	OrganizationResponse,
	OrganizationMemberResponse,
	SeasonResponse,
	SeasonCreate,
	GamepieceResponse,
	GamepieceRequest,
	MatchScoutingFieldRequest,
	MatchScoutingFieldResponse,
	MatchScoutingRequest,
	MatchScoutingResponse,
	PitFieldResponse,
	CreatePitFieldRequest,
	EditPitFieldRequest,
	GetPitsForSeasonRequest,
	SubmitPitFieldAnswerRequest,
	EventResponse,
	CustomEventRequest,
};

const endpoints = makeApi([
	{
		method: "post",
		path: "/auth/signup",
		alias: "signup_auth_signup_post",
		description: `Create a new user

If this is the first user on the server, make them a superuser

Paramaters:
    data (SignupRequest): The data to create the user

Returns:
    TokenResponse: The access token`,
		requestFormat: "json",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: SignupRequest
			},
		],
		response: TokenResponse,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/auth/validate",
		alias: "validate_user_auth_validate_get",
		description: `Validate the current user

Returns:
    User: The current user`,
		requestFormat: "json",
		response: UserResponse,
	},
	{
		method: "get",
		path: "/data/filters",
		alias: "get_data_filters_data_filters_get",
		description: `For a year, list of event codes, and list of team numbers, return a JSON object 
    containing the available filters that can additionally be applied

For example, if just a year is given, return all team numbers and events with data on the server.
If a year and event code is given, return all team numbers for that event and year with data on the server.
If a year and multiple event codes are given, return all team numbers which have data on the server for those event codes and year.
If a year and a team number is given, return all event codes which have data on the server for that team number and year.
If a year and multiple team numbers are given, return all event codes which have data on the server for those team numbers and year.`,
		requestFormat: "json",
		parameters: [
			{
				name: "year",
				type: "Query",
				schema: z.number().int()
			},
			{
				name: "event_codes",
				type: "Query",
				schema: z.string()
			},
			{
				name: "team_numbers",
				type: "Query",
				schema: z.string()
			},
		],
		response: z.unknown(),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/data/get",
		alias: "get_data_data_get_get",
		description: `Given a year, event codes, and team numbers, return the data that matches those filters

Data should be structured based on the stat_type and game_piece of the associated MatchScoutingField.
The data should be a list of JSON objects. Each object represents a team with data. In that object,
    there should be four lists: teleop, auton, capability, other
teleop and auton should be a list of JSON objects, for each game_piece for that season.
    Then, for each game piece, it should be a list of JSON objects that represents each individual field with type: auton_score, auton_miss, teleop_score, teleop_miss
    These fields should have the field type, name, uuid, list of all data points, and the minimum, the maximum, and the average (if applicable).

For example, there are two game pieces. Coral and Algae. There is a field for how much coral was scored and how much were dropped, both as a teleop_score.
    There will be a list of JSON objects for each team. In the team object, inside the teleop list, there should be two additional lists, one for coral and one for algae.
    Then there will two more JSON objects for both of those fields, with the field type, name, uuid, and list of all data points.

Next, for capabilities, find each field that is a capability and find the percentages of each value occurrence. This will most likely 
    be something that is a multiple_choice or choice MatchScoutingField, and we&#x27;ll want to show how often each value occurred using something like a pie chart.

Finally, for other, simply return the same field information and the value, as this will likely be a text input.

[
    {
        &quot;team_number&quot;: 1234,
        &quot;nickname&quot;: &quot;Team 1234&quot;,
        &quot;teleop&quot;: [
            &quot;coral&quot;: [
                {
                    &quot;field_uuid&quot;: &quot;uuid&quot;,
                    &quot;field_type&quot;: &quot;small_number&quot;,
                    &quot;field_name&quot;: &quot;Coral scored&quot;,
                    &quot;values&quot;: [1, 2, 3, ...],
                    &quot;min&quot;: 0,
                    &quot;max&quot;: 100,
                    &quot;avg&quot;: 50
                },
                {
                    &quot;field_uuid&quot;: &quot;uuid&quot;,
                    &quot;field_type&quot;: &quot;small_number&quot;,
                    &quot;field_name&quot;: &quot;Coral dropped&quot;,
                    &quot;values&quot;: [1, 2, 3, ...],
                    &quot;min&quot;: 0,
                    &quot;max&quot;: 100,
                    &quot;avg&quot;: 50
                }
            ],
            &quot;algae&quot;: [...],
        ],
        &quot;auton&quot;: [...],
        &quot;capability&quot;: [
            {
                &quot;field_uuid&quot;: &quot;uuid&quot;,
                &quot;field_type&quot;: &quot;choice&quot;,
                &quot;field_name&quot;: &quot;Climb level&quot;,
                &quot;values&quot;: [&quot;low&quot;, &quot;medium&quot;, &quot;high&quot;],
                &quot;percentages&quot;: [
                    {
                        &quot;value&quot;: &quot;low&quot;,
                        &quot;percentage&quot;: 50
                    }, {
                        &quot;value&quot;: &quot;medium&quot;,
                        &quot;percentage&quot;: 25
                    }, {
                        &quot;value&quot;: &quot;high&quot;,
                        &quot;percentage&quot;: 25
                    }
                ],
                ...
            }
        ],
        &quot;other&quot;: [
            {
                &quot;field_uuid&quot;: &quot;uuid&quot;,
                &quot;field_type&quot;: &quot;string&quot;,
                &quot;field_name&quot;: &quot;Notes&quot;,
                &quot;value&quot;: &quot;Some notes&quot;,
            },
            ...
        ]
    },
    ...
]`,
		requestFormat: "json",
		parameters: [
			{
				name: "year",
				type: "Query",
				schema: z.number().int()
			},
			{
				name: "event_codes",
				type: "Query",
				schema: z.string()
			},
			{
				name: "team_numbers",
				type: "Query",
				schema: z.string()
			},
		],
		response: z.unknown(),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/event/custom/:season_uuid",
		alias: "get_custom_events_event_custom__season_uuid__get",
		description: `Get all custom events for a season

Parameters:
    season_uuid (&#x60;UUID&#x60;): The UUID of the season to get custom events for

Returns:
    list[EventResponse]: A list of all custom events for the season`,
		requestFormat: "json",
		parameters: [
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string()
			},
		],
		response: z.array(EventResponse),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "post",
		path: "/event/custom/:season_uuid/create",
		alias: "create_custom_event_event_custom__season_uuid__create_post",
		description: `Create a custom event for a season

Parameters:
    season_uuid (&#x60;UUID&#x60;): The UUID of the season to create a custom event for
    data (&#x60;CustomEventRequest&#x60;): The UUID of the season to create a custom event for

Returns:
    EventResponse: The created custom event`,
		requestFormat: "json",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: CustomEventRequest
			},
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: EventResponse,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "delete",
		path: "/fields/delete/:field_uuid",
		alias: "delete_field_fields_delete__field_uuid__delete",
		description: `Delete a match scouting field

Requires superuser access

Parameters:
    field_uuid (&#x60;UUID&#x60;): The UUID of the field to delete

Returns:
    &#x60;MessageResponse&#x60;: A message indicating that the field was deleted`,
		requestFormat: "json",
		parameters: [
			{
				name: "field_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: z.object({ message: z.string() }).passthrough(),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/fields/get_presets",
		alias: "get_match_scouting_field_presets_fields_get_presets_get",
		description: `Get all JSON match scouting field presets

Requires superuser access

Returns:
    &#x60;list[Any]&#x60;: A list of all match scouting field presets`,
		requestFormat: "json",
		response: z.array(z.unknown()),
	},
	{
		method: "get",
		path: "/fields/season/:season_uuid",
		alias: "get_season_fields_fields_season__season_uuid__get",
		description: `Get all match scouting fields for a season

Parameters:
    season_uuid (&#x60;UUID&#x60;): The UUID of the season to get fields for

Returns:
    &#x60;list[MatchScoutingField]&#x60;: A list of all match scouting fields for the season`,
		requestFormat: "json",
		parameters: [
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: z.array(z.unknown()),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "delete",
		path: "/fields/season/:season_uuid/clear",
		alias: "clear_season_fields_fields_season__season_uuid__clear_delete",
		description: `Clear all match scouting fields for a season

Requires superuser access

Parameters:
    season_uuid (&#x60;UUID&#x60;): The UUID of the season to clear fields for

Returns:
    &#x60;MessageResponse&#x60;: A message indicating that the fields were cleared`,
		requestFormat: "json",
		parameters: [
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: z.object({ message: z.string() }).passthrough(),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "post",
		path: "/fields/season/:season_uuid/create",
		alias: "create_season_field_fields_season__season_uuid__create_post",
		description: `Create a new match scouting field

Requires superuser access

Parameters:
    season_uuid (&#x60;UUID&#x60;): The UUID of the season to create the field for
    data (MatchScoutingFieldRequest): The data to create the field

Returns:
    &#x60;MatchScoutingField&#x60;: The created field`,
		requestFormat: "json",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: MatchScoutingFieldRequest
			},
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: MatchScoutingFieldResponse,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "post",
		path: "/fields/season/:season_uuid/edit/:field_uuid",
		alias: "edit_season_field_fields_season__season_uuid__edit__field_uuid__post",
		description: `Edit a match scouting field

Requires superuser access

Parameters:
    season_uuid (&#x60;UUID&#x60;): The UUID of the season to edit the field for
    field_uuid (&#x60;UUID&#x60;): The UUID of the field to edit
    data (MatchScoutingFieldRequest): The data to edit the field

Returns:
    &#x60;MatchScoutingField&#x60;: The edited field`,
		requestFormat: "json",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: MatchScoutingFieldRequest
			},
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
			{
				name: "field_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: MatchScoutingFieldRequest,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/gamepieces",
		alias: "get_gamepieces_gamepieces_get",
		description: `Get all game pieces on the server

Returns:
    list[GamepieceResponse]: A list of all game pieces`,
		requestFormat: "json",
		response: z.array(GamepieceResponse),
	},
	{
		method: "post",
		path: "/gamepieces/create",
		alias: "create_gamepiece_gamepieces_create_post",
		description: `Create a new game piece

Requires superuser access

Parameters:
    data (GamepieceRequest): The data to create the game piece

Returns:
    &#x60;GamepieceResponse&#x60;: The created game piece`,
		requestFormat: "json",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: GamepieceRequest
			},
		],
		response: GamepieceResponse,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "delete",
		path: "/gamepieces/delete/:gamepiece_uuid",
		alias: "delete_gamepiece_gamepieces_delete__gamepiece_uuid__delete",
		description: `Delete a game piece

Requires superuser access

Parameters:
    gamepiece_uuid (&#x60;UUID&#x60;): The UUID of the game piece to delete

Returns:
    &#x60;MessageResponse&#x60;: A message indicating that the game piece was deleted`,
		requestFormat: "json",
		parameters: [
			{
				name: "gamepiece_uuid",
				type: "Path",
				schema: z.string()
			},
		],
		response: z.object({ message: z.string() }).passthrough(),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/gamepieces/season/:season_uuid",
		alias: "get_season_gamepieces_gamepieces_season__season_uuid__get",
		description: `Get all game pieces for a season

Parameters:
    season_uuid (&#x60;UUID&#x60;): The UUID of the season to get game pieces for

Returns:
    list[GamepieceResponse]: A list of all game pieces for the season`,
		requestFormat: "json",
		parameters: [
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: z.array(GamepieceResponse),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/organization/:organization_uuid",
		alias: "get_organization_organization__organization_uuid__get",
		description: `Get a specific organization

Parameters:
    data (OrganizationUuidRequest): The data to get the organization

Returns:
    &#x60;Organization&#x60;: The organization`,
		requestFormat: "json",
		parameters: [
			{
				name: "organization_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: OrganizationResponse,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/organization/:organization_uuid/members",
		alias: "get_organization_members_organization__organization_uuid__members_get",
		description: `Get all members of a specific organization

Parameters:
    data (OrganizationUuidRequest): The data to get the organization members

Returns:
    list[OrganizationMember]: A list of all organization members`,
		requestFormat: "json",
		parameters: [
			{
				name: "organization_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: z.array(OrganizationMemberResponse),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/organization/all/list",
		alias: "get_organizations_organization_all_list_get",
		description: `Get all organizations on the server

Returns:
    list[Organization]: A list of all organizations`,
		requestFormat: "json",
		response: z.array(OrganizationResponse),
	},
	{
		method: "post",
		path: "/organization/create",
		alias: "create_organization_organization_create_post",
		description: `Create a new organization

Parameters:
    data (OrganizationRequest): The data to create the organization

Returns:
    &#x60;Organization&#x60;: The created organization`,
		requestFormat: "json",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: OrganizationRequest
			},
		],
		response: OrganizationResponse,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "delete",
		path: "/organization/delete/:organization_uuid",
		alias: "delete_organization_organization_delete__organization_uuid__delete",
		description: `Delete a specific organization

Parameters:
    data (OrganizationUuidRequest): The data to delete the organization

Returns:
    &#x60;MessageResponse&#x60;: A message indicating that the organization was deleted`,
		requestFormat: "json",
		parameters: [
			{
				name: "organization_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: z.object({ message: z.string() }).passthrough(),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/organization/me/list",
		alias: "get_user_organizations_organization_me_list_get",
		description: `Get all organizations that the current user is a member of

Returns:
    list[Organization]: A list of all organizations`,
		requestFormat: "json",
		response: z.array(OrganizationResponse),
	},
	{
		method: "delete",
		path: "/pits/fields/:field_uuid/delete",
		alias: "delete_pit_field_pits_fields__field_uuid__delete_delete",
		description: `Delete a pit scouting field

Requires superuser access

Parameters:
    field_uuid (&#x60;UUID&#x60;): The UUID of the field to delete
    data (&#x60;DeletePitFieldRequest&#x60;): The UUID of the field to delete

Returns:
    &#x60;MessageResponse&#x60;: A message indicating that the field was deleted`,
		requestFormat: "json",
		parameters: [
			{
				name: "field_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: z.object({ message: z.string() }).passthrough(),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/pits/fields/:season_uuid",
		alias: "get_pit_fields_pits_fields__season_uuid__get",
		description: `Get all pit scouting fields for a season

Parameters:
    data (&#x60;PitFieldsRequest&#x60;): The UUID of the season to get fields for

Returns:
    list[PitFieldResponse]: A list of all pit scouting fields for the season`,
		requestFormat: "json",
		parameters: [
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: z.array(PitFieldResponse),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "delete",
		path: "/pits/fields/:season_uuid/clear",
		alias: "clear_pit_fields_pits_fields__season_uuid__clear_delete",
		description: `Clear all pit scouting fields for a season

Requires superuser access

Parameters:
    season_uuid (&#x60;UUID&#x60;): The UUID of the season to clear fields for
    data (&#x60;PitFieldsRequest&#x60;): The UUID of the season to clear fields for

Returns:
    &#x60;MessageResponse&#x60;: A message indicating that the fields were cleared`,
		requestFormat: "json",
		parameters: [
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: z.object({ message: z.string() }).passthrough(),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "post",
		path: "/pits/fields/:season_uuid/create",
		alias: "create_pit_field_pits_fields__season_uuid__create_post",
		description: `Create a new pit scouting field

Requires superuser access

Parameters:
    season_uuid (&#x60;UUID&#x60;): The UUID of the season to create the field for
    data (&#x60;CreatePitFieldRequest&#x60;): The data to create the field

Returns:
    &#x60;PitFieldResponse&#x60;: The created field`,
		requestFormat: "json",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: CreatePitFieldRequest
			},
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: PitFieldResponse,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "patch",
		path: "/pits/fields/:season_uuid/edit/:field_uuid",
		alias: "edit_pit_field_pits_fields__season_uuid__edit__field_uuid__patch",
		description: `Edit a pit scouting field

Requires superuser access

Parameters:
    season_uuid (&#x60;UUID&#x60;): The UUID of the season to edit the field for
    field_uuid (&#x60;UUID&#x60;): The UUID of the field to edit
    data (&#x60;EditPitFieldRequest&#x60;): The data to edit the field

Returns:
    &#x60;PitFieldResponse&#x60;: The edited field`,
		requestFormat: "json",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: EditPitFieldRequest
			},
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
			{
				name: "field_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: PitFieldResponse,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "post",
		path: "/pits/get/:season_uuid",
		alias: "get_pits_pits_get__season_uuid__post",
		description: `Get all pits for a season

Parameters:
    season_uuid (&#x60;UUID&#x60;): The UUID of the season to get pits for
    data (&#x60;GetPitsForSeasonRequest&#x60;): The UUID of the season to get pits for

Returns:
    list: A list of all pits for the season`,
		requestFormat: "json",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: GetPitsForSeasonRequest
			},
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
		],
		response: z.unknown(),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "post",
		path: "/pits/submit/:season_uuid/:team_number",
		alias: "submit_pit_pits_submit__season_uuid___team_number__post",
		description: `Get the season and event from the uuids. Then, check if a pit with that team number exists.
If it does, update that pit

For the answers in that pit, find each answer that does not already exist on the server, and add them

If a pit does not exist, that means it was created by the client of a user. It should be created.

Parameters:
    season_uuid (&#x60;UUID&#x60;): The UUID of the season to get pits for
    team_number (&#x60;int&#x60;): The team number to get pits for
    data (&#x60;SubmitPitFieldAnswerRequest&#x60;): The UUID of the season and event to get pits for

Returns:
    MessageResponse: A message indicating that the pits were submitted`,
		requestFormat: "json",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: SubmitPitFieldAnswerRequest
			},
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string().uuid()
			},
			{
				name: "team_number",
				type: "Path",
				schema: z.number().int()
			},
		],
		response: z.object({ message: z.string() }).passthrough(),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "post",
		path: "/scouting/submit",
		alias: "submit_match_scouting_scouting_submit_post",
		description: `Submit a match scouting form

Will create a MatchScoutingSubmission for each submission, and then create a MatchScoutingAnswer for each field answer

Parameters:
    data (MatchScoutingRequest): The data to submit the match scouting form

Returns:
    &#x60;MatchScoutingSubmission&#x60;: The submitted match scouting form`,
		requestFormat: "json",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: MatchScoutingRequest
			},
		],
		response: MatchScoutingResponse,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/seasons",
		alias: "get_seasons_seasons_get",
		description: `Get all seasons on the server

Returns:
    list[Season]: A list of all seasons`,
		requestFormat: "json",
		response: z.array(SeasonResponse),
	},
	{
		method: "get",
		path: "/seasons/active",
		alias: "get_active_season_seasons_active_get",
		description: `Get the active season on the server

Returns:
    Season: The active season`,
		requestFormat: "json",
		response: z.union([SeasonResponse, z.null()]),
	},
	{
		method: "post",
		path: "/seasons/create",
		alias: "create_season_seasons_create_post",
		description: `Create a new season

Requires superuser access

Parameters:
    data (&#x60;SeasonCreate&#x60;): The data to create the season

Returns:
    &#x60;SeasonResponse&#x60;: The created season`,
		requestFormat: "json",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: SeasonCreate
			},
		],
		response: SeasonResponse,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "delete",
		path: "/seasons/delete/:season_uuid",
		alias: "delete_season_seasons_delete__season_uuid__delete",
		description: `Delete a season

Requires superuser access

Parameters:
    season_uuid (&#x60;UUID&#x60;): The UUID of the season to delete

Returns:
    &#x60;MessageResponse&#x60;: A message indicating that the season was deleted`,
		requestFormat: "json",
		parameters: [
			{
				name: "season_uuid",
				type: "Path",
				schema: z.string()
			},
		],
		response: z.object({ message: z.string() }).passthrough(),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "post",
		path: "/token",
		alias: "login_for_access_token_token_post",
		description: `OAuth2 compatible token login, get an access token for future requests

Parameters:
    form_data (OAuth2PasswordRequestForm): The data to login with

Returns:
    dict[str, str]: The access token`,
		requestFormat: "form-url",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: Body_login_for_access_token_token_post
			},
		],
		response: TokenResponse,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/users/",
		alias: "get_users_users__get",
		description: `Get all users on the server

Requires superuser access

Returns:
    list[User]: A list of all users`,
		requestFormat: "json",
		response: z.array(UserResponse),
	},
	{
		method: "delete",
		path: "/users/delete/:username",
		alias: "delete_user_users_delete__username__delete",
		description: `Delete a user on the server

Requires superuser access

Parameters:
    username (str): The username of the user to delete

Returns:
    MessageResponse: A message indicating that the user was deleted`,
		requestFormat: "json",
		parameters: [
			{
				name: "username",
				type: "Path",
				schema: z.string()
			},
		],
		response: z.object({ message: z.string() }).passthrough(),
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "get",
		path: "/users/me/get_settings",
		alias: "get_user_settings_users_me_get_settings_get",
		description: `Get the settings for the current user

Returns:
    BaseSettings: The settings for the current user`,
		requestFormat: "json",
		response: BaseSettings,
	},
	{
		method: "post",
		path: "/users/me/update_settings",
		alias: "update_user_settings_users_me_update_settings_post",
		description: `Update the settings for the current user

Parameters:
    data (BaseSettings): The settings to update

Returns:
    BaseSettings: The settings for the current user`,
		requestFormat: "json",
		parameters: [
			{
				name: "body",
				type: "Body",
				schema: BaseSettings
			},
		],
		response: BaseSettings,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
	{
		method: "post",
		path: "/users/set_superuser/:username",
		alias: "set_superuser_users_set_superuser__username__post",
		description: `Set a user as a superuser

Requires superuser access

Parameters:
    username (str): The username of the user to set as a superuser

Returns:
    User: The user that was set as a superuser`,
		requestFormat: "json",
		parameters: [
			{
				name: "username",
				type: "Path",
				schema: z.string()
			},
		],
		response: UserResponse,
		errors: [
			{
				status: 422,
				description: `Validation Error`,
				schema: HTTPValidationError
			},
		]
	},
]);

export const api = new Zodios(endpoints);

export function createApiClient(baseUrl: string, options?: ZodiosOptions) {
    return new Zodios(baseUrl, endpoints, options);
}
