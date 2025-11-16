#!/bin/bash

# SMART READ GENERATOR - PRODUCTION READY v2.0
# Usage: ./smart_read_generator.sh <filename>
# Generates token-aware Read commands for large files

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MAX_SIZE_KB=256
MAX_TOKENS=25000
SAFE_MARGIN=0.8  # Use 80% of max for safety
SAFE_TOKENS=$((MAX_TOKENS * 80 / 100))  # 20000 tokens
CHARS_PER_TOKEN=4
SAFE_CHARS=$((SAFE_TOKENS * CHARS_PER_TOKEN))  # 80000 chars
SAFE_SIZE_KB=$((SAFE_CHARS / 1024))  # ~78KB

# Function to print colored output
print_header() {
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Validate arguments
if [ $# -eq 0 ]; then
    print_error "ERROR: No filename provided"
    echo ""
    echo "Usage: $0 <filename>"
    echo ""
    echo "Examples:"
    echo "  $0 index-previous.html"
    echo "  $0 /absolute/path/to/file.html"
    echo "  $0 ../relative/path/to/file.txt"
    echo ""
    exit 1
fi

INPUT_FILE="$1"

# Check if file exists
if [ ! -f "$INPUT_FILE" ]; then
    print_error "ERROR: File not found: $INPUT_FILE"
    echo ""
    echo "Please check:"
    echo "  - File path is correct"
    echo "  - File exists in the specified location"
    echo "  - You have permission to access the file"
    echo ""
    exit 1
fi

# Check if file is readable
if [ ! -r "$INPUT_FILE" ]; then
    print_error "ERROR: File is not readable: $INPUT_FILE"
    echo ""
    echo "Please check file permissions and try again."
    echo ""
    exit 1
fi

# Get absolute path
FILE=$(realpath "$INPUT_FILE")

# Check if file is empty
if [ ! -s "$FILE" ]; then
    print_error "ERROR: File is empty: $FILE"
    echo ""
    exit 1
fi

# Count total lines
TOTAL_LINES=$(wc -l < "$FILE")

# Handle files with no trailing newline
LAST_CHAR=$(tail -c 1 "$FILE")
if [ -n "$LAST_CHAR" ]; then
    TOTAL_LINES=$((TOTAL_LINES + 1))
fi

# Check if file has content
if [ $TOTAL_LINES -eq 0 ]; then
    print_error "ERROR: File has no lines: $FILE"
    echo ""
    exit 1
fi

# Get file size
FILE_SIZE=$(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE" 2>/dev/null)
FILE_SIZE_KB=$((FILE_SIZE / 1024))

# Display analysis header
print_header "SMART READ GENERATOR - TOKEN-AWARE WITH AUTO-SKIP"
echo ""
echo "  File: $FILE"
echo "  File size: ${FILE_SIZE_KB}KB"
echo "  Total lines: $TOTAL_LINES"
echo "  Max tokens: $MAX_TOKENS"
echo "  Safe tokens: $SAFE_TOKENS (80% margin)"
echo "  Safe size per chunk: ${SAFE_SIZE_KB}KB"
echo ""
print_header "STEP 1: Analyzing file line-by-line"
echo ""

# Step 1: Identify lines that are too large to read individually
oversized_lines=()
line_sizes=()

for ((line=0; line<TOTAL_LINES; line++)); do
    LINE_CONTENT=$(sed -n "$((line+1))p" "$FILE")
    LINE_SIZE=${#LINE_CONTENT}
    line_sizes[$line]=$LINE_SIZE
    LINE_TOKENS=$((LINE_SIZE / CHARS_PER_TOKEN))

    if [ $LINE_TOKENS -gt $MAX_TOKENS ]; then
        LINE_SIZE_KB=$((LINE_SIZE / 1024))
        oversized_lines+=($line)
        print_warning "Line $line: ${LINE_SIZE_KB}KB (~$LINE_TOKENS tokens) - TOO LARGE"
    fi
done

if [ ${#oversized_lines[@]} -eq 0 ]; then
    print_success "No oversized lines found - all lines can be read!"
else
    echo ""
    print_warning "Found ${#oversized_lines[@]} oversized line(s): ${oversized_lines[*]}"
fi

echo ""
print_header "STEP 2: Generating optimal chunks (skipping oversized lines)"
echo ""

# Step 2: Generate chunks, skipping oversized lines
chunks=()
current_size=0
chunk_start=-1

for ((line=0; line<TOTAL_LINES; line++)); do
    # Check if this line is oversized
    is_oversized=false
    for oversized in "${oversized_lines[@]}"; do
        if [ $oversized -eq $line ]; then
            is_oversized=true
            break
        fi
    done

    if [ "$is_oversized" = true ]; then
        # Finalize current chunk if exists
        if [ $chunk_start -ge 0 ]; then
            chunk_limit=$((line - chunk_start))
            chunks+=("$chunk_start:$chunk_limit")
            chunk_start=-1
            current_size=0
        fi
        continue
    fi

    # Process normal line
    LINE_SIZE=${line_sizes[$line]}

    if [ $chunk_start -eq -1 ]; then
        # Start new chunk
        chunk_start=$line
        current_size=$LINE_SIZE
    elif [ $((current_size + LINE_SIZE)) -gt $SAFE_CHARS ]; then
        # Current chunk is full, finalize it
        chunk_limit=$((line - chunk_start))
        chunks+=("$chunk_start:$chunk_limit")
        chunk_start=$line
        current_size=$LINE_SIZE
    else
        # Add to current chunk
        current_size=$((current_size + LINE_SIZE))
    fi
done

# Add final chunk
if [ $chunk_start -ge 0 ]; then
    chunk_limit=$((TOTAL_LINES - chunk_start))
    chunks+=("$chunk_start:$chunk_limit")
fi

print_success "Generated ${#chunks[@]} chunks"
echo ""
print_header "STEP 3: Validating chunks"
echo ""

# Step 3: Validate all chunks
ALL_VALID=true
for chunk in "${chunks[@]}"; do
    IFS=':' read -r offset limit <<< "$chunk"
    end_line=$((offset + limit))

    chunk_size=0
    for ((line=offset; line<end_line; line++)); do
        chunk_size=$((chunk_size + ${line_sizes[$line]}))
    done

    chunk_size_kb=$((chunk_size / 1024))
    estimated_tokens=$((chunk_size / CHARS_PER_TOKEN))

    echo "✓ offset=$offset, limit=$limit → ${chunk_size_kb}KB, ~$estimated_tokens tokens"

    if [ $chunk_size_kb -gt $MAX_SIZE_KB ] || [ $estimated_tokens -gt $MAX_TOKENS ]; then
        print_error "  INVALID - Exceeds limits!"
        ALL_VALID=false
    fi
done

echo ""

if [ "$ALL_VALID" = false ]; then
    print_error "ERROR: Validation failed!"
    exit 1
fi

print_success "All chunks validated successfully!"
echo ""

print_header "STEP 4: PRODUCTION-READY COMMANDS"
echo ""

# Step 4: Generate commands
# Single-line format
echo "SINGLE-LINE FORMAT:"
echo "---"
single_line=""
for i in "${!chunks[@]}"; do
    IFS=':' read -r offset limit <<< "${chunks[$i]}"
    if [ $i -eq 0 ]; then
        single_line="Read($FILE, offset=$offset, limit=$limit)"
    else
        single_line="$single_line, then Read($FILE, offset=$offset, limit=$limit)"
    fi
done
echo "$single_line"
echo ""

# Multi-line format
echo "MULTI-LINE FORMAT:"
echo "---"
for i in "${!chunks[@]}"; do
    IFS=':' read -r offset limit <<< "${chunks[$i]}"
    if [ $i -eq $((${#chunks[@]} - 1)) ]; then
        echo "then Read($FILE, offset=$offset, limit=$limit)"
    else
        echo "Read($FILE, offset=$offset, limit=$limit),"
    fi
done
echo ""

# Summary
readable_lines=$((TOTAL_LINES - ${#oversized_lines[@]}))
coverage=$((readable_lines * 100 / TOTAL_LINES))

print_header "SUMMARY"
echo ""
echo "Total lines: $TOTAL_LINES"
echo "Readable via offset/limit: $readable_lines ($coverage%)"
if [ ${#oversized_lines[@]} -gt 0 ]; then
    echo "Oversized (use Grep instead): ${#oversized_lines[@]}"
    echo "  Lines to skip: ${oversized_lines[*]}"
fi
echo "Total chunks: ${#chunks[@]}"
echo ""
print_success "PRODUCTION READY"
echo ""

# Save to file
OUTPUT_FILE="/home/user01/claude-test/Read_Large_Files/OUTPUT_RESULT_PRODUCTION_READ_COMMANDS.txt"
cat > "$OUTPUT_FILE" << EOF
════════════════════════════════════════════════════════════
  PRODUCTION-READY READ COMMANDS
  Generated: $(date)
════════════════════════════════════════════════════════════

FILE: $FILE
FILE SIZE: ${FILE_SIZE_KB}KB
TOTAL LINES: $TOTAL_LINES
READABLE LINES: $readable_lines ($coverage%)
CHUNKS: ${#chunks[@]}

SINGLE-LINE FORMAT (copy this):
═══════════════════════════════════════════════════════════

$single_line

MULTI-LINE FORMAT:
═══════════════════════════════════════════════════════════

EOF

for i in "${!chunks[@]}"; do
    IFS=':' read -r offset limit <<< "${chunks[$i]}"
    if [ $i -eq $((${#chunks[@]} - 1)) ]; then
        echo "then Read($FILE, offset=$offset, limit=$limit)" >> "$OUTPUT_FILE"
    else
        echo "Read($FILE, offset=$offset, limit=$limit)," >> "$OUTPUT_FILE"
    fi
done

if [ ${#oversized_lines[@]} -gt 0 ]; then
    cat >> "$OUTPUT_FILE" << EOF

OVERSIZED LINES (use Grep to search):
═══════════════════════════════════════════════════════════

Lines too large to read: ${oversized_lines[*]}

To search these lines, use:
Grep(pattern="your-search", path="$FILE", output_mode="content")

EOF
fi

cat >> "$OUTPUT_FILE" << EOF

STATUS: ✅ PRODUCTION READY - 100% VALIDATED
═══════════════════════════════════════════════════════════
EOF

echo ""
print_success "Commands saved to: $OUTPUT_FILE"
echo ""
print_header "READY TO USE"
echo ""
echo "Copy the SINGLE-LINE FORMAT above and use it to read your file!"
echo ""
