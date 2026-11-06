# Three-Academy Cross-Device Saving

This repository is the new public home for Ethical Hacking Academy. **No live app or Firebase project is configured here yet.** No student data belongs in GitHub.

## Intended system
- One Firebase Authentication project for all three apps.
- Per-student progress in Firestore paths `users/{uid}/academies/{academyId}/snapshots/{snapshotId}`.
- Allowed academy IDs: `business`, `law`, `ethical-hacking`.
- Two students can sign in separately to Ethical Hacking Academy. Only the owner's account will be granted enrollment in Business and Law Academy when an enrollment authorization mechanism is implemented.
- User-specific Firestore rules are included in `firebase/firestore.rules`; they separate data by UID. **They do not yet enforce academy enrollment.** Do not deploy publicly until enrollment rules and security tests are implemented.
- Existing Business and Law Academy local progress must be backed up and deliberately imported before any remote restore is attempted.
- Two-device tests must include iPhone Safari and standalone Home Screen web app.

## Required before launch
1. Create/configure the Firebase project, enable Email/Password sign-in and register the academy domains.
2. Implement enrollment restrictions for the two private-to-owner academies using trusted backend claims or server-controlled membership records. UI-only restrictions are not security.
3. Add Firestore security rules and write emulator tests verifying no cross-user and no unauthorized-academy access.
4. Connect each academy to its same account with an explicit first-import operation, then autosave and offline retry.
5. Protect conflict cases: never silently replace existing progress. Preserve a downloadable local backup.
6. Test large snapshots, authentication errors, PWA storage and second-device refresh.
7. Do not commit account passwords, service-account keys, or saved coursework to public GitHub.

Existing draft PRs:
- [Business Academy progress sync](https://github.com/gcfd8hy5mb-ai/business-academy/pull/1)
- [Law Academy progress sync](https://github.com/gcfd8hy5mb-ai/law-academy/pull/1)
