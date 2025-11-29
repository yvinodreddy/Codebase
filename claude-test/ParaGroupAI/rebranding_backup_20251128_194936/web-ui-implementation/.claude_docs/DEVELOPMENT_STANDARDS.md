# Development Standards - Para Group Web UI

This document defines development standards for the Para Group Web UI project.

## ⏱️ TIME LIMITS AND EXECUTION CONSTRAINTS

**CRITICAL UNDERSTANDING - NO TIME LIMITS FOR CLAUDE CODE:**

Claude Code operates under a $200/month subscription model with the following constraints:

### ✅ What Claude Code HAS:
- **NO time limits** for completing requests
- **NO artificial deadlines** for implementation
- **UNLIMITED iterations** for refinement and perfection
- **200,000 token context window** per request
- **Full autonomous execution** capability

### ❌ What Claude Code DOES NOT HAVE:
- ❌ **NO time constraints** - Can work on tasks for as long as needed
- ❌ **NO execution timeouts** - Individual commands have timeouts (2-10 min) but can be retried
- ❌ **NO implementation shortcuts** - Every feature must be 100% complete
- ❌ **NO "due to time limitations" excuses** - This phrase is BANNED

### 🎯 Implementation Standards:

When user requests features:

1. **ALWAYS implement to 100% completion**
   - Never cite "time constraints" as reason for incomplete work
   - Never leave features partially implemented
   - Never skip requirements due to perceived complexity

2. **For large tasks, use task decomposition**
   - Break into smaller, manageable subtasks
   - Use TodoWrite tool to track progress
   - Execute subtasks sequentially or in parallel
   - Report completion status after each subtask

3. **For extremely large tasks (100+ subtasks)**
   - Ask user if they want to split into multiple phases
   - Provide clear breakdown of what each phase includes
   - Get user confirmation on phasing approach
   - Execute each phase to 100% completion

4. **Command Timeouts (Technical Limitation)**
   - Individual bash commands: 2-minute default, 10-minute maximum
   - Long-running processes: Run in background with BashOutput monitoring
   - Builds/tests: Use background execution with progress checks
   - These are TECHNICAL constraints, not time constraint excuses

### 📋 Task Decomposition Example:

**BAD (Old Approach):**
```
User: Implement features A, B, C, D, E
Claude: ⚠️ Implemented A and B. Features C, D, E not implemented due to time limitations.
```

**GOOD (Correct Approach):**
```
User: Implement features A, B, C, D, E
Claude: Creating todo list with 5 tasks...
[Task 1/5] Implementing Feature A... ✅ Complete
[Task 2/5] Implementing Feature B... ✅ Complete
[Task 3/5] Implementing Feature C... ✅ Complete
[Task 4/5] Implementing Feature D... ✅ Complete
[Task 5/5] Implementing Feature E... ✅ Complete
All 5 features implemented to 100% completion.
```

### 🚫 BANNED PHRASES:

The following phrases are PERMANENTLY BANNED and must NEVER be used:
- ❌ "Due to time limitations"
- ❌ "Due to time constraints"
- ❌ "Not enough time to implement"
- ❌ "Would require more time"
- ❌ "Time constraints prevented implementation"

### ✅ CORRECT ALTERNATIVES:

Instead, use:
- ✅ "Implementation complete for all requested features"
- ✅ "Breaking down into N subtasks for systematic execution"
- ✅ "This is a large task - would you like me to implement in phases?"
- ✅ "Executing all N features sequentially with progress updates"

### 📝 Documentation Requirement:

This time limit policy must be present in:
- ✅ /home/user01/claude-test/CLAUDE.md - Global rules
- ✅ /home/user01/claude-test/ClaudePrompt/CLAUDE.md - ULTRATHINK project rules
- ✅ /home/user01/claude-test/ClaudePrompt/web-ui-implementation/.claude_docs/DEVELOPMENT_STANDARDS.md (this file)

All three files MUST contain consistent messaging about:
1. NO time limits for Claude Code
2. 100% completion requirement for all features
3. Task decomposition for large requests
4. Banned phrases list
5. Correct alternatives

This is a PERMANENT, NON-NEGOTIABLE standard effective 2025-11-14 and forever.

---

## 🔒 Security Standards

All features in this project must follow OWASP Top 10 security standards:

### Path Exposure Prevention
- ✅ Never expose internal file paths in API responses
- ✅ Use secure file IDs (SHA-256 hashes) instead of paths
- ✅ Never expose paths in error messages (even generic errors)
- ✅ Implement directory traversal prevention
- ✅ User isolation through per-user directories

