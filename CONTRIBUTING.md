# Contributing
Thank you for being interested in contributing to Open Scouting!

See the [milestones](https://github.com/FRC-Team3484/open-scouting/milestones) and [issues](https://github.com/FRC-Team3484/open-scouting/issues) page for the next things that need worked on.

## How to Contribute
1. Fork this repository. (Ensure you uncked the "Copy the `main` branch only" check box, to get access to any of the upcoming version branches)
2. Create a new branch, in the format `feat/<version>/#<issue number>-<issue description>`.
3. Use [Development Installation](/docs/development-installation.md) to setup the project locally to test changes.
4. Implement your changes.
5. Open a PR to the main repo, merging into the required version branch.
6. Your PR will be reviewed and eventually merged. 

Issues usually belong to a milestone. If a milestone is far off from being finished, it may take some time before your contribution gets released.

Thanks for your contribution!

## Frontend Contributions
When adding code to the frontend, there are a few rules and guidelines that should be followed:

- All Svelte components need a `@component` comment at the top of the file. This comment should explain the purpose of the component and any props it takes.
- Use TypeScript typing in variables, function paramaters and return types, and anywhere else as much as possible.
- All functions, `$effect`s and `onMount`s should have a comment explaining what it does. Exceptions can be made for `$effect`s or `onMount`s that have just one or two lines and are just updating state.
- Use `bold` [Phosphor Icons](https://phosphoricons.com/).
- Use [`shadcn-svelte`](https://shadcn-svelte.com/) components whereever possible.
- Design pages to be mobile and offline first. Pages should fall back to a good offline state or warning if no network is avaliable.
- When making network requests to the backend, use the generated typed orval functions.

See [Client Systems](/docs/client-systems.md) for more information on the avaliable custom systems and features in the frontend.

## Backend Contributions
Similarly, there are some things to keep in mind when adding code to the backend:

- Every route should have a comment explaining what it does, what paramaters it takes, and what it returns.
- Every route should have typed request and response schemas.
- Generate new orval schemas once you implement new routes or schemas.
- If new fields are added to the database, throughly test the automatic database migrations before pushing.
- Use python type hinting as much as possible.

See [Managing the Backend](/docs/managing-the-backend.md) for more information on working with backend code.

## AI Use
Please keep the following in mind when using AI tools to contribute to Open Scouting:

- PRs, issues, or code that were written entirely with the use of any kind of AI will not be accepted.
- AI use is permitted for overall feature planning, suggestions for improvement to your contribution, or help on complex implementations. 
- If you use AI to write small pieces of code, it should be refactored, throughly tested, and reimplemnted by a human before becoming part of Open Scouting.
- AI for boilerplate code (used as a inline suggestion tool) is permitted.
- **If you cannot understand the code you are contributing, it is not a good contribution.**

Use AI as a tool for help suggest solutions for complex implementations, to understand parts of Open Scouting you may not understand, and to write boilerplate. Do not use AI to implement entire features, components, or routes.