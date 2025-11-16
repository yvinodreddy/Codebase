# Quick Reference: Maximum Claude Opus Access

## TL;DR - Best Strategy for You

**🏆 Recommended: Hybrid API + Pro Subscription**

**Cost:** $43-53/month
**Access:** Effectively unlimited for professional use
**Savings:** 75-83% vs naive approach

---

## Immediate Action Plan

### Day 1: Setup (Today)
```bash
1. Subscribe to Claude Pro Annual
   URL: https://claude.ai/upgrade
   Cost: $216/year ($18/month)

2. Create API Account
   URL: https://console.anthropic.com
   Set billing alert: $50/month

3. Get free credits (usually $5-10)
```

### Day 2: First API Call
```python
pip install anthropic

import anthropic
client = anthropic.Anthropic(api_key="your-key-here")

# Your first cached call (90% savings!)
message = client.messages.create(
    model="claude-opus-4",
    max_tokens=4096,
    system=[{
        "type": "text",
        "text": "You are an expert programmer...",  # Your system prompt
        "cache_control": {"type": "ephemeral"}  # Cache this!
    }],
    messages=[
        {"role": "user", "content": "Your question here"}
    ]
)
```

---

## Decision Tree: Which Tool to Use?

```
Need Opus for complex task?
│
├─ Interactive/Exploratory?
│  └─ YES → Use Pro Web Interface
│
├─ Can wait 24 hours?
│  └─ YES → Use Batch API (50% discount)
│
├─ Automated/High volume?
│  └─ YES → Use API with caching (90% savings)
│
└─ Simple task?
   └─ Use Sonnet instead (5x cheaper)
```

---

## Cost Optimization Cheat Sheet

### Technique 1: Prompt Caching (90% savings)
**When:** Repeated requests with same context
**How:** Add `cache_control: {"type": "ephemeral"}` to system prompt
**Savings:** $15/M → $1.50/M on cached content

### Technique 2: Batch API (50% discount)
**When:** Non-urgent tasks (24hr processing OK)
**How:** Use `/v1/batches` endpoint
**Savings:** $15/M → $7.50/M

### Technique 3: Model Routing
**When:** Task doesn't need Opus depth
**How:** Use Sonnet ($3/M) or Haiku ($0.60/M) instead
**Savings:** 80-96% on those tasks

### Technique 4: Combine Caching + Batching
**When:** Overnight code reviews with shared context
**Savings:** 95% total! ($15/M → $0.75/M)

---

## Pricing Quick Reference

| Model | Input | Output | Cached Input | Best For |
|-------|-------|--------|--------------|----------|
| Opus 4.1 | $15/M | $75/M | $1.50/M | Complex reasoning |
| Sonnet 4.5 | $3/M | $15/M | $0.30/M | Balanced tasks |
| Haiku 4.5 | $0.60/M | $3/M | $0.06/M | Speed |

**Batch Discount:** 50% off all prices
**Cache Lifetime:** 5 minutes of inactivity

---

## Monthly Budget Examples

### Light User (10 requests/day)
- **Pro Only:** $20/month
- **API Only:** ~$5/month
- **Recommended:** API only

### Moderate (30 requests/day)
- **Unoptimized API:** ~$80/month
- **Optimized API:** ~$15/month
- **Recommended:** Pro ($20) + light API

### Heavy (100 requests/day)
- **Unoptimized API:** ~$250/month
- **Optimized API:** ~$25/month
- **Recommended:** Pro ($20) + Optimized API ($25-35) = $45-55/month

---

## Workflow Patterns

### Morning Routine
```
8:00 AM - Pro Web: Review architecture, plan complex features
9:00 AM - API (Opus cached): Generate implementation code
11:00 AM - API (Sonnet): Create tests
```

### Afternoon Routine
```
2:00 PM - Pro Web: Debug complex issues interactively
4:00 PM - API (Opus): Automated code generation
```

### Evening Routine
```
5:00 PM - Collect day's code changes
5:30 PM - Submit Batch API: Overnight code review
         (Results ready by 8 AM next day)
```

---

