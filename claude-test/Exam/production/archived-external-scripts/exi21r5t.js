// ==================== EXAM INTEGRATION WITH ENCRYPTED QUESTIONS ====================
// This file integrates the question database with the main exam system
// Handles randomization, encryption, and progressive decryption

// ==================== CONFIGURATION ====================
const EXAM_CONFIG = {
    totalQuestions: 15,
    objectiveCount: 10,
    subjectiveCount: 5,
    encryptionKey: 'ExamSecure2025!@#$%'
};

// ==================== QUESTION SELECTION ENGINE ====================
class ExamQuestionManager {
    constructor() {
        this.selectedQuestions = [];
        this.encryptedQuestions = [];
        this.currentQuestionIndex = 0;
        this.decryptedQuestions = new Map(); // Cache for already decrypted questions
    }

    /**
     * Initialize exam with random question selection
     */
    initializeExam() {
        console.log('🎯 Initializing exam with random question selection...');

        // Combine all objective questions (Python MCQ + SQL MCQ)
        const allObjective = [
            ...QUESTION_DATABASE.pythonMCQ,
            ...QUESTION_DATABASE.sqlMCQ
        ];
        console.log(`📊 Total objective questions available: ${allObjective.length}`);

        // Combine all subjective questions (Python + SQL)
        const allSubjective = [
            ...QUESTION_DATABASE.pythonSubjective,
            ...QUESTION_DATABASE.sqlSubjective
        ];
        console.log(`📊 Total subjective questions available: ${allSubjective.length}`);

        // Randomly select questions
        const selectedObjective = this.shuffleAndSelect(allObjective, EXAM_CONFIG.objectiveCount);
        const selectedSubjective = this.shuffleAndSelect(allSubjective, EXAM_CONFIG.subjectiveCount);

        // Combine selected questions
        this.selectedQuestions = [...selectedObjective, ...selectedSubjective];

        console.log(`✅ Selected ${this.selectedQuestions.length} questions for this exam`);
        console.log(`   - ${selectedObjective.length} objective questions`);
        console.log(`   - ${selectedSubjective.length} subjective questions`);

        // Encrypt all selected questions
        this.encryptAllQuestions();

        return this.encryptedQuestions.length;
    }

    /**
     * Fisher-Yates shuffle and select N random items
     */
    shuffleAndSelect(array, count) {
        const shuffled = [...array]; // Create copy

        // Fisher-Yates shuffle
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }

        // Select first N items
        return shuffled.slice(0, count);
    }

    /**
     * Encrypt all selected questions
     */
    encryptAllQuestions() {
        console.log('🔐 Encrypting all selected questions...');

        this.encryptedQuestions = this.selectedQuestions.map((question, index) => {
            const encrypted = CryptoJS.AES.encrypt(
                JSON.stringify(question),
                EXAM_CONFIG.encryptionKey
            ).toString();

            return {
                index: index,
                id: question.id,
                type: question.type,
                category: question.category,
                points: question.points,
                encrypted: encrypted,
                isDecrypted: false
            };
        });

        console.log(`✅ Successfully encrypted ${this.encryptedQuestions.length} questions`);
    }

    /**
     * Decrypt a single question (progressive decryption)
     * Only decrypt when user navigates to that question
     */
    decryptQuestion(index) {
        // Check if already decrypted in cache
        if (this.decryptedQuestions.has(index)) {
            console.log(`⚡ Using cached decrypted question ${index + 1}`);
            return this.decryptedQuestions.get(index);
        }

        console.log(`🔓 Decrypting question ${index + 1}...`);

        const encryptedQuestion = this.encryptedQuestions[index];
        if (!encryptedQuestion) {
            console.error(`❌ Question ${index + 1} not found`);
            return null;
        }

        try {
            const decrypted = CryptoJS.AES.decrypt(
                encryptedQuestion.encrypted,
                EXAM_CONFIG.encryptionKey
            );

            const questionData = JSON.parse(decrypted.toString(CryptoJS.enc.Utf8));

            // Cache the decrypted question
            this.decryptedQuestions.set(index, questionData);

            console.log(`✅ Successfully decrypted question ${index + 1}`);
            return questionData;

        } catch (error) {
            console.error(`❌ Error decrypting question ${index + 1}:`, error);
            return null;
        }
    }

    /**
     * Get current question (decrypted)
     */
    getCurrentQuestion() {
        return this.decryptQuestion(this.currentQuestionIndex);
    }

    /**
     * Navigate to next question
     */
    nextQuestion() {
        if (this.currentQuestionIndex < this.selectedQuestions.length - 1) {
            this.currentQuestionIndex++;
            return this.getCurrentQuestion();
        }
        return null;
    }

    /**
     * Navigate to previous question
     */
    previousQuestion() {
        if (this.currentQuestionIndex > 0) {
            this.currentQuestionIndex--;
            return this.getCurrentQuestion();
        }
        return null;
    }

    /**
     * Navigate to specific question
     */
    goToQuestion(index) {
        if (index >= 0 && index < this.selectedQuestions.length) {
            this.currentQuestionIndex = index;
            return this.getCurrentQuestion();
        }
        return null;
    }

    /**
     * Get question metadata without decryption (for navigation grid)
     */
    getQuestionMetadata() {
        return this.encryptedQuestions.map(q => ({
            id: q.id,
            type: q.type,
            category: q.category,
            points: q.points,
            index: q.index
        }));
    }

    /**
     * Get exam statistics
     */
    getStats() {
        return {
            total: this.selectedQuestions.length,
            current: this.currentQuestionIndex + 1,
            objective: this.selectedQuestions.filter(q => q.type === 'mcq').length,
            subjective: this.selectedQuestions.filter(q => q.type === 'coding').length,
            pythonQuestions: this.selectedQuestions.filter(q => q.category === 'python').length,
            sqlQuestions: this.selectedQuestions.filter(q => q.category === 'sql').length
        };
    }

    /**
     * Verify no questions repeat (for testing)
     */
    verifyNoDuplicates() {
        const ids = this.selectedQuestions.map(q => q.id);
        const uniqueIds = new Set(ids);

        if (ids.length === uniqueIds.size) {
            console.log('✅ VERIFIED: No duplicate questions in exam');
            return true;
        } else {
            console.error('❌ ERROR: Duplicate questions detected!');
            console.error('Total questions:', ids.length);
            console.error('Unique questions:', uniqueIds.size);
            return false;
        }
    }

    /**
     * Security check - ensure questions are encrypted in DOM
     */
    verifyEncryption() {
        console.log('🔐 Verifying encryption security...');

        // Check that encrypted questions don't contain readable text
        for (let i = 0; i < this.encryptedQuestions.length; i++) {
            const encrypted = this.encryptedQuestions[i].encrypted;

            // Encrypted text should not contain common question keywords
            const suspiciousKeywords = ['print', 'SELECT', 'def', 'function', 'SQL', 'Python'];
            const containsReadableText = suspiciousKeywords.some(keyword =>
                encrypted.includes(keyword)
            );

            if (containsReadableText) {
                console.warn(`⚠️ Question ${i + 1} may not be properly encrypted`);
                return false;
            }
        }

        console.log('✅ All questions properly encrypted');
        return true;
    }
}

