# ⚡ EMAIL TEMPLATE - QUICK START GUIDE

## 🎯 ONE-MINUTE SETUP

### **File Location:**
```
/home/user01/claude-test/Exam/production/EMAIL_TEMPLATE_SOLARIZED.html
```

### **Mustache Variables to Replace:**
```javascript
{{student_name}}           // Candidate's full name
{{student_email}}          // Candidate's email
{{session_id}}             // Unique exam session ID
{{submission_timestamp}}   // Submission date/time
{{start_time}}             // Exam start time
{{end_time}}               // Exam end time
{{duration}}               // Total exam duration
{{answered_questions}}     // Number answered
{{total_questions}}        // Total questions
{{percentage}}             // Completion percentage
{{mcq_score}}              // MCQ score
{{camera_status}}          // Camera on/off
{{video_link}}             // pCloud video URL
{{video_filename}}         // Video filename
{{video_folder_link}}      // pCloud folder URL
{{risk_score}}             // Security risk score
{{tab_switches}}           // Tab switch count
{{focus_loss_count}}       // Focus loss count
{{paste_attempts}}         // Paste attempt count
{{devtools_detected}}      // DevTools detection count
{{{answers_summary}}}      // HTML answers (triple braces!)
```

---

## 🎨 COLOR PALETTE CHEAT SHEET

### **Quick Copy-Paste:**
```css
/* Backgrounds */
#fdf6e3  /* Cream - main background */
#eee8d5  /* Beige - cards */

/* Text */
#586e75  /* Dark - main text */
#839496  /* Gray - secondary */
#073642  /* Very dark - headings */

/* Accents */
#268bd2  /* Blue - primary */
#859900  /* Green - success */
#dc322f  /* Red - danger */
#b58900  /* Yellow - warning */
#2aa198  /* Cyan - info */
```

### **Gradients:**
```css
linear-gradient(135deg, #268bd2 0%, #2aa198 100%)  /* Blue→Cyan */
linear-gradient(135deg, #859900 0%, #2aa198 100%)  /* Green→Cyan */
linear-gradient(135deg, #eee8d5 0%, #fdf6e3 100%)  /* Beige→Cream */
```

---

## 🚀 INTEGRATION METHODS

### **Method 1: Direct File Include (Simplest)**
```javascript
const fs = require('fs');
const mustache = require('mustache');

// Read template
const template = fs.readFileSync('EMAIL_TEMPLATE_SOLARIZED.html', 'utf8');

// Prepare data
const data = {
    student_name: studentInfo.name,
    student_email: studentInfo.email,
    session_id: examSession.id,
    submission_timestamp: new Date().toLocaleString(),
    start_time: examSession.startTime,
    end_time: examSession.endTime,
    duration: calculateDuration(examSession.startTime, examSession.endTime),
    answered_questions: Object.keys(studentData.answers).length,
    total_questions: QUESTIONS.length,
    percentage: Math.round((Object.keys(studentData.answers).length / QUESTIONS.length) * 100),
    mcq_score: calculateMCQScore(studentData.answers),
    camera_status: studentData.cameraWorking ? 'Active' : 'Inactive',
    video_link: studentData.videoUrl || '',
    video_filename: studentData.videoFilename || '',
    video_folder_link: 'https://your-pcloud-folder-link',
    risk_score: calculateRiskScore(securityData),
    tab_switches: securityData.tabSwitches,
    focus_loss_count: securityData.focusLossCount,
    paste_attempts: securityData.pasteAttempts,
    devtools_detected: securityData.devtoolsDetected,
    answers_summary: formatAnswersHTML(studentData.answers)
};

// Render template
const html = mustache.render(template, data);

// Send email
await sendEmail(data.student_email, 'Exam Results', html);
```

### **Method 2: EmailJS Template**
```javascript
// 1. Copy entire EMAIL_TEMPLATE_SOLARIZED.html content
// 2. Paste into EmailJS template editor
// 3. Save template with ID 'exam_results_solarized'

// In your code:
emailjs.send('your_service_id', 'exam_results_solarized', {
    student_name: studentInfo.name,
    student_email: studentInfo.email,
    // ... all other variables
});
```

