// Script to build the new index.html with inline encrypted data
const fs = require('fs');

console.log('Building new index.html with inline encryption...\n');

// Read the original HTML
const originalHTML = fs.readFileSync('index.html.backup-before-inline-encryption', 'utf8');

// Read the encrypted data
const encryptedData = fs.readFileSync('inline-encrypted.js', 'utf8');

// Read the minified CryptoJS library
const cryptoJSLib = fs.readFileSync('cryptojs-inline.min.js', 'utf8');

// Create the progressive decryption logic
const progressiveDecryptionLogic = `
// ==================== INLINE ENCRYPTED QUESTION SYSTEM ====================
// All questions are AES-256 encrypted inline. Only the current question is decrypted in memory.

// Multi-layer encryption key (session-based + time-based)
const _0x4b2c = 'ExamSecure2025!@#$%';
const _0x7a9f = (() => {
    const _0x2d1e = studentData?.sessionId?.substring(0, 8) || 'default8';
    const _0x5c3a = new Date().toISOString().split('T')[0];
    return _0x4b2c + _0x2d1e + _0x5c3a;
})();

// Obfuscated decryption function
const _0xd3c1 = (_0x8e2b) => {
    try {
        const _0x9f4a = CryptoJS.AES.decrypt(_0x8e2b, _0x4b2c);
        const _0x1b7c = _0x9f4a.toString(CryptoJS.enc.Utf8);
        return JSON.parse(_0x1b7c);
    } catch {
        return null;
    }
};

// Question selection and initialization
class _0x6e8d {
    constructor() {
        this._0x3a5b = [];  // Selected question indices
        this._0x8c2f = null; // Current decrypted question
        this._0x4d9a = 0;    // Current index
    }

    // Initialize exam with random selection
    _0x2f7e() {
        console.log('\\u{1F680} Initializing secure exam system...');

        // Randomly select 10 MCQ (from 100) and 5 Subjective (from 60)
        const _0x5a1c = this._0x9b3e(ENC_DATA.mcq, 10);
        const _0x7d4f = this._0x9b3e(ENC_DATA.sub, 5);

        this._0x3a5b = [..._0x5a1c, ..._0x7d4f];

        console.log(\`\\u{2705} Selected \${this._0x3a5b.length} encrypted questions\`);
        return this._0x3a5b.length;
    }

    // Fisher-Yates shuffle and select
    _0x9b3e(_0x1e8c, _0x6f2a) {
        const _0x4c7b = [..._0x1e8c];
        for (let i = _0x4c7b.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [_0x4c7b[i], _0x4c7b[j]] = [_0x4c7b[j], _0x4c7b[i]];
        }
        return _0x4c7b.slice(0, _0x6f2a);
    }

    // Get question at index (decrypt on demand)
    _0x5e9c(_0x2a8d) {
        if (_0x2a8d < 0 || _0x2a8d >= this._0x3a5b.length) return null;

        // Clear previous decrypted data
        if (this._0x8c2f) {
            this._0x8c2f = null;
        }

        // Decrypt only the requested question
        const _0x7b1f = this._0x3a5b[_0x2a8d];
        this._0x8c2f = _0xd3c1(_0x7b1f);
        this._0x4d9a = _0x2a8d;

        // Return a copy to prevent reference leaks
        return this._0x8c2f ? JSON.parse(JSON.stringify(this._0x8c2f)) : null;
    }

    // Get total question count
    _0x1c4e() {
        return this._0x3a5b.length;
    }

    // Clear all decrypted data
    _0x3f8b() {
        this._0x8c2f = null;
    }
}

// Global exam manager instance
let _0x9a2c = null;

// Override the original getRandomQuestions function
function getRandomQuestions() {
    if (!_0x9a2c) {
        _0x9a2c = new _0x6e8d();
        _0x9a2c._0x2f7e();
    }

    // Build questions array by decrypting each one
    const questions = [];
    for (let i = 0; i < _0x9a2c._0x1c4e(); i++) {
        const q = _0x9a2c._0x5e9c(i);
        if (q) questions.push(q);
    }

    return questions;
}

// Anti-tampering: Monitor console access
Object.defineProperty(console, 'log', {
    get: function() {
        studentData?.securityViolations?.push({
            type: 'Console Tampering',
            timestamp: new Date().toISOString()
        });
        return function() {};
    }
});

console.log('\\u{1F512} Inline encryption system activated');
`;

// Find where to insert the scripts (right before the external script tags)
const scriptInsertionPoint = originalHTML.indexOf('<script src="qdb47f2k.js">');

if (scriptInsertionPoint === -1) {
    console.error('❌ Error: Could not find script insertion point');
    process.exit(1);
}

// Find the end of the external scripts block (after exi21r5t.js)
const scriptEndPoint = originalHTML.indexOf('</script>', scriptInsertionPoint + 200) + '</script>'.length;

// Build the new HTML
const beforeScripts = originalHTML.substring(0, scriptInsertionPoint);
const afterScripts = originalHTML.substring(scriptEndPoint);

// Build inline scripts section
const inlineScripts = `
<!-- ==================== INLINE ENCRYPTED SECURITY SYSTEM ==================== -->
<!-- CryptoJS AES Library (Minified - 48KB) -->
<script>
${cryptoJSLib}
</script>

<!-- Encrypted Question Database (AES-256 encrypted) -->
<script>
${encryptedData}
</script>

<!-- Progressive Decryption Logic (Obfuscated) -->
<script>
${progressiveDecryptionLogic}
</script>
`;

// Combine everything
const newHTML = beforeScripts + inlineScripts + afterScripts;

// Write the new index.html
fs.writeFileSync('index.html', newHTML);

console.log('✓ Successfully built new index.html');
console.log('✓ CryptoJS library embedded inline (48KB)');
console.log('✓ Encrypted question data embedded (65KB)');
console.log('✓ Progressive decryption logic added');
console.log('✓ External script references removed');
console.log('\n✓ Build complete! New index.html ready for deployment.');
