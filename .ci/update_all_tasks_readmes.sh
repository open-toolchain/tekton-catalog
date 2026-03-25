#!/usr/bin/env bash

# Update README.md files in all task folders
# This script iterates through all subfolders and invokes update_readme.py
# to regenerate the task documentation in each folder's README.md

set -e

# Get the script directory and repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to repository root
cd "$REPO_ROOT"

# Define the folders to process (same as in update_root_readme.py)
FOLDERS=(
    "cloudfoundry"
    "container-registry"
    "cra"
    "devops-insights"
    "git"
    "kubernetes-service"
    "linter"
    "signing/dct"
    "slack"
    "sonarqube"
    "tester"
    "toolchain"
)

echo "Updating README.md files in all task folders..."
echo ""

# Track success/failure
total_folders=0
successful_folders=0
failed_folders=0

# Process each folder
for folder in "${FOLDERS[@]}"; do
    if [ -d "$folder" ]; then
        total_folders=$((total_folders + 1))
        echo "Processing: $folder"

        if python3 "$SCRIPT_DIR/update_readme.py" \
          --summary-anchor-output "## Available tasks" \
          --details-anchor-output "## Details" \
          --output "$folder/README.md" \
          --file "$folder/*.y*ml"; then
            successful_folders=$((successful_folders + 1))
            echo "  ✓ Successfully updated $folder/README.md"
        else
            failed_folders=$((failed_folders + 1))
            echo "  ✗ Failed to update $folder/README.md"
        fi
        echo ""
    else
        echo "Skipping: $folder (directory not found)"
        echo ""
    fi
done

# Print summary
echo "=========================================="
echo "Summary:"
echo "  Total folders processed: $total_folders"
echo "  Successful: $successful_folders"
echo "  Failed: $failed_folders"
echo "=========================================="

# Exit with error if any folder failed
if [ $failed_folders -gt 0 ]; then
    exit 1
fi

exit 0

# Made with Bob
