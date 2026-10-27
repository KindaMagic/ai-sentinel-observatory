# AI Sentinel Observatory

**An independent public-interest research project by George Sfougaras.**  
Founded October 2026.

*Evidence before alarm. Human control before automation.*

AI Sentinel Observatory is an evidence-based public record of significant AI safety incidents, containment problems, monitoring weaknesses, and developments affecting human oversight.

It is intended to make primary-source reports understandable, dated, open to criticism, and clear about what has **not** been established.

## Explore

- [Observatory website](https://kindamagic.github.io/ai-sentinel-observatory/) (public website)
- [Public methodology and guardrails](METHODOLOGY.md)
- [Website source](index.html)

## What the project is

- Three source-linked historical cases in a **read-only editorial evidence register**, alongside an automatically refreshed four-source public-news screening indicator.
- A four-lamp **screening and review framework**: Green or Amber can arise automatically from public publication keyword screening; Orange and Red require documented independent human review and cannot be auto-issued. The lamps are not a global danger index.
- A research aid supporting informed discussion and independent scrutiny.

## What it is not

- It is **not** a live sensor connected to AI systems, an official emergency service, or an AI safety certification.
- It cannot detect undisclosed incidents, predict human extinction, independently shut down systems, or establish whether a system is conscious.
- The owner's separate ChatGPT scheduled news watch is **private**. It does **not** automatically write to this repository or publish its outputs.
- Automated preliminary classifications are **not public findings**. There is **no human-validated overall severity rating**.
- Different publishers may be discussing the same event; publication counts do not equal incident counts. General security-product news is not evidence of failed AI oversight.

## Editorial safeguards

We aim to:
1. Link to original published sources and distinguish the date of an event from the date it was reported.
2. Separate observations from inference and distinguish a controlled evaluation from deployment.
3. Identify conflicts, missing verification, and the limits of each report.
4. Require documented human editorial review before publication of severe assessments.
5. Correct mistakes transparently. Please use [GitHub Issues](https://github.com/KindaMagic/ai-sentinel-observatory/issues) for corrections, sources and constructive scrutiny. Do not post private or sensitive information.

The current rules and full publication checklist are in [METHODOLOGY.md](METHODOLOGY.md).

## Who to contact (UK)

The public website includes a verified UK **Who to contact** directory. **999** is for immediate danger to life or a serious emergency, **101** for non-emergency police, **0300 123 2040** for Report Fraud / organisational live cyberattack reporting, and **0303 123 1113** for Information Commissioner's Office enquiries. For significant cyber incidents, organisations can use the [NCSC reporting portal](https://report.ncsc.gov.uk/). See official sources and restrictions on the website. No number is a general AI-existential-risk hotline; no calls are sent by Sentinel.

## Hosting

The site is hosted on GitHub Pages. A GitHub Actions workflow (`.github/workflows/ai-sentinel-monitor.yml`) runs **four source checks a day**, using `scripts/monitor.py` (Python standard library; no paid AI API). It writes `watch.json` and **directly deploys the refreshed static website through GitHub Pages**, avoiding the limitation that commits made with `GITHUB_TOKEN` do not trigger an ordinary branch-based Pages rebuild. The website reads `watch.json` on each visit. The underlying news feeds, not AI systems themselves, are being monitored.

The last check and available sources are shown on the site. If checks fail, severity is unknown; a stale result is labelled after 36 hours. Keyword screening can miss dangerous incidents or flag harmless articles. Only Green/Amber publication-screening colours are automatic; Orange/Red, emergency messages and reports to authorities are **never automatically issued**. The separate `incidents.json` register remains under editorial control.

To test the workflow, use GitHub **Actions → AI Sentinel public-source monitor → Run workflow**. Its results and any failures are visible in GitHub Actions.

## Development and licensing

**Status:** Public-interest pilot (v0.6), dated 26 October 2026.  
**Creator and editor:** George Sfougaras.

No open-source licence has been selected yet. Public access to the repository is not, by itself, permission to reuse its contents under an open-source licence.

This project does not claim endorsement by the organisations whose reports it examines.
