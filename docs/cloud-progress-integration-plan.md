# Ethical Hacking Academy — cloud progress follow-up
Verified: `auth.js` signs users in to the shared `academy-cloud-4132c` Firebase Authentication project.
Verified: its login UI currently says coursework saves on this device; the application has multiple localStorage progress keys.
Firestore screenshots show `users/{uid}/academies/business` and `law`, but no `ethical-hacking` document in that user's collection. **Do not infer an error from the missing document**: signing in does not create an academy progress document unless the app writes one.

Remaining:
1. Confirm published Firestore security rules allow a user-only `users/{uid}/academies/ethical-hacking/snapshots/progress-v1` document, or update rules securely.
2. Back up all `ethical-hacking-*` localStorage keys before migration.
3. Add explicit first-device link/restore and autosave with revision conflict handling; ensure all lesson, challenge, assignment and exam write paths trigger save.
4. Test the two-device restore with the same verified Firebase student account; independently test user isolation.
Do not claim cloud progress sync is live from authentication alone.
