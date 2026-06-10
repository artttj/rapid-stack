# rapid-stack

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](LICENSE) ![Claude Code](https://img.shields.io/badge/Claude%20Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white)

Best community skills packaged as short aliases. Use it to bring ideas to life fast and with good quality.

## Install

```
/plugin marketplace add artttj/rapid-stack
/plugin install rs@rapid-stack
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
| `/vibe` | UI scorecard, nine dimensions. Flags AI-default looks, ranks what to fix first. |
| `/polish` | Pixel-perfect cleanup pass on a design. |
| `/std` | Standards. Baseline conventions: immutability, files under 800 lines, functions under 50, named constants over magic numbers, errors handled at every layer. |
| `/prm` | Turns vague prompts into sharp ones. Works on claude.md, agents.md, system prompts. |
| `/sec` | OWASP pass. Run before anything that touches auth or new infra. |
| `/jobs` | Argue with Steve Jobs about your product. Built from 30+ interviews, keynotes, and memos. Stays in first person until you say exit. |

## What's bundled

The plugin bundles:

- **Skills:** `the-humanizer`, `coding-standards`, `prompt-optimizer`, `design`, `game-changing-features`, `vibe-check`
- **Agents:** `code-reviewer`, `code-simplifier`, `security-reviewer`

Two commands wrap external skills. Install them separately:

```
# for /ui
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max

# for /jobs
/plugin marketplace add alchaincyf/steve-jobs-skill
/plugin install steve-jobs
```

`/brn` and `/dbg` also wrap external skills (`superpowers:brainstorming` and `superpowers:systematic-debugging`) but fall back to inline prompts if those skills are not installed.

## Want them without the `/rs:` prefix?

 To type `/ask` or `/hum` directly, ask your agent: 
 
 *"Copy the rapid-stack commands into `~/.claude/commands/` so they work without the `rs:` prefix."* It will mirror each `.md` file into your user-level commands directory.

## License

MIT. See [LICENSE](LICENSE).

The wrapped skills keep their original licenses and authors:

- `ui-ux-pro-max`: MIT, by [nextlevelbuilder](https://github.com/nextlevelbuilder)
- `steve-jobs-perspective`: see [alchaincyf/steve-jobs-skill](https://github.com/alchaincyf/steve-jobs-skill)
- `the-humanizer`, `coding-standards`, `prompt-optimizer`, and the agents: see their respective sources
