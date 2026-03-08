import { VERSION } from "./constants";

export function main() {
    console.log(
        `%c\n\nOpen Scouting %c${VERSION}\n%cgithub.com/FRC-Team3484/open-scouting\n\n\n`,
        "color: #ff5151; font-weight: bold;",
        "color: #9e9e9eb3;",
        "color: #45b0ff;",
    );
}