/**
 * Quick test for path validation guards
 */

const EMOJI_REGEX = /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{FE00}-\u{FE0F}\u{1F1E0}-\u{1F1FF}]/u;
const WINDOWS_MAX_PATH = 260;

function isValidPath(fullPath, fileName) {
  if (EMOJI_REGEX.test(fileName)) {
    return { valid: false, reason: 'contains emoji characters' };
  }
  if (fullPath.length >= WINDOWS_MAX_PATH) {
    return { valid: false, reason: `path length ${fullPath.length} exceeds Windows limit of ${WINDOWS_MAX_PATH}` };
  }
  return { valid: true };
}

// Test cases
const tests = [
  { name: 'Study 2025 📕.md', path: '/vault/Study 2025 📕.md', shouldFail: true, reason: 'emoji' },
  { name: 'Mind Dump 🧠.md', path: '/vault/Mind Dump 🧠.md', shouldFail: true, reason: 'emoji' },
  { name: 'Regular Note.md', path: '/vault/Regular Note.md', shouldFail: false },
  { name: 'Another Note.md', path: '/vault/' + 'a'.repeat(240) + '.md', shouldFail: true, reason: 'length' },
  { name: 'Normal.md', path: '/vault/', shouldFail: false },
  { name: 'Repomix 📦.md', path: '/vault/Repomix 📦.md', shouldFail: true, reason: 'emoji' },
];

console.log('Running validation tests...\n');

let passed = 0;
let failed = 0;

tests.forEach((test, i) => {
  const result = isValidPath(test.path, test.name);
  const expectedToFail = test.shouldFail;
  const actuallyFailed = !result.valid;

  const success = expectedToFail === actuallyFailed;

  if (success) {
    console.log(`✓ Test ${i + 1}: ${test.name}`);
    if (!result.valid) {
      console.log(`  → Correctly rejected: ${result.reason}`);
    }
    passed++;
  } else {
    console.log(`✗ Test ${i + 1}: ${test.name}`);
    console.log(`  → Expected: ${expectedToFail ? 'reject' : 'accept'}`);
    console.log(`  → Actual: ${actuallyFailed ? 'rejected' : 'accepted'}`);
    if (result.reason) {
      console.log(`  → Reason: ${result.reason}`);
    }
    failed++;
  }
  console.log();
});

console.log(`Results: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
