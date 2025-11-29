# Dashboard Testing Checklist

## 1. Query Without Folder Path ✅

**Test**: Submit query without folder path
- [ ] Enter query: "What is Python?"
- [ ] Leave folder path empty
- [ ] Click Submit button
- [ ] Verify: Request succeeds
- [ ] Verify: Response displays correctly

**Expected**: Should work without folder path

---

## 2. Query With Folder Path ✅

**Test**: Submit query with valid folder path
- [ ] Enter folder path: /tmp/para-group-test-data
- [ ] Enter query: "Analyze the files in this folder"
- [ ] Click Submit button
- [ ] Verify: Request succeeds
- [ ] Verify: Response includes folder analysis

**Expected**: Should analyze folder and provide detailed response

---

## 3. Button Text Changed ✅

**Test**: Check submit button text
- [ ] Look at the main action button
- [ ] Verify text says "Submit" (not "Analyze Code")
- [ ] Verify icon is Sparkles
- [ ] Verify loading state says "Processing..."

**Expected**: Button should say "Submit"

---

## 4. Markdown Rendering ✅

**Test**: Check rich text formatting in results
- [ ] Submit query with markdown: "Explain markdown with examples"
- [ ] Verify: **Bold text** appears bold
- [ ] Verify: *Italic text* appears italic
- [ ] Verify: # Headings are formatted properly
- [ ] Verify: Lists have bullets/numbers
- [ ] Verify: Code blocks have syntax highlighting

**Expected**: All markdown should render beautifully

---

## 5. Download Markdown ✅

**Test**: Download results as markdown file
- [ ] Get a response
- [ ] Click the Markdown download button (FileText icon)
- [ ] Verify: File downloads as .md
- [ ] Open file in text editor
- [ ] Verify: Content is proper markdown

**Expected**: Downloads working .md file

---

## 6. Download Text ✅

**Test**: Download results as text file
- [ ] Get a response
- [ ] Click the Text download button (Download icon)
- [ ] Verify: File downloads as .txt
- [ ] Open file in text editor
- [ ] Verify: Content is plain text

**Expected**: Downloads working .txt file

---

## 7. Download PDF ✅

**Test**: Generate PDF from results
- [ ] Get a response
- [ ] Click the PDF download button (File icon)
- [ ] Wait for generation
- [ ] Verify: PDF downloads
- [ ] Open PDF
- [ ] Verify: Formatting preserved

**Expected**: Downloads properly formatted PDF

---

## 8. Print Functionality ✅

**Test**: Print results
- [ ] Get a response
- [ ] Click the Print button (Printer icon)
- [ ] Verify: New window opens with print preview
- [ ] Verify: Content is formatted for printing
- [ ] Verify: Can print or save as PDF

**Expected**: Print dialog opens with clean layout

---

## 9. Preview/Expand for Long Content ✅

**Test**: Show more/less for long responses
- [ ] Submit query that generates 1000+ characters
- [ ] Verify: Content is initially limited to 600px height
- [ ] Verify: "Show More" button appears
- [ ] Click "Show More"
- [ ] Verify: Full content expands
- [ ] Verify: Button changes to "Show Less"
- [ ] Click "Show Less"
- [ ] Verify: Content collapses back

**Expected**: Smooth expand/collapse animation

---

## 10. Links Open in New Tab ✅

**Test**: External links behavior
- [ ] Get response with links (submit query about URLs)
- [ ] Click any link in the response
- [ ] Verify: Opens in new tab
- [ ] Verify: External link icon appears next to link
- [ ] Verify: rel="noopener noreferrer" for security

**Expected**: Links open in new tab with icon

---

## 11. Professional Typography ✅

**Test**: Check spacing and readability
- [ ] View any response
- [ ] Check: Line spacing (1.8 line-height)
- [ ] Check: Paragraph spacing (mb-4)
- [ ] Check: Heading hierarchy (h1 > h2 > h3)
- [ ] Check: List spacing (space-y-2)
- [ ] Check: Code block padding (1.5rem)
- [ ] Check: Character spacing (tracking-wide)

**Expected**: Professional, readable layout

---

## 12. Code Syntax Highlighting ✅

**Test**: Code blocks with colors
- [ ] Submit query: "Show me a Python function"
- [ ] Verify: Code block has dark background
- [ ] Verify: Keywords are colored (def, if, return)
- [ ] Verify: Strings are colored
- [ ] Verify: Comments are dimmed
- [ ] Verify: Line numbers may appear

**Expected**: VS Code-like syntax highlighting

---

## 13. Dark Theme Colors ✅

**Test**: Verify dark theme throughout
- [ ] Check background: #0f172a (very dark blue-gray)
- [ ] Check cards: #1e293b (dark slate)
- [ ] Check text: #e2e8f0 (light gray)
- [ ] Check primary: #3b82f6 (soft blue)
- [ ] Check borders: #475569
- [ ] Check hover effects
- [ ] Check scrollbars (dark themed)

**Expected**: Consistent dark theme, easy on eyes

---

## 14. Keyboard Shortcuts ✅

**Test**: Cmd/Ctrl+Enter to submit
- [ ] Focus query textarea
- [ ] Type a query
- [ ] Press Cmd+Enter (Mac) or Ctrl+Enter (Windows)
- [ ] Verify: Form submits
- [ ] Verify: Loading state appears

**Expected**: Shortcut works like ChatGPT

---

## 15. Error Handling ✅

**Test**: Various error scenarios
- [ ] Submit with empty query (should show error)
- [ ] Submit with invalid folder path
- [ ] Test with network disconnected
- [ ] Verify: Clear error messages appear
- [ ] Verify: UI doesn't break

**Expected**: Graceful error handling

---

## 16. Responsive Design ✅

**Test**: Different screen sizes
- [ ] Test on desktop (1920x1080)
- [ ] Test on tablet (768x1024)
- [ ] Test on mobile (375x667)
- [ ] Verify: Layout adapts
- [ ] Verify: Two-column becomes one-column on mobile
- [ ] Verify: All buttons remain accessible

**Expected**: Fully responsive

---

## 17. Performance ✅

**Test**: Large responses
- [ ] Submit query generating 5000+ word response
- [ ] Verify: Page doesn't freeze
- [ ] Verify: Scrolling is smooth
- [ ] Verify: Download buttons work
- [ ] Check: Memory usage (< 200MB)

**Expected**: Handles large content gracefully

---

## 18. Accessibility ✅

**Test**: Keyboard navigation and screen readers
- [ ] Tab through all interactive elements
- [ ] Verify: Focus indicators visible
- [ ] Verify: All buttons keyboard accessible
- [ ] Test with screen reader (if available)
- [ ] Check: Alt text on icons
- [ ] Check: ARIA labels where needed

**Expected**: Fully accessible (WCAG 2.1 AA)

---

## Success Criteria

All 18 tests must pass for 100% success rate:

- [ ] 1. Query Without Folder Path
- [ ] 2. Query With Folder Path
- [ ] 3. Button Text Changed
- [ ] 4. Markdown Rendering
- [ ] 5. Download Markdown
- [ ] 6. Download Text
- [ ] 7. Download PDF
- [ ] 8. Print Functionality
- [ ] 9. Preview/Expand
- [ ] 10. Links in New Tab
- [ ] 11. Professional Typography
- [ ] 12. Syntax Highlighting
- [ ] 13. Dark Theme Colors
- [ ] 14. Keyboard Shortcuts
- [ ] 15. Error Handling
- [ ] 16. Responsive Design
- [ ] 17. Performance
- [ ] 18. Accessibility

**Target**: 18/18 tests passing (100% success rate)
