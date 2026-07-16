# rapid-stack

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE) ![Claude Code](https://img.shields.io/badge/Claude%20Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white)

Short slash-command aliases for the Claude Code skills and agents you already reach for. Plus `op`, an operator layer that carries a piece of work from spec to shipped, with proof at each step.

## Install

```
/plugin marketplace add artttj/rapid-stack
/plugin install rs@rapid-stack
/plugin install op@rapid-stack
/reload-plugins
```

Use them as `/rs:ask`, `/rs:cr`, `/rs:hum`, and so on.

## The commands

| Command | What it does |
|---|---|
| `/ask` | Answers questions about the codebase. Read-only by design. |
| `/brn` | Lightweight brainstorm. Asks clarifying questions before acting, so the model doesn't run off and hallucinate. |
| `/dbg` | Systematic debugging. Reproduce first, hypothesize from evidence, change one variable at a time. Stops guess-fixing. |
| `/10x` | Find the biggest wins in an idea. Smallest effort, largest payoff. Catches features you missed. |
| `/trim` | Simplify. Tightens recently changed code without changing behavior. Operates on the current diff. |
| `/cr` | Code review without the 40-comment pile-on. High-confidence findings only. |
| `/hum` | Self-educating humanizer skill that keeps up with the latest LinkedIn AI slop patterns. |
| `/ui` | Draft UI ideas with real UX quality across platforms. |
| `/vibe` | UI scorecard, eight dimensions plus an AI-sameness screen. Flags AI-default looks, ranks what to fix first. |
| `/polish` | Pixel-perfect cleanup pass on a design. |
| `/std` | Standards. Baseline conventions: immutability, files under 800 lines, functions under 50, named constants over magic numbers, errors handled at every layer. |
| `/prm` | Turns vague prompts into sharp ones. Works on claude.md, agents.md, system prompts. |
| `/sec` | OWASP pass. Run before anything that touches auth or new infra. |
| `/mimic` | Learn any brand from a URL or screenshot, generate a design system. Two sessions, same look. |
| `/jobs` | Argue with Steve Jobs about your product. Built from 30+ interviews, keynotes, and memos. Stays in first person until you say exit. |

## What's bundled

The plugin bundles:

- **Skills:** `the-humanizer`, `coding-standards`, `prompt-optimizer`, `design`, `game-changing-features`, `vibe-check`
- **Agents:** `code-reviewer`, `code-simplifier`, `security-reviewer`

Three commands wrap external skills. Install them separately:

```
# for /ui
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max

# for /mimic
git clone https://github.com/dominikmartn/hue ~/.claude/skills/hue

# for /jobs
/plugin marketplace add alchaincyf/steve-jobs-skill
/plugin install steve-jobs
```

`/brn` and `/dbg` also wrap external skills (`superpowers:brainstorming` and `superpowers:systematic-debugging`) but fall back to inline prompts if those skills are not installed.

## op — the operator layer

Second plugin in this marketplace. Where rs gives you single-shot aliases, op runs the whole loop: route, spec, plan, build, ship, with proof at the end of every command.

| Command | What it does |
|---|---|
| `/op:go` | Front door. Classifies the ask (bug, small fix, or feature), confirms the route, hands off. |
| `/op:spec` | Feature spec in `docs/specs/<slug>/spec.md`. You approve it with one keypress. |
| `/op:plan` | Build plan pinned to the approved spec by content hash. Think expensive, execute cheap. |
| `/op:build` | Executes the plan: TDD, subagents for big plans, capped code review, verification. |
| `/op:ship` | Commit, push, deploy, cache-busted live check, smoke test, screenshot. |
| `/op:sync` | Pull prod state (db, images, feed) to localhost per the project recipe. |
| `/op:show` | Serve locally, screenshot the responsive breakpoints (mobile, tablet, desktop), verdict. |
| `/op:release` | Bump, notes, tag, publish, verify the published artifact. |

op reads per-project ops from `.claude/op.json`. The first run discovers your serve/deploy/sync commands and writes the file. Deep disciplines come from `superpowers`, review and polish from `rs`. Both are optional: every wrapper degrades to a short inline fallback.

## Want them without the `/rs:` prefix?

 To type `/ask` or `/hum` directly, ask your agent: 
 
 *"Copy the rapid-stack commands into `~/.claude/commands/` so they work without the `rs:` prefix."* It will mirror each `.md` file into your user-level commands directory.

## License

MIT. See [LICENSE](LICENSE).

The wrapped skills keep their original licenses and authors:

- `ui-ux-pro-max`: MIT, by [nextlevelbuilder](https://github.com/nextlevelbuilder)
- `hue`: MIT, by [dominikmartn](https://github.com/dominikmartn/hue)
- `steve-jobs-perspective`: see [alchaincyf/steve-jobs-skill](https://github.com/alchaincyf/steve-jobs-skill)
- `the-humanizer`, `coding-standards`, `prompt-optimizer`, and the agents: see their respective sources
