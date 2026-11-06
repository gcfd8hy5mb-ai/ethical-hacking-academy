# Ethical Hacking Academy

This project is being prepared as a 350-hour ethical hacking education app. The secure student-saving foundation is developed separately from the live app.

## Learner accounts
- One Firebase Authentication project is shared with Business and Law Academy.
- Each authenticated student gets a unique UID and personal cloud records.
- The owner's account can be granted all three academy enrollments.
- The invited second student gets Ethical Hacking enrollment only.
- Enrollment must be assigned by trusted administrator code, never from the browser.

## Progress model
Store per-user academy progress using small documents, rather than one enormous record:
`users/{uid}/academies/ethical-hacking/snapshots/{storageKey}`

Each record has: `raw` JSON string, `schemaVersion:1`, `updatedAt` server timestamp, `academy:'ethical-hacking'`.

Suggested logical keys:
- `ethical-hacking-progress-v1`
- `ethical-hacking-exam-results-v1`
- `ethical-hacking-lab-results-v1`
- `ethical-hacking-notes-v1`

This is a draft data contract, not a working learning app. Save on device first, explicitly import first-device work, then enable cloud autosave after successful conflict checks. Do not use GitHub to store private student data.

## Release blockers
- Firestore rule emulator tests for owner, invited student, unknown student and anonymous access.
- Confirm rules were actually published to Firebase.
- Safe account enrollment flow and verified email.
- Two-device sync and conflict recovery tests.
- Test compatibility with iPhone Safari and Home Screen PWA.
