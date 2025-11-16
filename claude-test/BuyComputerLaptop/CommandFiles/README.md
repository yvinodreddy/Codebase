# Claude Code Custom Commands

This directory contains custom slash commands for Claude Code.

## Available Commands

### `/laptop-comparison` - Laptop Purchase Guide Generator

**Purpose:** Generate comprehensive, mobile-responsive HTML laptop comparison guides with AI/ML performance analysis.

**When to use:**
- Researching laptop purchases
- Comparing multiple laptop models
- Need detailed AI/ML hardware analysis
- Want India market pricing and purchase links
- Need budget vs. longevity analysis

**How to use:**

```bash
/laptop-comparison

# Then provide:
# 1. List of laptops you're considering
# 2. Your budget range
# 3. Primary use case (AI/ML, gaming, development)
# 4. Desired specs (RAM, GPU, CPU)
# 5. Expected longevity (years)
```

**Example:**

```
/laptop-comparison

I'm looking at these laptops for AI/ML work:
1. Lenovo Legion Pro 5 (i7-14650HX + RTX 4060)
2. HP OMEN 16 (Ryzen 7 + RTX 4060)
3. Dell XPS 15 (i7 + RTX 4050)

Budget: ₹1.5 lakhs (can stretch if needed)
Requirements: 32GB RAM, good GPU for deep learning, 6-8 year lifespan
```

**Output:**
- Single HTML file (70KB+)
- Mobile-responsive with Bootstrap
- Detailed performance scores for each laptop
- Budget analysis and recommendations
- Purchase links for India market
- Complete action plan

**Features Generated:**
✅ AI/ML performance score breakdowns (GPU, CPU, RAM, Longevity)
✅ Visual score bars with color coding
✅ Budget stretch ROI analysis
✅ Comparison tables
✅ Technical deep dive (why specs matter)
✅ Purchase tips for India market
✅ Decision tree and action plan
✅ Bonus recommendations beyond your list

---

## How Slash Commands Work

Slash commands are stored in `.claude/commands/` as markdown files.

**To create a new command:**
1. Create a `.md` file in `.claude/commands/`
2. Add instructions for Claude
3. Use the command with `/command-name`

**Current Location:** `/home/user01/claude-test/.claude/commands/`

**To use from anywhere:**
- Navigate to `/home/user01/claude-test/` directory
- Run `/laptop-comparison` with your laptop details
- Claude will generate the complete HTML guide

---

## Tips

- Commands work best when you provide detailed requirements
- Be specific about budget, use case, and must-have specs
- Mention if budget is flexible for longevity
- The more laptops you provide, the better the comparison
- Output is always mobile-responsive HTML ready to view in browser

---

Last updated: October 20, 2025
