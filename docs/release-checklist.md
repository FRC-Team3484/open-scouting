# Release Checklist
Follow these steps before releasing a new version of Open Scouting

1. Create a new changelog file for the frontend
    - Follow the other changelog files and match a similar style
2. Type out the release notes on the GitHub for creating new releases
    - Be sure to follow the format from previous releases, and include a summary, screenshot, full list of changes, what issues were closed, and who contributed to this release
    - Make sure to set the tag correctly, and mark as a pre release version if the version is `alpha`, `beta` or `rc`
    - Don't submit this release yet, wait until the pull request for that version is merged
    - Use the "Save as Draft" button as needed, if the PR isn't ready to be merged yet
3. Create a pull request into `main` from the branch for this new version, and paste the release notes as the description (or make a new comment if the PR already exists)
4. Merge the version's PR into `main`
5. Publish the release

Open Scouting has now been updated to a new version!

Now, update any production servers:
```bash
cd open-scouting
docker compose down
docker compose pull
docker compose up -d
```