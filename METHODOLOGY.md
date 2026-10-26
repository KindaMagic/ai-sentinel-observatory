# AI Sentinel Observatory · Public methodology v0.2
**Prepared:** 26 October 2026. **Status:** Independent public-interest pilot; human safety review pending.

## Purpose
Provide a transparent, readable evidence register of publicly documented events related to AI control, containment, security and oversight. This is an early-warning **research aid**, not real-time operational monitoring, an extinction-risk forecast, a safety certification or an emergency-response service.

## Boundary between components
- **Private watch**: a scheduled ChatGPT task that checks public sources daily and may notify the owner if there are credible new developments. Not publicly accessible, not a security sensor, cannot inspect private systems.
- **Public observatory**: a static, dated, read-only website. It updates **only when an editor deliberately publishes a reviewed revision**. It does not automatically receive results from the private watch.
- **Offline register v0.1**: an optional local evidence-entry tool. Its browser-local records are *not* automatically published, reviewed, shared or backed up.

## Sources and observations
1. Record the original event date separately from the date a report was published.
2. Provide direct URLs to primary sources and note their institutional roles (operator, independent evaluator, regulator, investigative reporter).
3. Distinguish test environment from real deployment and confirmed consequences from attempted actions.
4. Give the most important alternative explanation, uncertainty or missing verification.
5. Do not assume a company's statement about remediation is independently verified.
6. Distinguish a new incident from a follow-up report about an old incident.

## Human-approved triage rubric
- **Green**: no qualifying new event found in the observed sources; not an all-clear.
- **Amber**: credible risk signal or emerging but unresolved event.
- **Orange**: significant primary-documented real-world control failure or independently documented major oversight weakness; requires escalation for specialist review.
- **Red**: severe ongoing real-world loss-of-control incident independently corroborated and expressly confirmed by a qualified human reviewer.

**No public rating is assigned in the first pilot snapshot.** The separate automated watch generated Orange private triage on 26 October, but it was not independently human-validated. Review must precede any rated public alert.

## Public traffic lights (editorial watch, separate from the formal rubric)
The website now displays a **three-light evidence-attention indicator**: Green, Amber, Red. On **26 October 2026**, it displays **AMBER WATCH** because several recent, primary-source reports warrant scrutiny. It is **provisional and dated**, not a certified AI threat level, and does not supersede the four-level human-approved triage rubric above.

- A green watch would mean no qualifying new reports in *the sources checked*, never a guarantee of safety.
- An amber watch means credible documented concerns requiring scrutiny, including unverified repairs or consequential evaluation failures. It is **not** a prediction of imminent catastrophe.
- A red light must **not** be displayed unless a qualifying severe ongoing incident is independently corroborated and authorised through the human-review process.
- Orange remains available as a **formal escalation category**, distinct from the simplified public-facing traffic lights. Neither an automated Orange suggestion nor an Amber watch counts as a formal approved public rating.
- **The traffic light is manually updated in source files** and must show an assessment date. It is not automatically updated by the private scheduled watch. Old status dates must not be presented as today's assessment.


## Publishing and governance guardrails
- No automatically published Orange/Red alerts; human editor authorises each public revision.
- At least two sources for major claims wherever available; where unavailable, publish the verification gap plainly.
- Red should require an accountable qualified human reviewer plus second independent expert review, if time permits.
- Never browse purported secrets, seek restricted access, probe third-party systems or run potentially dangerous demonstrations.
- No automated control, shutdown, external messaging, accusations or enforcement.
- Keep a dated public corrections log for amendments; preserve removed claims with explanations.
- No identifying personal data of developers, targets or security researchers unless necessary and already responsibly public; do not reproduce exploit steps.

## Publication checklist
[ ] Human editor reviews every entry and original source.
[ ] Confirm all URLs are available and editorial summaries accurately reflect those sources.
[ ] Confirm the date on the page, incident ID references and public review status.
[ ] Establish an accountable editorial contact and a corrections channel before soliciting public submissions.
[ ] Apply a version tag, save an immutable local copy of the published JSON and HTML.
[ ] Use static hosting with HTTPS; do not add analytics or forms without considering privacy obligations.
[ ] Follow up serious claims with independent expert validation before making extraordinary warnings.

## Limitations
This prototype provides no live model telemetry; an unreported incident will be invisible. It cannot enforce guardrails on external AI developers or prevent catastrophic outcomes. A model assessing AI safety is not impartial self-verification.