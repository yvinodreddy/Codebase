# Smart Read Generator - Quick Reference

## One-Line Usage

```bash
./smart_read_generator.sh <filename>
```

## Common Commands

```bash
# Current directory file
./smart_read_generator.sh index-previous.html

# Absolute path
./smart_read_generator.sh /home/user01/claude-test/Exam/index-previous.html

# Relative path
./smart_read_generator.sh ../other-directory/file.txt

# Run tests
./test_smart_generator.sh
```

## What Happens

1. Script analyzes file ✓
2. Generates optimal chunks ✓
3. Validates 100% of chunks ✓
4. Displays production-ready commands ✓
5. Saves to PRODUCTION_READ_COMMANDS.txt ✓

## Copy Command From Output

Look for this section:
```
SINGLE-LINE FORMAT:
---
Read(/path/to/file, offset=0, limit=3), then Read(...)
```

**Copy that entire line** and use it!

## Key Limits

- **File Size:** 256KB max
- **Tokens:** 25000 max (~100KB)
- **Safety:** Script uses 80% (78KB chunks)

## Errors?

| Error | Solution |
|-------|----------|
| No filename provided | Add filename: `./smart_read_generator.sh yourfile.txt` |
| File not found | Check path and filename spelling |
| File is empty | Use a file with content |
| Permission denied | Check file permissions: `chmod +r yourfile.txt` |

## For Oversized Lines

If the script says "Lines too large to read: 3 23", use Grep:
```
Grep(pattern="search-term", path="/path/to/file", output_mode="content")
```

## Output File

Commands saved to: **PRODUCTION_READ_COMMANDS.txt**

Open it and copy the SINGLE-LINE FORMAT!

---

**That's it! Simple as:**
```bash
./smart_read_generator.sh yourfile.txt
```
**Then copy the output command!**