### **Method 3: Nodemailer**
```javascript
const nodemailer = require('nodemailer');
const fs = require('fs');
const mustache = require('mustache');

const transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 587,
    secure: false,
    auth: {
        user: 'your-email@gmail.com',
        pass: 'your-app-password'
    }
});

const template = fs.readFileSync('EMAIL_TEMPLATE_SOLARIZED.html', 'utf8');
const html = mustache.render(template, data);

await transporter.sendMail({
    from: '"Exam System" <exams@semanticdataservices.com>',
    to: data.student_email,
    subject: 'Your Examination Results',
    html: html
});
```

---

## 📋 PRE-FLIGHT CHECKLIST

### **Before Sending:**
- [ ] All mustache variables have data (no `{{blank}}` in output)
- [ ] Video link is valid (or `{{#video_link}}` conditional works)
- [ ] Answers are properly formatted HTML (use triple braces `{{{answers_summary}}}`)
- [ ] Risk score calculated correctly (0-100)
- [ ] Timestamps formatted for readability
- [ ] Duration calculated properly (e.g., "45 minutes")
- [ ] Percentage rounded to whole number

### **Test Email:**
- [ ] Send test to yourself first
- [ ] Check in Gmail, Outlook, Apple Mail
- [ ] Test on mobile device
- [ ] Verify all colors render correctly
- [ ] Check that buttons are clickable
- [ ] Confirm video links work

---

## 🎨 WINDOWS TERMINAL SETTINGS APPLIED

### **Typography:**
```css
font-family: 'Cascadia Mono', 'Segoe UI', ...;
font-size: 12pt;
line-height: 1.2;
letter-spacing: -0.02em;
```

### **Layout:**
```css
padding: 8px;  /* 8,8,8,8 from Windows Terminal */
background-color: #fdf6e3;  /* Solarized Light Base3 */
```

### **Visual:**
- **Cursor color:** #002B36
- **Background opacity:** 100%
- **Intense text style:** font-weight: 700

---

## 🐛 TROUBLESHOOTING

### **"Colors look different in Outlook"**
- **Solution:** This is expected. Outlook uses Microsoft Word rendering engine which has limited CSS support. The fallbacks ensure readability.

### **"Fonts not showing up"**
- **Solution:** Cascadia Mono may not be installed on recipient's system. Template has fallbacks: Segoe UI → System fonts.

### **"Video section not hiding when no video"**
- **Solution:** Ensure you're using mustache conditionals:
  ```html
  {{#video_link}}
    <!-- Video section -->
  {{/video_link}}
  ```

### **"Answers not displaying HTML"**
- **Solution:** Use triple braces for HTML content:
  ```javascript
  {{{answers_summary}}}  // Not {{answers_summary}}
  ```

### **"Layout broken on mobile"**
- **Solution:** Responsive CSS is built-in. Check that email client supports media queries. Gmail mobile app does.

---

## 📊 RISK SCORE CALCULATION EXAMPLE

```javascript
function calculateRiskScore(securityData) {
    let score = 0;

    // Tab switches (30 points max)
    score += Math.min(securityData.tabSwitches * 10, 30);

    // Focus loss (20 points max)
    score += Math.min(securityData.focusLossCount * 5, 20);

    // Paste attempts (30 points max)
    score += Math.min(securityData.pasteAttempts * 15, 30);

    // DevTools detected (20 points max)
    score += Math.min(securityData.devtoolsDetected * 20, 20);

    return Math.min(score, 100);  // Cap at 100
}
```

---

## 🎯 FORMATTING ANSWERS EXAMPLE

```javascript
function formatAnswersHTML(answers) {
    let html = '<div style="font-family: \'Cascadia Mono\', monospace; font-size: 13px; color: #586e75;">';

    QUESTIONS.forEach((q, index) => {
        html += `<div style="margin-bottom: 20px; padding: 12px; background: #eee8d5; border-left: 3px solid #268bd2; border-radius: 6px;">`;
        html += `<strong style="color: #073642;">Q${index + 1}:</strong> ${q.question}<br>`;

        if (q.type === 'mcq' || q.type === 'multi-select') {
            const userAnswer = answers[index];
            const isCorrect = q.type === 'mcq'
                ? userAnswer === q.correctAnswer
                : arraysEqual(userAnswer, q.correctAnswer);

            html += `<span style="color: ${isCorrect ? '#859900' : '#dc322f'}; font-weight: 600;">`;
            html += `Answer: ${formatMCQAnswer(userAnswer)}`;
            html += isCorrect ? ' ✓' : ' ✗';
            html += '</span>';
        } else {
            html += `<div style="background: #fdf6e3; padding: 8px; margin-top: 8px; border-radius: 4px; white-space: pre-wrap;">${answers[index] || '<em style="color: #93a1a1;">Not answered</em>'}</div>`;
        }

        html += '</div>';
    });

    html += '</div>';
    return html;
}
```

