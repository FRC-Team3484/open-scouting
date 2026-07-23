import { replaceState } from "$app/navigation";
import { page } from "$app/state";

let observer: IntersectionObserver | undefined;

function getObserver() {
    if (observer) return observer;

    observer = new IntersectionObserver(
        (entries) => {
            const visible = entries
                .filter((e) => e.isIntersecting)
                .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

            if (!visible) return;

            const team = visible.target.getAttribute("data-team-number");
            if (!team) return;

            const params = new URLSearchParams(page.url.search);
            if (params.get("pit") === team) return;

            params.set("pit", team);
            replaceState(`?${params}`, {});
        },
        {
            threshold: [0.25, 0.5, 0.75]
        }
    );

    return observer;
}

export function pitVisibility(node: HTMLElement, teamNumber: number) {
    node.dataset.teamNumber = String(teamNumber);

    getObserver().observe(node);

    return {
        destroy() {
            observer?.unobserve(node);
        }
    };
}