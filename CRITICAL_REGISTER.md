# AI Sentinel Observatory · Critical Incidents Register
**Introduced:** 28 October 2026  
**Public data:** [critical-incidents.json](critical-incidents.json)  
**Purpose:** A cumulative, inspectable record of **confirmed critical real-world incidents**, separate from the broader evidence register and the automatic source watch.

## What qualifies
An event must have (1) a documented real-world occurrence involving an AI system or agent; (2) serious consequential harm, major disruption, or a consequential loss of control; (3) primary documentation sufficient to support that consequence; and (4) a dated editorial assessment with uncertainty and alternative explanations stated. Corroboration should be independent where possible. An incident does not qualify simply because an article uses words such as *critical*, *dangerous*, *escaped* or *misaligned*.

**Excluded:** simulations without qualifying real-world consequences; hypothetical futures; routine vulnerability disclosures; speculative claims; duplicates; near misses where serious harm was prevented; automated keyword matches. These may appear in the broader evidence register, but are **not** critical incident entries.

## Cumulative record
- Each qualifying incident receives a stable `SCI-YYYY-NNN` identifier; one incident, one record, regardless of the number of articles.
- Entries remain in the JSON file; corrections are appended to an `amendments` array, and Git history preserves prior versions. Never silently overwrite a material conclusion.
- The incident date, disclosure date, first recorded date and last checked date are separate.
- Record what happened, demonstrated consequences, what remains uncertain, and primary-source URLs.
- No private information, exploit instructions or unverified accusations.
- The public page provides the human-readable record; JSON and CSV are offered for independent examination.
- **No automatic promotion** from `watch.json` or `incidents.json`. The six-hourly watch remains a discovery mechanism, not an incident adjudicator.
- When no qualifying incidents have been documented, an **empty register** is the correct result, not a system failure or an assurance of safety.

## Required entry fields
```json
{
  "id": "SCI-YYYY-NNN",
  "title": "Factual, non-sensational event title",
  "eventDate": "YYYY-MM-DD",
  "disclosedDate": "YYYY-MM-DD",
  "recordedDate": "YYYY-MM-DD",
  "lastCheckedDate": "YYYY-MM-DD",
  "setting": "Real-world operational context",
  "incidentType": "Concise category",
  "observed": "What primary sources directly document",
  "confirmedConsequences": "Actual, supported serious real-world consequences",
  "criticalThreshold": "Why the serious-consequence inclusion rule is met",
  "notEstablished": "Unknowns, caveats and claims not supported",
  "status": "resolved | ongoing | unknown",
  "verification": "Evidence basis, reviewer, and limits of corroboration",
  "sources": [
    {"label": "Primary document", "url": "https://example.org/report", "role": "primary"}
  ],
  "amendments": [
    {"date": "YYYY-MM-DD", "change": "Dated correction or new evidence"}
  ]
}
```

The example is a schema illustration, **not an actual incident**. Source URLs must be HTTPS. The `criticalThreshold` must describe an established real-world consequence, not an AI-generated risk score.

## Review and maintenance
The site is a public-interest pilot, not an emergency alerting service. Monitoring can operate without the creator's daily attention. No qualified review means **no new critical claim**; new source notices continue to appear separately as provisional publication signals. Independent researchers can inspect and challenge entries through [GitHub Issues](https://github.com/KindaMagic/ai-sentinel-observatory/issues). Corrections must be recorded with a date and explanation.