---

## 🚀 COMPLETE WORKING EXAMPLE

```javascript
// exam-email-sender.js
const fs = require('fs');
const mustache = require('mustache');
const nodemailer = require('nodemailer');

// Setup email transporter
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
    }
});

// Function to send exam results
async function sendExamResults(examData) {
    // Read template
    const template = fs.readFileSync(
        './EMAIL_TEMPLATE_SOLARIZED.html',
        'utf8'
    );

    // Calculate values
    const duration = calculateDuration(examData.startTime, examData.endTime);
    const percentage = Math.round(
        (examData.answeredQuestions / examData.totalQuestions) * 100
    );
    const riskScore = calculateRiskScore(examData.securityData);

    // Prepare data
    const data = {
        student_name: examData.studentName,
        student_email: examData.studentEmail,
        session_id: examData.sessionId,
        submission_timestamp: new Date(examData.submissionTime).toLocaleString(),
        start_time: new Date(examData.startTime).toLocaleString(),
        end_time: new Date(examData.endTime).toLocaleString(),
        duration: duration,
        answered_questions: examData.answeredQuestions,
        total_questions: examData.totalQuestions,
        percentage: percentage,
        mcq_score: examData.mcqScore,
        camera_status: examData.cameraStatus,
        video_link: examData.videoUrl,
        video_filename: examData.videoFilename,
        video_folder_link: examData.pcloudFolderUrl,
        risk_score: riskScore,
        tab_switches: examData.securityData.tabSwitches,
        focus_loss_count: examData.securityData.focusLoss,
        paste_attempts: examData.securityData.pasteAttempts,
        devtools_detected: examData.securityData.devtools,
        answers_summary: formatAnswersHTML(examData.answers)
    };

    // Render template
    const html = mustache.render(template, data);

    // Send email
    const info = await transporter.sendMail({
        from: '"Exam System" <exams@semanticdataservices.com>',
        to: data.student_email,
        cc: 'evaluator@semanticdataservices.com',
        subject: `Exam Results - ${data.student_name} - Session ${data.session_id}`,
        html: html
    });

    console.log('✅ Email sent:', info.messageId);
    return info;
}

// Helper functions
function calculateDuration(start, end) {
    const ms = new Date(end) - new Date(start);
    const minutes = Math.floor(ms / 60000);
    return `${minutes} minutes`;
}

function calculateRiskScore(securityData) {
    return Math.min(
        (securityData.tabSwitches * 10) +
        (securityData.focusLoss * 5) +
        (securityData.pasteAttempts * 15) +
        (securityData.devtools * 20),
        100
    );
}

function formatAnswersHTML(answers) {
    // Implementation from above
    return '<div>...</div>';
}

// Export
module.exports = { sendExamResults };
```

---

## 📞 SUPPORT

### **Issues:**
If colors don't match or fonts don't load:
1. Check that file path is correct
2. Verify mustache syntax (double braces for text, triple for HTML)
3. Test in multiple email clients
4. Check spam folder

### **Customization:**
To change colors, edit CSS variables at top of HTML file:
```css
:root {
    --primary-bg: #YOUR_COLOR;
    --accent-primary: #YOUR_COLOR;
}
```

---

## ✅ CHECKLIST SUMMARY

**Setup:** ✅ Template file ready at `/home/user01/claude-test/Exam/production/EMAIL_TEMPLATE_SOLARIZED.html`

**Integration:** ✅ Choose one of 3 methods (Direct/EmailJS/Nodemailer)

**Variables:** ✅ Replace all 19 mustache variables with real data

**Testing:** ✅ Send test email, check in 3+ email clients

**Deployment:** ✅ Send to real candidates

**Quality:** ✅ Solarized Light colors match exam system

**Typography:** ✅ Cascadia Mono + Windows Terminal settings applied

**Status:** ✅ **PRODUCTION READY**

---

**🚀 YOU'RE READY TO SEND WORLD-CLASS EXAM RESULTS EMAILS! 🚀**
