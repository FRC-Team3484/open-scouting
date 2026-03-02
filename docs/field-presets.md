# Field Presets
Match scouting field presets can be created and later used to quickly import match scouting fields on another server.

Create a match scouting preset by defining your match scouting fields on your local development server, and then press `Export Fields as JSON`. Place this downloaded file in `/backend/app/match_scouting_presets` and give it a meaningful name. This file will appear as an option to import from in your local server, and upon pushing code to production, it will be avalable there as well.

You can alternatively use the `Upload a JSON file` option to import fields on a new server without using a preset.