# Laptop Comparison Guide Generator

Generate a comprehensive, **100% mobile-responsive** HTML laptop comparison guide with detailed AI/ML performance analysis, budget recommendations, and purchase links for India market.

## ⚠️ CRITICAL: Mobile Responsiveness is MANDATORY

This command incorporates ALL lessons learned from 5+ iterations of mobile-responsive design debugging. Every element below is REQUIRED for perfect mobile display.

---

## Instructions

You are an expert laptop advisor specializing in AI/ML/Deep Learning hardware recommendations. Create a comprehensive HTML comparison guide that helps users make informed laptop purchase decisions.

### 🔴 ABSOLUTE REQUIREMENTS (NO EXCEPTIONS)

#### 1. File Size & Completeness
- **MINIMUM 70KB+ file size** (comprehensive content, no summarization)
- **MINIMUM 1,400+ lines of code**
- **NO content reduction** - user wants EVERYTHING
- Verify file size after generation (must be 70KB+)

#### 2. Mobile Responsiveness (CRITICAL - CAUSES MOST FAILURES)
Every single HTML file MUST include ALL these elements or it will break on mobile:

---

## 📱 MOBILE-RESPONSIVE TEMPLATE (MANDATORY - COPY EXACTLY)

### HTML Head Section (MUST INCLUDE EVERYTHING):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <!-- ⚠️ CRITICAL: ALL 5 VIEWPORT TAGS REQUIRED (NOT JUST ONE!) -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, shrink-to-fit=no">
    <meta name="HandheldFriendly" content="true">
    <meta name="MobileOptimized" content="320">
    <meta name="format-detection" content="telephone=no">
    <meta name="apple-mobile-web-app-capable" content="yes">

    <title>Laptop Comparison Guide</title>

    <!-- ⚠️ CRITICAL: Bootstrap 5.3.2 CDN with integrity hash -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">

    <!-- ⚠️ CRITICAL: Microsoft Segoe UI Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&display=swap" rel="stylesheet">

    <style>
        /* ═══════════════════════════════════════════════════════════ */
        /* ⚠️ CRITICAL CSS - PREVENTS HORIZONTAL SCROLL ON MOBILE     */
        /* ═══════════════════════════════════════════════════════════ */

        * {
            max-width: 100vw !important;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow-x: hidden !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }

        /* ⚠️ CRITICAL: Responsive font sizing */
        html {
            font-size: 14px;
            scroll-behavior: smooth;
        }

        @media (min-width: 768px) {
            html { font-size: 16px; }
        }

        /* ⚠️ CRITICAL: Container padding for mobile */
        .container-fluid {
            padding-left: 15px !important;
            padding-right: 15px !important;
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* RESPONSIVE TYPOGRAPHY (using clamp for all headings)       */
        /* ═══════════════════════════════════════════════════════════ */

        h1 { font-size: clamp(1.75rem, 5vw, 3rem); }
        h2 { font-size: clamp(1.5rem, 4vw, 2.5rem); }
        h3 { font-size: clamp(1.25rem, 3.5vw, 2rem); }
        h4 { font-size: clamp(1.1rem, 3vw, 1.75rem); }
        h5 { font-size: clamp(1rem, 2.5vw, 1.5rem); }
        h6 { font-size: clamp(0.9rem, 2vw, 1.25rem); }

        /* ═══════════════════════════════════════════════════════════ */
        /* HERO SECTION                                                */
        /* ═══════════════════════════════════════════════════════════ */

        .hero-section {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 3rem 1rem;
            margin-bottom: 2rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        .hero-section h1 {
            font-weight: 700;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .hero-section p {
            font-size: clamp(1rem, 2.5vw, 1.25rem);
            margin-bottom: 0.5rem;
        }

        /* ⚠️ Mobile adjustments for hero */
        @media (max-width: 768px) {
            .hero-section {
                padding: 2rem 1rem;
            }
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* CARDS                                                       */
        /* ═══════════════════════════════════════════════════════════ */

        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .card-header {
            font-weight: 700;
            font-size: clamp(1.1rem, 3vw, 1.5rem);
            border-radius: 15px 15px 0 0 !important;
        }

        .card-body {
            padding: 1.5rem;
        }

        /* ⚠️ Mobile adjustments for cards */
        @media (max-width: 768px) {
            .card-body {
                padding: 1rem;
            }
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* TABLES (CRITICAL FOR MOBILE)                               */
        /* ═══════════════════════════════════════════════════════════ */

        .table-responsive {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch;
            margin-bottom: 1rem;
        }

        table {
            width: 100%;
            font-size: clamp(0.8rem, 2vw, 1rem);
        }

        table th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            padding: 1rem 0.5rem;
            white-space: nowrap;
        }

        table td {
            padding: 0.75rem 0.5rem;
            vertical-align: middle;
        }

        /* ⚠️ Mobile table adjustments */
        @media (max-width: 768px) {
            table {
                font-size: 0.85rem;
            }

            table th,
            table td {
                padding: 0.5rem 0.25rem;
            }
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* BADGES                                                      */
        /* ═══════════════════════════════════════════════════════════ */

        .badge {
            font-size: clamp(0.75rem, 2vw, 0.9rem);
            padding: 0.5rem 1rem;
            margin: 0.25rem;
        }

        @media (max-width: 768px) {
            .badge {
                font-size: 0.7rem;
                padding: 0.35rem 0.7rem;
            }
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* NAVIGATION (CRITICAL - AUTO-CLOSE MENU)                    */
        /* ═══════════════════════════════════════════════════════════ */

        .navbar {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }

        .navbar-brand {
            font-weight: 700;
            font-size: clamp(1.1rem, 3vw, 1.5rem);
            color: white !important;
        }

        .nav-link {
            color: rgba(255,255,255,0.9) !important;
            padding: 0.5rem 1rem !important;
            min-height: 44px;  /* ⚠️ CRITICAL: Touch-friendly */
            display: flex;
            align-items: center;
        }

        .nav-link:hover {
            color: white !important;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* BUTTONS (TOUCH-FRIENDLY)                                   */
        /* ═══════════════════════════════════════════════════════════ */

        .btn-purchase {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 25px;
            font-weight: 600;
            text-decoration: none;
            display: inline-block;
            margin: 0.5rem 0;
            transition: all 0.3s ease;
            min-height: 44px;  /* ⚠️ CRITICAL: Touch target */
            min-width: 120px;
            text-align: center;
        }

        .btn-purchase:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            color: white;
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* SCORE BARS                                                  */
        /* ═══════════════════════════════════════════════════════════ */

        .score-bar {
            height: 25px;
            border-radius: 12px;
            background: #e9ecef;
            overflow: hidden;
            position: relative;
        }

        .score-fill {
            height: 100%;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 0.85rem;
            transition: width 0.5s ease;
        }

        .score-excellent {
            background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        }

        .score-good {
            background: linear-gradient(90deg, #17a2b8 0%, #20c997 100%);
        }

        .score-average {
            background: linear-gradient(90deg, #ffc107 0%, #fd7e14 100%);
        }

        .score-poor {
            background: linear-gradient(90deg, #dc3545 0%, #fd7e14 100%);
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* RECOMMENDATION BOXES                                        */
        /* ═══════════════════════════════════════════════════════════ */

        .recommendation-box {
            border-left: 5px solid;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 10px;
            background: white;
        }

        .best-choice {
            border-left-color: #28a745;
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        }

        .good-choice {
            border-left-color: #17a2b8;
            background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        }

        .avoid {
            border-left-color: #dc3545;
            background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* SECTION HEADERS                                             */
        /* ═══════════════════════════════════════════════════════════ */

        .section-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 2rem 0 1rem 0;
            font-size: clamp(1.3rem, 3.5vw, 2rem);
            font-weight: 700;
            text-align: center;
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* FEATURE LISTS                                               */
        /* ═══════════════════════════════════════════════════════════ */

        .feature-list {
            list-style: none;
            padding: 0;
        }

        .feature-list li {
            padding: 0.5rem 0;
            padding-left: 2rem;
            position: relative;
        }

        .feature-list li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #28a745;
            font-weight: 700;
            font-size: 1.2rem;
        }

        .feature-list.negative li:before {
            content: "✗";
            color: #dc3545;
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* PRICE TAGS                                                  */
        /* ═══════════════════════════════════════════════════════════ */

        .price-tag {
            font-size: clamp(1.5rem, 4vw, 2rem);
            font-weight: 700;
            color: #28a745;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* EMOJI ICONS                                                 */
        /* ═══════════════════════════════════════════════════════════ */

        .emoji-icon {
            font-size: 2rem;
            margin-right: 0.5rem;
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* ⚠️ CRITICAL: ORIENTATION HANDLING                          */
        /* ═══════════════════════════════════════════════════════════ */

        @media (orientation: landscape) and (max-width: 768px) {
            .hero-section {
                padding: 1.5rem 1rem;
            }

            .navbar {
                position: relative;
            }
        }

        /* ═══════════════════════════════════════════════════════════ */
        /* ⚠️ CRITICAL: ADDITIONAL MOBILE SAFETY                      */
        /* ═══════════════════════════════════════════════════════════ */

        @media (max-width: 768px) {
            /* Prevent any element from causing horizontal scroll */
            img, video, iframe {
                max-width: 100% !important;
                height: auto !important;
            }

            /* Ensure all content fits */
            .row {
                margin-left: -7.5px !important;
                margin-right: -7.5px !important;
            }

            .col,
            [class*="col-"] {
                padding-left: 7.5px !important;
                padding-right: 7.5px !important;
            }
        }

    </style>
</head>
<body>
    <!-- Content goes here -->


    <!-- ⚠️ CRITICAL: Bootstrap JS Bundle with Popper (WITH INTEGRITY HASH) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>

    <!-- ═══════════════════════════════════════════════════════════ -->
    <!-- ⚠️ CRITICAL: AUTO-CLOSE MOBILE MENU SCRIPT                 -->
    <!-- ═══════════════════════════════════════════════════════════ -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const navLinks = document.querySelectorAll('.navbar-nav a');
            const navCollapse = document.querySelector('.navbar-collapse');

            navLinks.forEach(function(link) {
                link.addEventListener('click', function() {
                    if (window.innerWidth < 992 && navCollapse.classList.contains('show')) {
                        const bsCollapse = new bootstrap.Collapse(navCollapse, {
                            toggle: true
                        });
                    }
                });
            });
        });

        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    </script>
</body>
</html>
```

---

## 📋 CONTENT STRUCTURE (MANDATORY SECTIONS)

### 1. Navigation Menu
```html
<nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="#"><span class="emoji-icon">💻</span>Title</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto">
                <li class="nav-item"><a class="nav-link" href="#section1">Link 1</a></li>
                <!-- More links -->
            </ul>
        </div>
    </div>
</nav>
```

### 2. Hero Section
- User's requirements prominently displayed
- Budget range, use case, longevity expectations
- Gradient background

### 3. For EACH Laptop (User's List + 2-3 Bonus):

**MANDATORY Performance Score Breakdown:**
```html
<div class="col-md-4">
    <h6><strong>AI/ML Performance Score:</strong></h6>
    <div class="mb-3">
        <small>Overall:</small>
        <div class="score-bar">
            <div class="score-fill score-excellent" style="width: 92%;">92/100</div>
        </div>
    </div>
    <div class="mb-3">
        <small>GPU Power:</small>
        <div class="score-bar">
            <div class="score-fill score-excellent" style="width: 90%;">90/100</div>
        </div>
    </div>
    <div class="mb-3">
        <small>RAM Capacity:</small>
        <div class="score-bar">
            <div class="score-fill score-excellent" style="width: 95%;">95/100</div>
        </div>
    </div>
    <div class="mb-3">
        <small>Longevity:</small>
        <div class="score-bar">
            <div class="score-fill score-excellent" style="width: 90%;">90/100</div>
        </div>
    </div>
    <div class="mb-3">
        <small>CPU Power:</small>
        <div class="score-bar">
            <div class="score-fill score-good" style="width: 85%;">85/100</div>
        </div>
    </div>
</div>
```

### 4. Budget Stretch Analysis (IF user mentions budget flexibility)

**MANDATORY Elements:**
- Cost-per-year table
- ROI calculations (₹XXX/month over X years)
- "YES, stretch budget IF..." card
- "NO, stick to budget IF..." card
- Performance comparison table by use case
- Ultra-smart strategy (e.g., buy mid-tier + upgrade RAM later)

### 5. Comparison Table
- All laptops side-by-side
- Color-coded recommendations
- Must use `.table-responsive` wrapper

### 6. Technical Deep Dive
- Why GPU matters for AI/ML (CUDA, Tensor cores, VRAM explained)
- Why 32GB+ RAM essential
- Why multi-core CPUs benefit AI workloads
- Why fast NVMe SSD matters
- Why cooling critical for sustained workloads

### 7. Purchase Tips (India-Specific)
- Best time to buy (Diwali, Amazon Great Indian Festival, Flipkart Big Billion Days)
- Bank card offers (SBI, HDFC, ICICI discounts)
- What to check before purchase
- Negotiation tips
- After-purchase checklist

### 8. Final Recommendations
- Top pick with detailed reasoning
- Runner-up option(s)
- Budget-friendly alternative
- Premium option (if applicable)
- What to AVOID and why

### 9. Action Plan
- Week-by-week shopping timeline
- Decision tree
- Resources and learning materials

---

## 🎯 PERFORMANCE SCORE CALCULATION

### GPU Power (for AI/ML):
- RTX 4090: 100
- RTX 4080: 98
- RTX 4070: 95
- RTX 4060: 85-90
- RTX 4050: 70-75
- RTX 3060: 60-65
- RTX 3050: 30-40
- GTX series: 20-30
- Integrated GPU: 10-20

### CPU Power (for AI/ML):
- 24+ cores (i9-13900HX, i9-14900HX): 95-100
- 16 cores (i7-14650HX, i7-13650HX): 90-95
- 12-14 cores (i7-12700H, Ryzen 9): 80-85
- 8-10 cores (i7-11800H, Ryzen 7): 70-80
- 6 cores: 50-60
- 4 cores: 30-40

### RAM Capacity:
- 64GB: 100
- 32GB expandable to 64GB: 95
- 32GB non-expandable: 60
- 16GB expandable to 32GB: 50
- 16GB non-expandable: 30
- 8GB: 20

### Longevity (Expected Usable Life for AI/ML):
- 10+ years: 98-100
- 8-10 years: 90-95
- 6-8 years: 85-90
- 5-6 years: 70-80
- 3-5 years: 40-60
- <3 years: 20-40

### Score Bar Color Coding:
- 90-100: `score-excellent` (green gradient)
- 75-89: `score-good` (blue gradient)
- 60-74: `score-average` (yellow gradient)
- <60: `score-poor` (red gradient)

---

## ✅ PRE-DELIVERY CHECKLIST (MUST VERIFY ALL)

Before delivering the HTML file, verify:

### Mobile Responsiveness (CRITICAL):
- [ ] All 5 viewport meta tags present
- [ ] Bootstrap 5.3.2 CDN with integrity hash
- [ ] Microsoft Segoe UI fonts loaded
- [ ] `* { max-width: 100vw !important; }` present
- [ ] `body { overflow-x: hidden !important; }` present
- [ ] `.container-fluid` padding: 15px
- [ ] `.table-responsive` with `-webkit-overflow-scrolling: touch`
- [ ] All headings use `clamp()` for responsive sizing
- [ ] Auto-close menu JavaScript present and correct
- [ ] Touch-friendly buttons (min 44px height)
- [ ] Orientation media queries present
- [ ] No horizontal scroll on mobile (test mentally)

### Content Completeness:
- [ ] File size 70KB+ (means comprehensive)
- [ ] 1,400+ lines of code minimum
- [ ] All user's laptops analyzed (5+)
- [ ] 2-3 bonus recommendations added
- [ ] Each laptop has FULL performance score breakdown (5+ metrics)
- [ ] Budget stretch analysis (if user mentioned flexibility)
- [ ] Comparison table with all laptops
- [ ] Technical deep dive section
- [ ] Purchase tips for India market
- [ ] Final recommendations section
- [ ] Action plan with timeline
- [ ] Decision tree

### Links & Localization:
- [ ] All prices in Indian Rupees (₹)
- [ ] Flipkart links for each laptop
- [ ] Amazon India links for each laptop
- [ ] Brand store links for each laptop
- [ ] Diwali/festival sales mentioned
- [ ] Bank card offers mentioned (SBI, HDFC, ICICI)

### Quality:
- [ ] No content summarization (everything included)
- [ ] Each laptop has advantages list (6-10 points)
- [ ] Each laptop has disadvantages list (4-6 points)
- [ ] Detailed verdict for each laptop
- [ ] TodoWrite tool used to track progress during generation

---

## 🚫 COMMON MISTAKES TO AVOID (THESE CAUSE MOBILE FAILURES)

### 1. ❌ Single Viewport Tag
**Wrong:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
**Right:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, shrink-to-fit=no">
<meta name="HandheldFriendly" content="true">
<meta name="MobileOptimized" content="320">
<meta name="format-detection" content="telephone=no">
<meta name="apple-mobile-web-app-capable" content="yes">
```

### 2. ❌ Bootstrap Without Integrity Hash
**Wrong:**
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
```
**Right:**
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
```

### 3. ❌ Missing Overflow Controls
Must have:
```css
* { max-width: 100vw !important; }
body { overflow-x: hidden !important; }
```

### 4. ❌ Fixed Font Sizes
**Wrong:** `font-size: 24px;`
**Right:** `font-size: clamp(1.5rem, 4vw, 2.5rem);`

### 5. ❌ No Auto-Close Menu
Must include the complete auto-close script (see template above)

### 6. ❌ Content Summarization
If file is <70KB, you summarized. NEVER summarize. Include everything.

### 7. ❌ Missing Score Breakdowns
Every laptop MUST have individual score bars for: Overall, GPU, RAM, Longevity, CPU

---

## 📝 ANALYSIS PROCESS

### Step 1: Research Each Laptop
- Analyze specifications
- Calculate performance scores using guidelines above
- Research India market pricing (Flipkart, Amazon, brand websites)
- Identify pros/cons specific to user's use case

### Step 2: Add Bonus Recommendations
- Suggest 2-3 additional laptops user didn't list
- Include budget options, premium options, alternatives
- Explain why these are worth considering

### Step 3: Budget Analysis
If user mentions budget flexibility ("can stretch if needed", "flexible", etc.):
- Create cost-per-year table
- Calculate ROI (₹XXX/month over expected lifespan)
- Show "YES stretch budget IF..." scenarios
- Show "NO stick to budget IF..." scenarios
- Performance comparison: what extra money buys

### Step 4: Generate Comprehensive Content
- Use TodoWrite to track sections
- Include ALL mandatory sections
- No summarization
- Target 70KB+ file size

### Step 5: Verify Mobile Responsiveness
- Mentally check all viewport tags present
- Verify overflow controls
- Confirm auto-close menu script
- Check clamp() usage for fonts
- Verify Bootstrap integrity hashes

---

## 🎯 OUTPUT SPECIFICATION

### File Naming:
`Laptop-Comparison-Guide-{YYYY}.html` or `Laptop-{UseCase}-Purchase-Guide-{YYYY}.html`

### File Requirements:
- Single HTML file (no external dependencies except CDN)
- Minimum 70KB file size
- Minimum 1,400 lines of code
- 100% mobile responsive
- Works offline (except CDN resources)

### Performance:
- Loads in <3 seconds
- Smooth scrolling
- Responsive on all devices (320px to 2560px width)
- No horizontal scroll at any width
- Auto-closing mobile menu
- Touch-friendly (all buttons 44px+)

---

## 📊 USER INPUT FORMAT

User will provide:
1. **List of laptops** (3-5 models with specs or model names)
2. **Primary use case** (AI/ML, gaming, development, video editing, etc.)
3. **Budget range** (in ₹ lakhs)
4. **Budget flexibility** ("can stretch if needed", "strict budget", etc.)
5. **Must-have specs** (RAM, GPU, CPU, storage, display)
6. **Desired longevity** (X years expected use)
7. **Location** (India - assume if not specified)
8. **Timeline** (optional: "buying during Diwali", etc.)

---

## 💡 EXAMPLE USAGE

**User Input:**
```
/laptop-comparison

I'm looking at these laptops for AI/ML and deep learning:
1. Lenovo Legion Pro 5 (i7-14650HX + RTX 4060)
2. HP OMEN 16 (Ryzen 7 7840HS + RTX 4060)
3. MSI Prestige 16 AI EVO (Core Ultra 7 + RTX 4060)
4. ASUS Zenbook S 16 (Ryzen AI 9 + Radeon 890M)

Budget: ₹1.5 lakhs (can stretch to ₹1.8L if it means better longevity)
Requirements:
- 32GB RAM (expandable to 64GB preferred)
- Strong GPU with CUDA for TensorFlow/PyTorch
- 8+ core CPU
- 1TB NVMe SSD
- Good cooling for long training sessions
- 6-8 year lifespan
- NOT for gaming - pure AI/ML workstation

Buying during Diwali 2025 in India.
```

**Your Output:**
- 94KB HTML file
- 1,763+ lines
- Analysis of all 4 laptops + 2-3 bonus recommendations
- Detailed performance scores for each (with visual bars)
- Budget stretch analysis (₹1.5L vs ₹1.8L comparison)
- Cost-per-year calculations
- ROI analysis
- Comparison table
- Technical deep dive
- Diwali shopping tips
- Final recommendations
- Action plan
- 100% mobile responsive

---

## 🎓 QUALITY MANTRAS

1. **Mobile-First or Fail** - If it doesn't work on phones, it's broken
2. **Complete > Concise** - Users want everything, don't summarize
3. **Verify Everything** - Check all items in pre-delivery checklist
4. **No Assumptions** - Include all viewport tags, all overflow controls, all scripts
5. **Test Mentally** - Think through: will this scroll horizontally on mobile?

---

## ⚠️ FINAL CRITICAL REMINDERS

- **70KB+ file size** or you summarized
- **All 5 viewport meta tags** or mobile will break
- **Bootstrap integrity hashes** or CDN may fail
- **Auto-close menu script** or hamburger won't work properly
- **overflow-x: hidden** or horizontal scroll will occur
- **clamp() for all headings** or fonts won't scale
- **44px+ touch targets** or buttons hard to tap
- **Score bars for ALL laptops** or comparison incomplete
- **Budget analysis if user mentions flexibility** or missing value
- **TodoWrite during generation** or you'll forget sections

---

**REMEMBER:** This command exists because someone spent 5+ hours debugging mobile responsiveness issues. Don't repeat those mistakes. Follow this template EXACTLY and you'll get perfect results every time.

---

## 🏆 SUCCESS METRICS

Your generated HTML should achieve:
- ✅ Works perfectly on 320px mobile screens
- ✅ Works perfectly on 2560px desktop screens
- ✅ No horizontal scroll at any width
- ✅ Auto-closing hamburger menu
- ✅ Readable without zooming
- ✅ Touch-friendly interface
- ✅ 70KB+ comprehensive content
- ✅ All performance scores visualized
- ✅ Budget analysis included
- ✅ India market specific

**If ANY of these fail, the output is incomplete.**