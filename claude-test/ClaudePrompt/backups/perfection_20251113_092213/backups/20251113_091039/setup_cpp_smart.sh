#!/bin/bash
################################################################################
# Setup Script for cpp_smart
# Makes it easy to install and use cpp_smart wrapper
################################################################################

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"
echo "  cpp_smart Setup - Intelligent CPP Command Tracking"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Choose installation method:"
echo ""
echo "  1. Create alias 'cpps' → cpp_smart (Recommended)"
echo "  2. Create alias 'cpp' → cpp_smart (Replaces cpp with smart version)"
echo "  3. Just use ./cpp_smart directly (No alias)"
echo "  4. Show usage examples"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}Creating alias 'cpps' for cpp_smart...${NC}"

        # Add to .bashrc
        if ! grep -q "alias cpps=" ~/.bashrc 2>/dev/null; then
            echo "alias cpps='$SCRIPT_DIR/cpp_smart'" >> ~/.bashrc
            echo -e "${GREEN}✅ Alias added to ~/.bashrc${NC}"
        else
            echo -e "${YELLOW}⚠️  Alias already exists in ~/.bashrc${NC}"
        fi

        # Make available in current session
        alias cpps="$SCRIPT_DIR/cpp_smart"

        echo ""
        echo -e "${GREEN}✅ Setup complete!${NC}"
        echo ""
        echo "Usage:"
        echo "  cpps \"Fix the login bug\" -v"
        echo "  cpps \"Explain async/await\" -v"
        echo ""
        echo "To use in current terminal:"
        echo "  source ~/.bashrc"
        echo ""
        ;;

    2)
        echo ""
        echo -e "${YELLOW}⚠️  WARNING: This will replace 'cpp' with cpp_smart${NC}"
        echo "Original cpp will still be available as './cpp'"
        echo ""
        read -p "Are you sure? [y/N]: " confirm

        if [[ $confirm =~ ^[Yy]$ ]]; then
            echo ""
            echo -e "${BLUE}Creating alias 'cpp' for cpp_smart...${NC}"

            # Backup existing alias if any
            if grep -q "alias cpp=" ~/.bashrc 2>/dev/null; then
                sed -i.bak '/alias cpp=/d' ~/.bashrc
                echo -e "${YELLOW}  Backed up old alias to ~/.bashrc.bak${NC}"
            fi

            # Add new alias
            echo "alias cpp='$SCRIPT_DIR/cpp_smart'" >> ~/.bashrc
            alias cpp="$SCRIPT_DIR/cpp_smart"

            echo -e "${GREEN}✅ Setup complete!${NC}"
            echo ""
            echo "Usage (now ALL cpp commands are tracked):"
            echo "  cpp \"Fix the login bug\" -v"
            echo "  cpp \"Add dark mode feature\" -v"
            echo ""
            echo "To use in current terminal:"
            echo "  source ~/.bashrc"
            echo ""
        else
            echo ""
            echo "Setup cancelled."
            echo ""
        fi
        ;;

    3)
        echo ""
        echo -e "${GREEN}✅ No alias needed!${NC}"
        echo ""
        echo "Usage:"
        echo "  ./cpp_smart \"Your prompt here\" -v"
        echo "  $SCRIPT_DIR/cpp_smart \"Your prompt here\" -v"
        echo ""
        ;;

    4)
        echo ""
        echo "════════════════════════════════════════════════════════════════════════════════"
        echo "  cpp_smart Usage Examples"
        echo "════════════════════════════════════════════════════════════════════════════════"
        echo ""
        echo "🐛 BUG FIXES (auto-detected):"
        echo "  ./cpp_smart \"Fix the login bug\" -v"
        echo "  ./cpp_smart \"Resolve timeout error\" -v"
        echo "  ./cpp_smart \"Debug the crash issue\" -v"
        echo ""
        echo "⭐ FEATURES (auto-detected):"
        echo "  ./cpp_smart \"Add dark mode feature\" -v"
        echo "  ./cpp_smart \"Implement user authentication\" -v"
        echo "  ./cpp_smart \"Create API endpoint\" -v"
        echo ""
        echo "🧪 TESTING (auto-detected):"
        echo "  ./cpp_smart \"Test the payment flow\" -v"
        echo "  ./cpp_smart \"Verify database connection\" -v"
        echo "  ./cpp_smart \"Validate user input\" -v"
        echo ""
        echo "📊 ANALYSIS (auto-detected):"
        echo "  ./cpp_smart \"Explain how async/await works\" -v"
        echo "  ./cpp_smart \"What is the difference between let and const?\" -v"
        echo "  ./cpp_smart \"How does the authentication system work?\" -v"
        echo ""
        echo "🔧 REFACTORING (auto-detected):"
        echo "  ./cpp_smart \"Refactor the auth module\" -v"
        echo "  ./cpp_smart \"Optimize database queries\" -v"
        echo "  ./cpp_smart \"Clean up the code\" -v"
        echo ""
        echo "📚 DOCUMENTATION (auto-detected):"
        echo "  ./cpp_smart \"Write README for the project\" -v"
        echo "  ./cpp_smart \"Document the API endpoints\" -v"
        echo "  ./cpp_smart \"Create user guide\" -v"
        echo ""
        echo "════════════════════════════════════════════════════════════════════════════════"
        echo ""
        ;;

    *)
        echo ""
        echo "Invalid choice. Exiting."
        echo ""
        exit 1
        ;;
esac

echo "Dashboard: http://localhost:8000/dashboard.html"
echo ""
