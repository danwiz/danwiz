# Git Platform Architecture

## Authoritative platforms

- **GitHub:** authoritative public source for the Dane Wisdom profile, GitHub Pages portfolio, flagship open-source work, repository modernization, public documentation, issues, projects, pull requests, releases, and Actions.
- **Google Drive:** business records, research briefs, governance documents, source registers, working files, and production documentation requiring collaborative editing or controlled workspace organization.
- **GitLab:** future secondary mirror, CI/CD portability environment, DevSecOps laboratory, and possible self-managed demonstration platform after GitHub repositories are stable.
- **External AI providers:** accessed through provider-neutral interfaces and documented selection criteria.

## AI architecture decision

GitHub Models is not a forward-looking platform dependency. Do not design new Wisdom Technologies applications, assessment workflows, documentation systems, or repository automation around the GitHub Models playground, catalog, inference API, or bring-your-own-key functions.

Use a provider-neutral AI service boundary instead:

```text
Application or workflow
        ↓
AI service interface
        ↓
Policy, logging, budget, and safety controls
        ↓
Approved model provider adapter
```

The interface should support:

- provider and model substitution;
- explicit data-handling classification;
- configurable prompts and policies;
- cost and usage logging;
- timeout, retry, and fallback behavior;
- human approval for consequential actions;
- evaluation against stable test cases;
- removal of a provider without redesigning the calling application.

## GitHub integration principles

1. Repositories remain usable without an AI subscription.
2. AI-generated changes pass through normal issues, branches, pull requests, tests, and review gates.
3. Secrets and personal or client data are never inserted into prompts or public repository artifacts.
4. Copilot features are optional productivity aids rather than architectural dependencies.
5. GitHub Actions workflows remain deterministic where practical and disclose any AI-dependent step.
6. Paid AI-credit usage requires an approved budget and measurable purpose.

## GitLab mirror strategy

Mirror only stable, governed repositories. Validate that builds, tests, release metadata, documentation, and CI behavior remain portable. Do not duplicate paid AI-agent capabilities merely for feature parity.
