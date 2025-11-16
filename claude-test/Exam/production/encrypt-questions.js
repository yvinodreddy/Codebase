// Node.js script to encrypt all questions using CryptoJS
const CryptoJS = require('crypto-js');
const fs = require('fs');
const path = require('path');

// Change to script directory
process.chdir(__dirname);

// Read and evaluate the files
const qdbCode = fs.readFileSync('qdb47f2k.js', 'utf8');
const qsbCode = fs.readFileSync('qsb83m9p.js', 'utf8');

// Create a context to eval the code
const context = { CryptoJS };
const evalInContext = (code) => {
    return function() { return eval(code); }.call(context);
};

evalInContext(qdbCode);
evalInContext(qsbCode);

// Extract from context
const QUESTION_DATABASE = context.QUESTION_DATABASE;
const PYTHON_SUBJECTIVE = context.PYTHON_SUBJECTIVE;
const SQL_SUBJECTIVE = context.SQL_SUBJECTIVE;

// Merge subjective questions
QUESTION_DATABASE.pythonSubjective = PYTHON_SUBJECTIVE;
QUESTION_DATABASE.sqlSubjective = SQL_SUBJECTIVE;

// Encryption configuration
const ENCRYPTION_KEY = 'ExamSecure2025!@#$%';

// Combine all questions
const allQuestions = [
    ...QUESTION_DATABASE.pythonMCQ,
    ...QUESTION_DATABASE.sqlMCQ,
    ...QUESTION_DATABASE.pythonSubjective,
    ...QUESTION_DATABASE.sqlSubjective
];

console.log(`Total questions to encrypt: ${allQuestions.length}`);

// Encrypt each question
const encryptedQuestions = allQuestions.map((q, idx) => {
    const jsonString = JSON.stringify(q);
    const encrypted = CryptoJS.AES.encrypt(jsonString, ENCRYPTION_KEY).toString();

    if ((idx + 1) % 20 === 0) {
        console.log(`Encrypted ${idx + 1}/${allQuestions.length} questions...`);
    }

    return encrypted;
});

console.log(`\nSuccessfully encrypted ${encryptedQuestions.length} questions!`);

// Generate JavaScript array for inline inclusion
const outputData = {
    mcq: encryptedQuestions.slice(0, 100),  // First 100 are MCQ (50 Python + 50 SQL)
    sub: encryptedQuestions.slice(100)      // Rest are subjective (30 Python + 30 SQL)
};

// Write to output file
fs.writeFileSync('encrypted-data.json', JSON.stringify(outputData, null, 2));
console.log('\nEncrypted data written to: encrypted-data.json');

// Generate inline JavaScript code
const inlineCode = `const ENC_DATA = ${JSON.stringify(outputData)};`;
fs.writeFileSync('inline-encrypted.js', inlineCode);
console.log('Inline JavaScript written to: inline-encrypted.js');
