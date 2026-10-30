# Firebase enrollment and deployment prerequisites

The Firestore rules require a verified email for Ethical Hacking Academy. Business and Law Academy additionally require **trusted, server-issued** Firebase Authentication custom claims such as `{academies: ['business', 'law']}`.

**Never let the browser set enrollment claims.** A trusted server using the Firebase Admin SDK must grant these claims only to the authorized owner UID. Do not put a service account key in public GitHub, browser code or chat.

Steps required before release:
1. Create a Firebase project and register three web apps under it.
2. Enable Email/Password authentication and email verification.
3. Register each academy's hosting domain in Firebase Authentication authorized domains.
4. Provision the owner identity and grant custom claims through a trusted administrative action.
5. Deploy and test Firestore rules against the emulator before allowing students to upload.
6. Implement full storage-key inventories and migration with explicit choices; current draft modules are **manual upload/restore only**, not autosave.
7. On iPhone Safari and PWA, verify the same account and progress work on two different devices.

Current Firestore rules have default-deny behavior for all documents outside the user-owned snapshot paths. For an invited second ethical-hacking student, use an independently verified account.
