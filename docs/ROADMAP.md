# Roadmap
This document describes the roadmap for Open Scouting, and roughly when each feature should be worked on. These are separated into each upcoming [release](https://github.com/FRC-Team3484/open-scouting/releases).

---

## To-Do
### `v0.1.3-alpha`
- [ ] [#70](https://github.com/FRC-Team3484/open-scouting/issues/70) - Charts in the advanced data view don't update when the filters do
- [x] [#71](https://github.com/FRC-Team3484/open-scouting/issues/71) - Organize client side code
- [x] [#54](https://github.com/FRC-Team3484/open-scouting/issues/54) - Update Tailwind.css to v4.0
- [ ] [#60](https://github.com/FRC-Team3484/open-scouting/issues/60) - In certain cases, the `/authentication` page cannot be loaded
- [ ] [#78](https://github.com/FRC-Team3484/open-scouting/issues/78) - Show any client errors in the developer menu

### `v0.1.4-alpha`
- [ ] [#73](https://github.com/FRC-Team3484/open-scouting/issues/73) - Reimplement the ability to sort data in the advanced data view
- [ ] [#18](https://github.com/FRC-Team3484/open-scouting/issues/18) - Export data
- [ ] [#22](https://github.com/FRC-Team3484/open-scouting/issues/22) - Add the ability to import data
- [ ] [#77](https://github.com/FRC-Team3484/open-scouting/issues/77) - Auto save match scouting progress

---
## Completed
### `v0.1.2-alpha`
- [x] [#62](https://github.com/FRC-Team3484/open-scouting/issues/62) - Issues with saving and syncing pit scouting data
- [x] [#63](https://github.com/FRC-Team3484/open-scouting/issues/63) - Offline pit scouting data doesn't seem to be cleared locally properly
- [x] [#64](https://github.com/FRC-Team3484/open-scouting/issues/64) - Add a button to return to the top of the screen in pit scouting
- [x] [#26](https://github.com/FRC-Team3484/open-scouting/issues/26) - Autofill match and team numbers when contributing separately
- [x] [#66](https://github.com/FRC-Team3484/open-scouting/issues/66) - Add a field on the contribute page for indicating what kind of match
- [x] [#69](https://github.com/FRC-Team3484/open-scouting/issues/69) - Create team summaries in the advanced data view

### `v0.1.1-alpha`
- [x] Fix bugs found at competition

### `v0.1.0-alpha`
- [x] Officially hosted in production and bug fixes

### `v0.0.10-alpha`
- [x] [#19](https://github.com/FRC-Team3484/open-scouting/issues/19) - More ways to view data
- [x] [#55](https://github.com/FRC-Team3484/open-scouting/issues/55) - Create a better home page
- [x] Many requests use `@csrf_exempt` when they shouldn't

### `v0.0.9-alpha`
- [x] [#5](https://github.com/FRC-Team3484/open-scouting/issues/5) - Be able to collect pit scouting data
- [x] [#52](https://github.com/FRC-Team3484/open-scouting/issues/52) - Fetch requests in the client are using headers for large data

### `v0.0.8-alpha`
- [x] Make site able to be run out of a docker container in production
- [x] Adjust site for new repository location

### `v0.0.7-alpha`
- [x] [#44](https://github.com/FRC-Team3484/open-scouting/issues/44) - Backups database store isn't getting created correctly
- [x] [#30](https://github.com/FRC-Team3484/open-scouting/issues/30) - Add tests
- [x] [#46](https://github.com/FRC-Team3484/open-scouting/issues/46) - Authentication status isn't updated on index page due to caching
- [x] Test and try to break the application and find as many bugs as possible

### `v0.0.6-alpha`
- [x] [#16](https://github.com/FRC-Team3484/open-scouting/issues/16) - Show data in the table differently depending on the kind of field
- [x] [#23](https://github.com/FRC-Team3484/open-scouting/issues/23) - URL Parameter support on `/index`
- [x] [#20](https://github.com/FRC-Team3484/open-scouting/issues/20) - Allow the user to create an account
- [x] [#13](https://github.com/FRC-Team3484/open-scouting/issues/13) - Save the username and team number to Data

### `v0.0.5-alpha`
- [x] [#41](https://github.com/FRC-Team3484/open-scouting/issues/41) - Implement a way to show a server message
- [x] Implement 2025 season fields and examples

### `v0.0.4-alpha`
- [x] [#9](https://github.com/FRC-Team3484/open-scouting/issues/9) - Create a wiki page for how season_fields.py should be formatted
- [x] [#7](https://github.com/FRC-Team3484/open-scouting/issues/7) - Add a field for additional notes
- [x] [#25](https://github.com/FRC-Team3484/open-scouting/issues/25) - Add increment buttons to numerical values
  - [x] [#10](https://github.com/FRC-Team3484/open-scouting/issues/10) - Add 0 to season_fields.py choices
- [x] [#37](https://github.com/FRC-Team3484/open-scouting/issues/37) - Be able to collapse sections in /submit
- [x] [#38](https://github.com/FRC-Team3484/open-scouting/issues/38) - Add demo mode
- [x] [#39](https://github.com/FRC-Team3484/open-scouting/issues/39) - Non-ASCII characters in event name breaks data submission

### `v0.0.3-alpha`
- [x] [#24](https://github.com/FRC-Team3484/open-scouting/issues/24) - Implement a collapsible menu
  - [x] [#14](https://github.com/FRC-Team3484/open-scouting/issues/14) - Add a dark mode toggle
  - [x] [#4](https://github.com/FRC-Team3484/open-scouting/issues/4) - Attribute The Blue Alliance
- [x] [#17](https://github.com/FRC-Team3484/open-scouting/issues/17) - Offline use of the application

### `v0.0.2-alpha`
- [x] [#2](https://github.com/FRC-Team3484/open-scouting/issues/2) - Add custom events
- [x] [#3](https://github.com/FRC-Team3484/open-scouting/issues/3) - View events from previous years

### `v0.0.1-alpha`
- [x] Initial release with basic features