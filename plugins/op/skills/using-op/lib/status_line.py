#!/usr/bin/env python3
import subprocess
import sys


def sh(args: list, cwd: str) -> tuple:
    try:
        out = subprocess.run(args, cwd=cwd, capture_output=True,
                             text=True, timeout=10)
        return out.returncode, out.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return 1, ""


def gather(repo: str, run=sh) -> dict | None:
    code, branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo)
    if code != 0 or not branch:
        return None
    _, porcelain = run(["git", "status", "--porcelain"], repo)
    code, counts = run(["git", "rev-list", "--left-right", "--count",
                        "@{upstream}...HEAD"], repo)
    if code == 0 and counts:
        behind, ahead = (int(x) for x in counts.split())
        upstream = True
    else:
        behind = ahead = 0
        upstream = False
    code, pr = run(["gh", "pr", "view", "--json", "url", "-q", ".url"], repo)
    pr_url = pr if code == 0 and pr.startswith("http") else ""
    return {"branch": branch, "dirty": bool(porcelain), "ahead": ahead,
            "behind": behind, "upstream": upstream, "pr": pr_url}


def format_line(state: dict | None) -> str:
    if state is None:
        return "git: not a repository"
    branch = state["branch"] + ("*" if state["dirty"] else "")
    if not state["upstream"]:
        push = "no upstream"
    elif state["ahead"] == 0 and state["behind"] == 0:
        push = "pushed"
    else:
        parts = []
        if state["ahead"]:
            parts.append(f"{state['ahead']} ahead")
        if state["behind"]:
            parts.append(f"{state['behind']} behind")
        push = ", ".join(parts)
    pr = state["pr"] or "no PR"
    return f"git: {branch} — {push} — {pr}"


if __name__ == "__main__":
    print(format_line(gather(sys.argv[1] if len(sys.argv) > 1 else ".")))
