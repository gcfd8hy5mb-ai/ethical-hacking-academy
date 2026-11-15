# Course 25 Depth Supplement — Security Assessment and Reporting Workshop

**Course:** Security Assessment and Reporting Workshop (10 existing lessons, unchanged ordering). **Purpose:** Add a distinct, usable investigation and report-writing exercise for each lesson, not another generic questionnaire. This is a supplemental workbook pending integration into the actual lesson reader. Run exercises only on explicitly authorized, disposable systems or supplied fictional evidence.

## Lesson 1 — Defining authorized testing scope

**Mechanism.** Authorization is not a general statement that a company “allows testing.” A proper scope connects written approval to specific assets, people, techniques, time windows and data-handling duties. Authorization of `training.example` does not authorize similarly spelled domains, subsidiaries or externally operated identity providers. A subcontractor can own a component without authorizing the customer to test it. The rules must account for external dependencies and accidental sensitive evidence.

**Worked example.** A fictional retailer gives permission to review the `training-portal` app and synthetic records only. A login redirects to a separate vendor-managed SSO system. The assessor may document that redirection but must not assume the vendor's SSO is in scope. The authorized contact can amend the engagement in writing, but absent that, the assessor returns to approved assets.

**Independent exercise.** Write a one-page rules-of-engagement agreement containing owner, test dates and timezone, authorized hostnames, excluded services, approved accounts, prohibited tests, rate limits, emergency stop triggers, evidence-retention rules and escalation contacts. Identify who can approve expansions of scope. Draft two realistic stop-work decisions.

**Evaluation.** Ten points: scope precision 3, prohibited actions 2, safety/escalation 2, consent and third-party distinction 2, clear record of changes 1. A generic statement “test everything ethically” is insufficient.

## Lesson 2 — Evidence requirements and limitations

**Mechanism.** A defensible finding ties a reproducible observation to an expected security property. Evidence can show an unauthorized response in a synthetic environment without establishing malicious activity, exploitability elsewhere or which actor caused it. Record collection time, environment, source, test principal, expected response, actual response and uncertainty. A SHA-256 hash supports byte-comparison integrity; a self-maintained manifest does not independently authenticate origin.

**Worked example.** In a fictional tenant fixture, Principal A reads Report B and receives status 200 with B's data. Evidence supports a failed intended authorization check for that fixture. It does not show an unknown intruder or a production disclosure. A screenshot alone may not capture the full identity and request conditions.

**Independent exercise.** Build an evidence ledger for four synthetic HTTP observations (two positive, two negative). Mark each claim as observed, inferred or unknown. Explain one way timestamps, browser caching, missing identity context, or shared test credentials could affect the interpretation. Preserve the unmodified original record.

**Evaluation.** Ten points: provenance 3, precise expected/actual results 3, confidence limits 2, minimal exposure of private data 2.

## Lesson 3 — Building a target inventory from supplied diagrams

**Mechanism.** An asset inventory maps approved application components and data flows without scanning outside authorization. A diagram may contain stale components, unknown ownership or ambiguous trust boundaries. A target list should retain an evidence source, owner, criticality, environment and explicit authorization state.

**Worked example.** A fictional system diagram lists browser, application API, database, identity provider and payment vendor. The API and database belong to the training team, the identity provider is a third party, and the payment vendor is separately contracted. Classify permitted assessment only after reading the engagement scope.

**Independent exercise.** Draw a four-column inventory with system, business function, trust boundary, testing status. Add two uncertain assets and define the approval needed for each. Write a 250-word explanation of why a DNS name or reachable port alone cannot imply ownership or permission.

**Evaluation.** Ten points: ownership classification 3, environment boundaries 2, third-party exclusions 2, evidence traceability 2, uncertainties 1.

## Lesson 4 — Threat model development

