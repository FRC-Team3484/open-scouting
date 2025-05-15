<div align="center">

  ![Open Scouting logo](repo/images/icon.png)

  <h1>Open Scouting</h1>

  **An open source application for easier scouting at First Robotics competitions**

  **[Live Server](https://206.189.255.232/) ● [Releases](https://github.com/FRC-Team3484/open-scouting/releases) ● [Issues](https://github.com/FRC-Team3484/open-scouting/issues) ● [Development branch](https://github.com/FRC-Team3484/open-scouting/tree/development)**

</div>

<div align="center">

  ![Open Scouting screenshot on mobile](repo/images/mobile.png)

</div>

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=django,python,html,css,js,tailwind" />
  </a>
</p>


## Features
- Save data offline in case of poor connection in the stands
- Work with The Blue Alliance's API to grab match data allowing to autofill team numbers
- View all data from an event in a table
- Have a system for quickly setting up all the required data entries for a new season
  - Have fields to quickly set up and provide to the user when scouting, e.g. "text", "boolean", "data" ect.
- Allow other teams to view and contribute data to the same server
- Create custom events if events aren't listed on TBA
- Keep backups of scouting reports locally
- Dark/light mode theme support
- Manually go offline in case of bad connection
- Scout team's pits at competition
- View and filter data for multiple teams at multiple events and filter that data by a specific recorded stat
- Scouts can select what field position they're watching (Red 1, Blue 2, ect.) and the team number for them to watch will be autofilled
- Match numbers are automatically incremented, meaning scouts only need to enter the match they're scouting and the match type and everything else will be filled in for subsequent matches
<!-- - Tie multiple clients together into a "session" so all the devices can be sent to the next match simultaneously -->
  <!-- - This will iterate the match number and help autofill some additional information -->
<!-- - Auto jump to the next section that needs filled out -->

## Installation
- Follow the steps in [Development Installation](./docs/Development_Installation.md) for how to get Open Scouting up and running locally for development or contributing
- Follow the steps in [Production Installation](./docs/Production_Installation.md) for how to get Open Scouting installed on a server for production use


## Contributing
Contributions are welcome to this project! Please see the [issues](https://github.com/FRC-Team3484/open-scouting/issues) page or the [roadmap](/docs/ROADMAP.md) for any current bugs or features that need implemented. Features in the roadmap should be prioritized over features as an issue, although any help is always appreciated.

You can view the guide on how `season_fields.py` is formatted [here](/docs/Formatting_Season_Fields.md) if your contribution involves this file

Additionally, there's a document explaining how to use several systems provided in the client that may be needed while adding new features [here](/docs/Client_Systems.md)

When contributing, please fork this repository (ensure you uncheck the "Copy the `main` branch only" check box, this gives you access to the `development` branch with the latest changes)

Next, create a new branch and implement your changes. You can install this project locally for testing by following the steps in [Development Installation](#development-installation). Once you've made your changes, please open a pull request into the `development` branch, and your changes will be reviewed and merged

Eventually, `development` will be merged into `main` and your changes will be released into production with a new release. Thanks for your contribution!

## To-Do
Please see the [roadmap](/docs/ROADMAP.md) for the currently planned out things that need to be completed. Additionally, see the [issues page](https://github.com/FRC-Team3484/open-scouting/issues) for any current bugs or features that need implemented, but aren't officially scheduled.