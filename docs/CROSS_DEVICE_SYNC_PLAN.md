# Cross-device progress sync — migration contract (draft)

Status: DESIGN ONLY. No cloud writes, migrations, or student data changes have been enabled.

## Current state
Firebase Auth implemented; cloud Firestore writes and sync not yet present in audited app.js.

## Verified browser storage keys
- `ethical-hacking-academy-progress-v1`

Other local lab, exam, portfolio and report keys must be inventoried separately before full sync.

## Required behavior
1. Authenticate and verify the user before reading or writing any remote student record. For Business and Law, implement an audited identity integration first.
2. Use per-user access controls on the backend, scoped by authenticated UID, academy namespace, and data type; never trust client-supplied identity.
3. Export and back up existing browser records before any migration. Treat browser data as authoritative for its own initial import unless the student explicitly chooses another version.
4. On first sign-in, show a review of local and cloud records. Never silently replace an existing record or delete unanswered local work.
5. Merge monotonic completion flags by union where legitimate; preserve exam attempts and graded history as distinct, immutable records with unique identifiers.
6. Treat drafts, simulation decisions, and latest working state as potentially conflicting. Retain both versions until the student resolves conflicts.
7. Make remote writes idempotent with stable operation IDs. Maintain schema version and timestamps; support retry after offline editing.
8. Keep the application usable offline with explicit pending-sync feedback; do not claim a draft is cloud-saved until the backend confirms.
9. Validate payload sizes and formats, preserve a downloadable export, and test two devices signing into the same account.
10. Avoid cross-academy mixing of grades, progress, and assessments.

## Suggested document layout
`students/{uid}/academies/ethical-hacking-academy/records/{recordId}` is a *proposed* logical layout, not an existing Firestore collection. Confirm provider and security rules before implementation.

## Acceptance criteria
- Signed-out access cannot read or change another student's data.
- First migration never reduces completed lessons, highest scores, or available drafts.
- Two-device edits reconcile predictably without silent data loss.
- Authentication failure, offline operation, and quota errors are visible and recoverable.
- Existing iPhone layout and all curriculum modules continue to work.
- Automated emulator integration tests verify rules, migrations, and conflict handling.