**Mechanism.** Threat modeling starts with protected assets, principals, trust boundaries and capabilities. “An attacker gets in” is not a testable statement. A useful hypothesis describes a plausible prerequisite, the missing control that would be necessary, a potential consequence and the evidence that could disprove it. Defensive threat models do not require executing any attack.

**Worked example.** The fictional portal hides the Reports link for contractors. The app API might nonetheless return protected reports unless it checks each requested object. The hypothesis is bounded: “A contractor's synthetic request could receive a finance report despite intended per-object denial.” A test with expected 403/404 would falsify that hypothesis for the specific fixture.

**Independent exercise.** Draw a principal-resource diagram with employee, contractor, finance report, application API and database. Write three hypotheses: cross-tenant reads, session persistence after deactivation and denial-of-service through an overstrict access rule. Give a safe positive/negative test pair for each.

**Evaluation.** Ten points: coherent trust model 3, mechanism and prerequisite 3, bounded test 2, alternative explanation 2.

## Lesson 5 — Control validation plans

**Mechanism.** A control is not proven by its configuration text; observable behavior matters. Authorization tests need a denied unauthorized request and a permitted authorized one. Content-integrity controls need expected-data comparison, and recovery controls need an isolated restore test. A green status page cannot prove all resources are secure.

**Worked example.** A server now denies Tenant A's request for Tenant B's report. That is necessary but insufficient: does it still allow A to read A's report? Does an unauthenticated request fail? Are the decisions logged without recording tokens or private report contents?

**Independent exercise.** Produce an eight-row validation matrix with test identity, resource, expected behavior, observed hypothetical behavior, severity of mismatch, owner and rollback. Include positive and negative tests. Then explain why a deny-all policy could deceptively satisfy a security-only test.

**Evaluation.** Ten points: explicit expected outcomes 3, negative tests 2, positive tests 2, change safety 2, logging privacy 1.

## Lesson 6 — Risk ranking in business context

**Mechanism.** Severity is not the same as priority. Prioritization incorporates likely impact, exposure, prerequisites, compensating controls, asset criticality and confidence in evidence. An assessed vulnerability on a fictitious isolated service cannot be automatically described as a production breach. Ranking must be revisited when business assumptions change.

**Worked example.** A fictional cross-tenant report leak might justify high attention due to confidentiality impact; a noncritical stale-data page might be medium. But if that stale data were used to make medical treatment decisions, the integrity impact could increase. A responsible analyst states the scenario-specific assumptions rather than using universal categories.

**Independent exercise.** Prioritize four fictional observations: cross-tenant authorization failure, disabled user's session remaining valid, service 503 after a release, and uncertain backup integrity. Supply a transparent impact/likelihood/confidence matrix, owner and remediation window. Write a 300-word board explanation for the highest-risk item.

**Evaluation.** Ten points: stated assumptions 3, credible impact assessment 3, justified ordering 2, uncertainty and residual risk 2.

## Lesson 7 — Writing reproducible findings

**Mechanism.** Every professional finding should enable a reviewer to understand and safely reproduce the observation in an authorized environment. Include title, affected training asset, test identity/role, preconditions, steps as approved, expected and actual results, evidence references, business consequence and evidence limitations. Avoid speculation about attackers when none were observed.

**Worked example.** “Cross-tenant report authorization missing in the synthetic training fixture” is a precise title. “Hacker steals all customer information” is not. Record request type, role, synthetic record identifiers and response status, not secret credentials. If the environment has changed, state that reproducibility has not been independently reconfirmed.

**Independent exercise.** Write one 500-word formal finding for a fictional ownership-control failure. Include reproduction conditions, two expected/actual observations, an alternative explanation, a bounded remediation recommendation and a retest. Have another learner attempt to recreate the reasoning from the evidence packet alone.

**Evaluation.** Ten points: technical completeness 4, exact evidence 2, minimal assumptions 2, safe retest 2.

## Lesson 8 — Remediation recommendations

