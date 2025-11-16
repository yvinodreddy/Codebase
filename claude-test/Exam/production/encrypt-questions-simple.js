// Simple Node.js script to encrypt questions
const CryptoJS = require('crypto-js');
const fs = require('fs');

// Read the JS files and extract question data using regex
const qdbContent = fs.readFileSync('qdb47f2k.js', 'utf8');
const qsbContent = fs.readFileSync('qsb83m9p.js', 'utf8');

// Extract the pythonMCQ array
const pythonMCQMatch = qdbContent.match(/pythonMCQ:\s*\[([\s\S]*?)\],\s*\/\/ ====/);
const sqlMCQMatch = qdbContent.match(/sqlMCQ:\s*\[([\s\S]*?)\],\s*\/\/ Due to/);

// Extract subjective arrays
const pythonSubMatch = qsbContent.match(/const PYTHON_SUBJECTIVE = \[([\s\S]*?)\];/);
const sqlSubMatch = qsbContent.match(/const SQL_SUBJECTIVE = \[([\s\S]*?)\];/);

console.log('Parsing question arrays...');

// Create a temporary evaluation scope
const scope = {
    pythonMCQ: null,
    sqlMCQ: null,
    pythonSubjective: null,
    sqlSubjective: null
};

// Execute in eval to parse the JavaScript objects
try {
    eval(`scope.pythonMCQ = [${pythonMCQMatch[1]}];`);
    eval(`scope.sqlMCQ = [${sqlMCQMatch[1]}];`);
    eval(`scope.pythonSubjective = [${pythonSubMatch[1]}];`);
    eval(`scope.sqlSubjective = [${sqlSubMatch[1]}];`);
} catch (e) {
    console.error('Error parsing questions:', e.message);
    process.exit(1);
}

console.log(`Parsed ${scope.pythonMCQ.length} Python MCQ questions`);
console.log(`Parsed ${scope.sqlMCQ.length} SQL MCQ questions`);
console.log(`Parsed ${scope.pythonSubjective.length} Python subjective questions`);
console.log(`Parsed ${scope.sqlSubjective.length} SQL subjective questions`);

// Combine all questions
const allMCQ = [...scope.pythonMCQ, ...scope.sqlMCQ];
const allSubjective = [...scope.pythonSubjective, ...scope.sqlSubjective];

// Encryption key
const ENCRYPTION_KEY = 'ExamSecure2025!@#$%';

console.log('\nEncrypting questions...');

// Encrypt MCQ questions
const encryptedMCQ = allMCQ.map((q, idx) => {
    const encrypted = CryptoJS.AES.encrypt(JSON.stringify(q), ENCRYPTION_KEY).toString();
    if ((idx + 1) % 20 === 0) {
        console.log(`  Encrypted ${idx + 1}/${allMCQ.length} MCQ questions...`);
    }
    return encrypted;
});

// Encrypt subjective questions
const encryptedSubjective = allSubjective.map((q, idx) => {
    const encrypted = CryptoJS.AES.encrypt(JSON.stringify(q), ENCRYPTION_KEY).toString();
    if ((idx + 1) % 10 === 0) {
        console.log(`  Encrypted ${idx + 1}/${allSubjective.length} subjective questions...`);
    }
    return encrypted;
});

console.log(`\n✓ Successfully encrypted ${encryptedMCQ.length} MCQ questions`);
console.log(`✓ Successfully encrypted ${encryptedSubjective.length} subjective questions`);

// Create the output structure
const outputData = {
    mcq: encryptedMCQ,
    sub: encryptedSubjective
};

// Write to JSON file
fs.writeFileSync('encrypted-data.json', JSON.stringify(outputData, null, 2));
console.log('\n✓ Encrypted data written to: encrypted-data.json');

// Generate inline JavaScript code (compact format for HTML)
const inlineCode = `const ENC_DATA=${JSON.stringify(outputData)};`;
fs.writeFileSync('inline-encrypted.js', inlineCode);
console.log('✓ Inline JavaScript written to: inline-encrypted.js');

console.log('\n✓ Encryption complete!');