## Common Mistakes to Avoid

❌ Using Opus for everything (use Sonnet when sufficient)
❌ Not caching system prompts (losing 90% savings)
❌ Sending full codebase as context (send only relevant files)
❌ Verbose output requests (output tokens cost 5x input)
❌ Ignoring batch API for non-urgent work
❌ Not setting billing alerts (surprise bills)
❌ Pro subscription without using it (if API is cheaper for your volume)

---

## ROI Calculation

**If Claude saves you 2 hours/month:**
- Your time value: 2 hrs × $50/hr = $100
- Cost: $50/month (hybrid approach)
- ROI: $50 profit = 100% return
- Break-even: 1 hour saved

**If Claude saves you 20 hours/month:**
- Your time value: 20 hrs × $50/hr = $1,000
- Cost: $50/month
- ROI: $950 profit = 1,900% return

**Key Insight:** Even 1 hour saved pays for itself

---

## Emergency "Need More Now" Options

### This Week: Hit Usage Limit
**Solution:** Switch to API immediately
- Set up takes 15 minutes
- Use caching from first request
- Budget $50 for emergency work
- Scale down next month

### This Month: Critical Deadline
**Solution:** Temporary budget increase
- Increase API budget to $100-200
- Still use caching/batching
- Way cheaper than hiring help
- Resume normal budget next month

### Long-term: Growing Team
**Solution:** Evaluate Team/Enterprise
- Team: $25/user (5 minimum)
- Enterprise: Custom pricing
- Contact: sales@anthropic.com

---

## Tool Comparison

### Claude Pro Web ($20/month)
✅ Interactive, fast
✅ Extended thinking mode
✅ Mobile app
✅ No coding needed
❌ Usage caps
❌ Can't automate

### Anthropic API (Variable cost)
✅ True pay-as-you-go
✅ Unlimited volume
✅ Full automation
✅ 90% savings with caching
❌ Requires coding
❌ Need to manage costs

### Hybrid (Both)
✅ Best of both worlds
✅ Interactive + automated
✅ Redundancy
✅ Maximum flexibility
❌ Higher total cost ($45-55/month)
❌ Manage two systems

---

## Success Metrics

After 1 month, you should achieve:

✅ Total cost under $60/month
✅ 50-100+ Opus requests/day capability
✅ 80%+ of API requests hitting cache
✅ 30%+ of requests via batch API
✅ Zero "out of quota" frustrations
✅ Sonnet handling 60%+ of total volume

---

## Next Steps

**Today:**
1. [ ] Subscribe to Claude Pro Annual ($216/year)
2. [ ] Create Anthropic API account
3. [ ] Set billing alert ($50)

**This Week:**
4. [ ] Make first API call with caching
5. [ ] Create system prompt template
6. [ ] Set up batch processing script
7. [ ] Track all usage in spreadsheet

**This Month:**
8. [ ] Optimize caching patterns
9. [ ] Implement model routing logic
10. [ ] Build helper automation tools
11. [ ] Review costs and adjust

**Ongoing:**
- Monitor usage weekly
- Optimize prompts monthly
- Adjust budget as needed
- Scale based on ROI

---

## Key Contacts & Resources

**Anthropic API Console:** https://console.anthropic.com
**Claude Pro Signup:** https://claude.ai/upgrade
**API Documentation:** https://docs.anthropic.com
**Pricing Details:** https://claude.ai/pricing
**Enterprise Sales:** sales@anthropic.com

**Cost Calculators:**
- See CLAUDE_OPUS_ACCESS_STRATEGY.md for Python calculators
- Estimate your costs before committing

---

## The Truth About "Unlimited"

**Reality:** No truly unlimited Opus exists at any price.

**But:** With optimization, you can:
- Handle 100+ complex requests/day
- Spend only $40-50/month
- Never worry about hitting limits
- Get Opus-quality results when you need them

**Bottom Line:** This is as close to unlimited as you can get, and it's sustainable long-term.

---

**Questions? See the full strategy document:**
`CLAUDE_OPUS_ACCESS_STRATEGY.md` (15,000+ word complete guide)