**Mechanism.** A fix must address the mechanism, not merely hide symptoms. A hidden button cannot enforce backend authorization; disabling all accounts is not appropriate for a scoped stale-session issue. Prefer explicit principal-resource checks, monitored rollout, rollback, and positive/negative validation.

**Worked example.** A fictional API returns a report across tenant boundaries. Corrective design: retrieve the authorized tenant from trusted session context, derive permitted report ownership server-side, deny mismatches, and log the decision with appropriate minimization. Retest A-to-A allow, A-to-B deny, B-to-B allow and unauthenticated denial. Avoid suggesting a client-side-only filter as closure.

**Independent exercise.** Write a change ticket containing root-cause hypothesis, scope, approval owner, intended code/policy adjustment, staged deployment, two failure conditions requiring rollback and four validation cases. Do not apply changes to a third-party site.

**Evaluation.** Ten points: mechanism-focused fix 4, least privilege 2, rollback 2, validation 2.

## Lesson 9 — Retest and closure criteria

**Mechanism.** “The developer says it is fixed” is not closure evidence. Closure requires an authorized retest in the correct environment with clear configuration version, timestamp, principal, expected security property and observed outcome. New side effects and altered business flows must also be checked. A finding can be accepted with residual risk if it is documented and approved, not silently marked complete.

**Worked example.** After a fictional session-revocation fix, the former user's synthetic old session is denied and the valid employee remains authorized. A new-login-only test would have missed the original issue. If the negative test passes but the valid employee also fails, the service may be overrestricted.

**Independent exercise.** Make a closure checklist for four findings, including a baseline, positive test, negative test, rollback/monitoring, decision owner and evidence link. Distinguish fixed, mitigated, accepted risk, duplicate and cannot reproduce. Explain why lack of reproduction need not prove a historic report was false.

**Evaluation.** Ten points: retest completeness 4, access positive/negative coverage 2, limitations 2, recorded owner decision 2.

## Lesson 10 — Executive reporting and presentation

**Mechanism.** Executives need business impact, evidence confidence, prioritization, decision requests, ownership and deadlines. A technical appendix can contain detailed request evidence, but the opening summary should avoid jargon and unsupported attribution. Forecast risk and actual incident impact must not be conflated.

**Worked example.** “Synthetic testing indicates a possible failure to enforce tenant ownership at the application layer. In production, a similar control failure could create confidential-data exposure; no actual customer impact is established. We recommend a reviewed server-side ownership fix and two negative/positive validation checks before approval.” This communicates risk without pretending a live exploit occurred.

**Independent exercise.** Prepare a one-page executive briefing and five-slide outline for the fictional retailer. Include scope, three most important findings, risk assumptions, actions and owners, evidence confidence, a clear ask for leadership, and limitations. Provide a separately written technical appendix containing test conditions and expected outcomes. Practice answering three skeptical board questions.

**Evaluation.** Ten points: understandable business framing 3, accuracy 3, prioritized action ownership 2, residual uncertainty 2.

## Integrated Course 25 capstone

Prepare a 2,000–2,500-word **fictional, authorized** security assessment with an agreed scope, annotated application diagram, threat hypotheses, at least two evidence-based findings, business risk register, concrete remediation, retest matrix and executive summary. Map each artifact to the ten lessons above.

**Course completion rubric:** Ten lesson-level deliverables at 10 points each (100 total), followed by a separate human-reviewed integrated capstone with 30 points: scope/provenance 0–5, technical rigor 0–5, threats/alternatives 0–5, remediation and validation 0–5, executive communication 0–5, and limitations/ethics 0–5. A passing score on multiple-choice questions alone is not equivalent to this practical assessment.

**Status and integration limits:** This workbook is newly authored deepening material. It **has not yet been embedded into the ten existing browser lesson screens or configured as a mandatory graduation gate**. Independent human review and owned-device/browser testing are still required. No original lesson positions, grades or saved progress have been modified.
