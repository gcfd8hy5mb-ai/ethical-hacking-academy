# Batch 8–15 practical coursework verification register

**Status as of 2026-11-14:** GitHub repository files were verified on the development branch. The Python 3.11/3.12 regression workflow was committed as `.github/workflows/coursework-practical-tests.yml`. No successful Python test run has yet been observed; a Vercel deployment/check success is **not** a Python test result. This audit is not independent academic or professional sign-off.

## Coverage inventory

| Batch | Executable practical | Test file | Test methods claimed in authored test | Status |
|---|---|---|---:|---|
| 8 | Workbook plus existing Batch 7 localhost fixture | No dedicated Batch 8 test found in this review | N/A | Manual and editorial review outstanding |
| 9 | Offline fictional investigation and evidence integrity | `tests/test_batch9_independent_investigation.py` | 6 | Written; execution pending |
| 10 | Real HTTP service on literal `127.0.0.1` | `tests/test_batch10_live_defense_practicum.py` | 7 | Written; execution pending |
| 11 | Synthetic Windows/Linux/SOC event correlation | `tests/test_batch11_soc_correlation.py` | 7 | Written; execution pending |
| 12 | Inert forensic and recovery evidence | `tests/test_batch12_forensics_triage.py` | 7 | Written; execution pending |
| 13 | Synthetic authorized security assessment/report | `tests/test_batch13_assessment_reporting.py` | 8 | Written; execution pending |
| 14 | Offline identity/segmentation/detection model | `tests/test_batch14_enterprise_architecture.py` | 8 | Written; execution pending |
| 15 | Offline vulnerability-management and automation | `tests/test_batch15_defensive_automation.py` | 7 | Written; execution pending |

**Expected authored test-method count across Batches 9–15: 50**. This is an inventory count, **not** 50 passing tests. The Batch 8 content is a workbook rather than an independent new executable assessment.

## CI workflow details

The newly committed workflow listens only to changes on `coursework/batch8-independent-incident-response` and a manual dispatch trigger. It has **read-only repository permissions** and no deployment, merge, publishing or secret-handling step. It checks Python syntax and runs each Batch 9–15 test file with the standard-library `unittest` runner on Ubuntu and Python 3.11 and 3.12. It intentionally makes no changes to student progress, Firebase or production.

**Important:** Push-trigger execution and check availability depend on repository GitHub Actions settings. If no Actions run appears, inspect repository Actions permissions, workflow listing and whether the newly added branch workflow is enabled. No run or success is implied by the presence of the YAML file.

To execute independently on a laptop with Python 3:
```bash
for batch in 9 10 11 12 13 14 15; do
  python3 -m unittest discover -s tests -p "test_batch${batch}_*.py" -v || exit 1
done
```

On Windows PowerShell:
```powershell
9..15 | ForEach-Object {
    py -3 -m unittest discover -s tests -p "test_batch${_}_*.py" -v
    if ($LASTEXITCODE -ne 0) { throw "Batch ${_} tests failed" }
}
```

## Acceptance gates before considering merge

1. **Automated suite:** Record exact per-batch, per-Python-version pass/fail totals; fix test, code or portability defects, and rerun until results are reproducible. Test only the development branch.
2. **Real localhost lab:** On Windows and Linux, run Batch 10's service on loopback only. Verify a degraded state, repair it and record expected real HTTP outcomes. Confirm that the private route remains denied.
3. **Offline fixtures:** Initialize a brand-new workspace, confirm the blank score, submit the correct choices, verify expected score and show that modified evidence invalidates results. Never modify an existing student's workspace.
4. **Mobile/Desktop navigation:** Open Real Computer Labs from both an iPhone Safari/PWA and desktop browser. Verify Batch 8–15 entries, readable preformatted commands and workbook access. A Markdown file link can be downloaded or displayed as raw Markdown depending on hosting and should be checked.
5. **Progress safety:** Verify lesson completion, exam history, localStorage, authentication and Firebase progress before/after navigation on **test profiles only**; don't use or overwrite actual student records. The standalone scripts are designed not to touch them, but cross-device persistence was not tested.
6. **Curriculum quality:** Independently review the explanations, technical accuracy, difficulty, answer-key exposure, learning outcomes and terminology. A workbook with published answers cannot substitute for a blinded independent practical exam.

## Current blockers / limitations

- The working container could not clone GitHub because DNS resolution for `github.com` failed. Connector access allowed repository commits and file verification, not local test execution.
- The available commit workflow lookup returned no pull-request-triggered runs; it does not establish whether a push-triggered Actions run happened.
- No confirmed regression test execution, Windows/Linux physical-device practical, iPhone Safari walkthrough, independent penetration-test assessment or external academic sign-off yet.
- **No production deployment or merge was performed.** Vercel statuses on branch commits are preview checks, not proof of curriculum functionality.

## Next technical steps

Collect actual GitHub Actions test results or execute the suite on a personal laptop; isolate and correct any failing cases in the same branch. Then run a targeted browser/OS acceptance matrix before proposing a draft PR or merge. Do not inflate instructional content count, passing test count or academic-equivalence claims.
