#!/bin/bash

# Interactive menu to read project plan files
# Created for Vinod R. Yellagonda - 30-Day Healthcare Application Plan

clear

echo "========================================="
echo "  30-DAY HEALTHCARE APPLICATION PLAN"
echo "  File Viewer Menu"
echo "========================================="
echo ""
echo "Choose a file to view:"
echo ""
echo "1. STEP_0_INDEX.md (Navigation Guide)"
echo "2. STEP_1_READ_THIS_FIRST.md (Strategy & Quick Start)"
echo "3. STEP_2_30_DAY_PLAN.md (Complete 30-Day Plan)"
echo "4. Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Opening STEP_0_INDEX.md..."
        echo "========================================="
        less STEP_0_INDEX.md
        ;;
    2)
        echo ""
        echo "Opening STEP_1_READ_THIS_FIRST.md..."
        echo "========================================="
        less STEP_1_READ_THIS_FIRST.md
        ;;
    3)
        echo ""
        echo "Opening STEP_2_30_DAY_PLAN.md..."
        echo "========================================="
        less STEP_2_30_DAY_PLAN.md
        ;;
    4)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run again and choose 1-4."
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "File viewing complete."
echo "Run ./READ_FILES.sh again to view another file."
echo "========================================="