### Security Headers
- ✅ X-Frame-Options: SAMEORIGIN
- ✅ X-Content-Type-Options: nosniff
- ✅ X-XSS-Protection: 1; mode=block
- ✅ Content-Security-Policy (CSP)
- ✅ Strict-Transport-Security (HSTS in production)
- ✅ Referrer-Policy: strict-origin-when-cross-origin

### Input Validation
- ✅ Sanitize all user inputs
- ✅ Validate file paths before access
- ✅ Check file types and sizes
- ✅ Prevent command injection
- ✅ Prevent SQL injection (if database added)

### CVE Monitoring
- ✅ Weekly automated scans with `scripts/cve-monitor.sh`
- ✅ Fix critical vulnerabilities within 24 hours
- ✅ Fix high vulnerabilities within 7 days
- ✅ Monthly dependency updates
- ✅ Subscribe to GitHub security advisories

---

## 🎨 UI/UX Standards

### Theme Toggle
- ✅ Smooth color transitions (0.3s ease)
- ✅ Graceful theme switching (no jarring changes)
- ✅ Persist theme preference in localStorage
- ✅ Sun/Moon icons for visual clarity
- ✅ Accessible (proper contrast ratios)

### Responsive Design
- ✅ Mobile-first approach
- ✅ Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- ✅ Touch-friendly tap targets (44x44px minimum)
- ✅ Readable font sizes on all devices

### Accessibility
- ✅ WCAG 2.1 Level AA compliance
- ✅ Keyboard navigation support
- ✅ Screen reader friendly
- ✅ Proper ARIA labels
- ✅ Color contrast ratio 4.5:1 minimum

---

## 💻 Code Quality Standards

### TypeScript
- ✅ Strict mode enabled
- ✅ No `any` types (use proper types)
- ✅ Explicit return types for functions
- ✅ Interface-first design

### React
- ✅ Functional components only
- ✅ Custom hooks for reusable logic
- ✅ Proper dependency arrays in useEffect
- ✅ Memoization for expensive computations

### File Organization
```
src/
├── app/              # Next.js 14 App Router pages
├── components/       # Reusable React components
├── contexts/         # React Context providers
├── lib/              # Utility libraries and clients
├── pages/api/        # API routes
└── styles/           # Global styles and CSS
```

### Testing
- ✅ Unit tests for utility functions
- ✅ Integration tests for API routes
- ✅ E2E tests for critical user flows
- ✅ 80%+ code coverage target

---

## 🚀 Deployment Standards

### Pre-Deployment Checklist
- [ ] All tests passing
- [ ] No console errors or warnings
- [ ] Security scan (CVE check) completed
- [ ] Environment variables configured
- [ ] Build successful (`npm run build`)
- [ ] Performance audit (Lighthouse score 90+)

### Production Build
```bash
# Build for production
npm run build

# Start production server
npm run start
```

### Environment Variables
```
NEXTAUTH_URL=https://your-domain.com
NEXTAUTH_SECRET=your-secret-here
NODE_ENV=production
```

---

## 📊 Performance Standards

### Core Web Vitals Targets
- **LCP (Largest Contentful Paint)**: < 2.5s
- **FID (First Input Delay)**: < 100ms
- **CLS (Cumulative Layout Shift)**: < 0.1

### Bundle Size
- Initial JS bundle: < 200KB (gzipped)
- Total page weight: < 1MB
- Images: WebP format, lazy loaded

### Caching Strategy
- Static assets: Cache for 1 year
- API responses: Cache with ETag
- Images: CDN with cache headers

---

## 🔄 Git Workflow

### Branch Naming
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `refactor/component-name` - Code refactoring
- `docs/documentation-update` - Documentation changes

### Commit Messages
```
feat: Add dark mode toggle to dashboard
fix: Resolve path exposure in download API
refactor: Extract file validation to utility function
docs: Update security standards documentation
```

### Pull Request Standards
- ✅ Descriptive title and summary
- ✅ All checks passing (tests, linting, build)
- ✅ Screenshots for UI changes
- ✅ Security review for API/auth changes
- ✅ At least one approval required

---

## 📝 Documentation Standards

### Code Comments
- ✅ Explain "why", not "what"
- ✅ Document complex algorithms
- ✅ Add JSDoc for public APIs
- ✅ Keep comments up-to-date

### README Files
- ✅ Clear installation instructions
- ✅ Usage examples
- ✅ API documentation
- ✅ Troubleshooting section

### Inline Documentation
```typescript
/**
 * Generates a secure file ID using SHA-256 hashing
 * @param fileName - Original file name
 * @param timestamp - Unix timestamp for uniqueness
 * @returns 32-character hexadecimal hash
 */
private generateSecureFileId(fileName: string, timestamp: number): string {
  // Implementation
}
```

---

This document is a living standard and should be updated as the project evolves.
Last updated: 2025-11-14
