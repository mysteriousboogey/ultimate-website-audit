# Ultimate Website Audit

A portable agent skill for evidence-based **SEO, AEO and GEO** website audits. Audits one site or compares multiple sites, with concise findings, practical fixes and reproducible readiness scores.

## Use it with your assistant

Download or clone this repository. Import the whole folder into a host that supports Markdown skills, or add it as project files and ask the assistant to read [SKILL.md](SKILL.md). Detailed setup, capability requirements, Windows/POSIX commands and manual-chat usage are in [runtime.md](references/runtime.md).

```text
Read SKILL.md and its linked references, then audit https://example.com.
```

```text
Audit these websites for SEO, AEO and GEO: URL1, URL2, URL3.
```

If the host accepts a filesystem skills directory:

```sh
python3 scripts/install.py --dest /absolute/path/to/host-skills/ultimate-website-audit
```

Use the destination documented by your assistant host. Existing folders are never overwritten.

## Compatibility

Model-independent: there is no provider SDK, model identifier, subscription or API-key requirement. Full operation needs an assistant with file reading, public web retrieval and Python 3.10+. Browser rendering enables additional checks. Another installed skill is not required.

This does **not** mean every LLM product can install or run it natively. Text-only chats cannot crawl sites or execute Python; use the documented manual evidence workflow instead. Hosts may require a different import process or forbid code/network access. No host/model integration is claimed as tested unless stated below.

## What the scores mean

Separate SEO, AEO and GEO scores, with **Overall = 50% SEO + 25% AEO + 25% GEO**. 80–100 is Good; below 80 Needs improvement. Unknown checks do not become failures or passes. Coverage is reported; incomplete audits are provisional. Scores measure observed readiness, not actual ranking or citation probability.

The assistant collects and interprets evidence using a fixed rubric. Python calculates the arithmetic. This repository is not a standalone autonomous crawler or an SEO SaaS service.

## Verify your installation

```sh
python3 scripts/test_score.py
python3 scripts/test_install.py
python3 scripts/score.py examples/audit-input.json
```

The example is intentionally unassessed and returns null scores. No paid services are needed for these checks.

Local validation: macOS, Python 3.14; calculator and installation tests. Scrapling 0.5.1 HTTP extraction was used for the research. The included GitHub Actions workflow is configured for Windows, Linux and macOS with Python 3.10/3.12/3.14; a configured matrix is not a passing result until its run succeeds. Other LLM hosts, a full client-site audit and browser rendering have not been tested.

## Research and constraints

[Research notes and authoritative sources](references/research.md), [audit methodology](references/methodology.md), [weighted rubric](references/rubric.json). Research checked 7 November 2026. Current official guidance takes precedence over older industry recommendations. The skill distinguishes documented requirements from emerging practices, avoids special AI-markup myths and never guarantees ranking or citation gains.

Crawl only authorized public content, respect robots/terms, avoid private/sensitive data, and do not bypass paywalls or authentication. Evidence quality and assistant judgement limit audit quality. No website modifications are performed.
