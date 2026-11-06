// Run ONLY in a trusted administrator environment with Firebase Admin credentials.
// Usage: node scripts/grant-academy-access.cjs <uid> <owner|student>
// Never run this script in a browser and never commit a service-account private key.
// Set GOOGLE_APPLICATION_CREDENTIALS to a securely stored credential file.
const admin = require('firebase-admin');
const [uid,role] = process.argv.slice(2);
if (!uid || !['owner','student'].includes(role)) {
  console.error('Usage: node scripts/grant-academy-access.cjs <uid> <owner|student>');
  process.exit(2);
}
const academies = role === 'owner'
  ? ['business','law','ethical-hacking']
  : ['ethical-hacking'];
admin.initializeApp({credential:admin.credential.applicationDefault()});
(async()=>{
  const user=await admin.auth().getUser(uid);
  if (!user.emailVerified) throw new Error('Verify email before granting enrollment.');
  const existing=user.customClaims||{};
  await admin.auth().setCustomUserClaims(uid,{...existing,academies});
  console.log('Granted',academies.join(', '),'to UID:',uid);
  console.log('User must sign out and sign in again to refresh claims.');
})().catch(error=>{console.error(error.message);process.exitCode=1});