// ==================== INITIALIZATION ====================
function initializeExamSystem() {
    console.log('🚀 Initializing Exam System...');
    console.log('═'.repeat(60));

    // Create exam manager instance
    examManager = new ExamQuestionManager();

    // Initialize with random questions
    const totalQuestions = examManager.initializeExam();

    // Verify no duplicates
    examManager.verifyNoDuplicates();

    // Verify encryption
    examManager.verifyEncryption();

    // Get statistics
    const stats = examManager.getStats();
    console.log('═'.repeat(60));
    console.log('📊 EXAM STATISTICS:');
    console.log(`   Total Questions: ${stats.total}`);
    console.log(`   Objective (MCQ): ${stats.objective}`);
    console.log(`   Subjective (Coding): ${stats.subjective}`);
    console.log(`   Python Questions: ${stats.pythonQuestions}`);
    console.log(`   SQL Questions: ${stats.sqlQuestions}`);
    console.log('═'.repeat(60));
    console.log('✅ Exam System Ready!');

    return examManager;
}

// ==================== HELPER FUNCTIONS ====================

/**
 * Render question HTML based on type
 */
function renderQuestion(questionData, questionNumber) {
    if (!questionData) return '';

    const isObjective = questionData.type === 'mcq';

    if (isObjective) {
        return renderObjectiveQuestion(questionData, questionNumber);
    } else {
        return renderSubjectiveQuestion(questionData, questionNumber);
    }
}

/**
 * Render objective (MCQ) question
 */
function renderObjectiveQuestion(question, questionNumber) {
    const optionsHTML = question.options.map((option, index) => {
        const optionLetter = String.fromCharCode(65 + index); // A, B, C, D
        return `
            <div class="option-item" data-option="${index}">
                <input type="radio"
                       id="q${questionNumber}_opt${index}"
                       name="q${questionNumber}"
                       value="${index}">
                <label for="q${questionNumber}_opt${index}">
                    <span class="option-letter">${optionLetter}</span>
                    <span class="option-text">${option}</span>
                </label>
            </div>
        `;
    }).join('');

    return `
        <div class="question-content">
            <div class="question-header">
                <span class="question-number">Question ${questionNumber}</span>
                <span class="question-type-badge ${question.category}">${question.category.toUpperCase()} MCQ</span>
                <span class="points-badge">${question.points} points</span>
            </div>
            <div class="question-text">${question.question.replace(/\n/g, '<br>')}</div>
            <div class="options-container">
                ${optionsHTML}
            </div>
        </div>
    `;
}

/**
 * Render subjective (coding) question
 */
function renderSubjectiveQuestion(question, questionNumber) {
    return `
        <div class="question-content">
            <div class="question-header">
                <span class="question-number">Question ${questionNumber}</span>
                <span class="question-type-badge coding ${question.category}">${question.category.toUpperCase()} CODING</span>
                <span class="points-badge">${question.points} points</span>
            </div>
            <div class="question-text">${question.question.replace(/\n/g, '<br>')}</div>
            <div class="code-editor-container">
                <textarea class="code-editor"
                          id="q${questionNumber}_code"
                          placeholder="Write your solution here..."
                          spellcheck="false">${question.starterCode || ''}</textarea>
            </div>
            ${question.explanation ? `<div class="hint-text">💡 Hint: ${question.explanation}</div>` : ''}
        </div>
    `;
}

// ==================== EXPORT FOR USE ====================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ExamQuestionManager,
        initializeExamSystem,
        renderQuestion,
        EXAM_CONFIG
    };
}
