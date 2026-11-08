# Ethical Hacking Academy — Redesign V2 (isolated development)

This branch is an experimental redesign. **Do not merge into main or change production GitHub Pages until the user has reviewed and approved the result.**

## Guardrails
- Preserve student progress keys, Firebase authentication/cloud saves, lesson IDs, original coursework, assessments, and browser/desktop compatibility.
- Preserve the distinctive **charcoal, cream, and gold** Academy palette. Do not clone the Business Academy design.
- Preserve the recently approved **single-page natural scrolling** (no nested lab scrollbars).
- Keep the desktop **Learn / Practice split workstation**, stacking it on mobile.
- Distinguish browser simulations, local machine commands, and graded evidence; never imply a browser simulation is a real system shell.
- Keep the current deployed main branch untouched.

## V2 redesign direction
1. Polish the desktop navigation and Academy dashboard, with a coherent professional cybersecurity operations aesthetic and compact learning-path cards.
2. Refine course and lesson flows: visible progress, lightweight navigation, practical workbench with readable explanations and clear lesson sequence.
3. Improve Cyber Range presentation: organized lab disciplines, task objectives, simulated output, evidence capture and clear assessment states.
4. Refine mobile responsiveness; ensure accessible typography, tap targets, reduced-motion support and consistent styles.
5. Run existing curriculum, workstation, offline lab and checkpoint regression suites, plus new UI regression checks before proposing merge.

## Release workflow
All experiments remain on `redesign/cyber-academy-v2`. Present screenshots or a branch-specific preview for approval. Only merge to `main` with explicit approval. Do not enable GitHub Pages publishing from this branch without reviewing the deployment workflow.
