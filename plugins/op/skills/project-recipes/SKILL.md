---
name: project-recipes
description: Use when an op command needs a per-project operation (serve, build, test, deploy, sync, release, live URL) — reads, discovers, and heals .claude/op.json in the target repo.
---

# Project recipes

Per-repo ops live in `.claude/op.json`, committed, never secret. SSH aliases (e.g. `myhost`) are fine; tokens and passwords never enter this file.

## Schema

All keys optional. A command that needs a missing key runs Discovery; gated actions (deploy, publish) refuse rather than guess.

```json
{
  "serve": "python3 -m http.server 8080",
  "build": "./build.sh",
  "test": "python3 -m pytest -q",
  "deploy": "ssh myhost 'cd /srv/www/<proj> && git pull && ./build.sh'",
  "sync": { "db": "<cmd>", "images": "<cmd>", "feed": "<cmd>" },
  "release": { "versions": ["package.json"], "publish": "npm publish", "verify": "<url>" },
  "live_url": "https://example.com",
  "cache_check": "curl -s \"$URL?v=$BUST\" | grep <marker>",
  "smoke": ["<url1>", "<url2>"],
  "rollback": "<cmd>"
}
```

`$URL` and `$BUST` are the only substitutions: the caller replaces them with `live_url` and a fresh cache-buster value at run time.

## Discovery (on missing file or key)

1. Read AGENTS.md / CLAUDE.md, `scripts/`, `package.json`, Makefile, and any existing `.claude/skills/` in the repo (per-repo ops skills often already document deploy and serve).
2. Draft the key(s) and present them as an arrow-choice: proposed value / edit / skip.
3. Write the confirmed keys to `.claude/op.json` (create the file if absent, merge if present). Show the diff.

## Self-heal (on a failing recipe command)

1. Show the failing command and its error.
2. Rediscover that key (step 1 above), propose the fix as an arrow-choice.
3. Update the file on confirm, then retry once.

Hard stop: never invent a deploy, publish, or sync target that is not in the file or explicitly confirmed by the user this session.
