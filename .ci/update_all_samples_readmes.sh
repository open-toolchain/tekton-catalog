#!/usr/bin/env bash

# Update README.md files in all sample folders
# This script finds all sample folders containing Pipeline/TriggerTemplate YAML files
# and a README.md, then invokes generate_pipeline_doc.py to update the documentation

set -e

# Get the script directory and repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to repository root
cd "$REPO_ROOT"

echo "Updating README.md files in all sample folders..."
echo ""

# Track success/failure
total_samples=0
successful_samples=0
failed_samples=0

# Define mapping of sample folders to task folders
# Key: sample folder path (relative to repo root)
# Value: space-separated list of folders containing tasks
declare -A SAMPLE_TASK_FOLDERS=(
    ["container-registry/sample"]="git container-registry"
    ["container-registry/sample-cr-build"]="git container-registry"
    ["container-registry/sample-docker-dind-sidecar"]="git container-registry"
    ["container-registry/sample-docker-dind-cluster"]="git container-registry"
    ["git/sample"]="git"
    ["git/sample-git-trigger"]="git"
    ["git/sample-git-pr-status"]="git"
    ["git/sample-set-commit-status"]="git"
    ["git/sample-skip-ci"]="git"
    ["kubernetes-service/sample"]="git kubernetes-service container-registry"
    ["devops-insights/sample"]="git devops-insights"
    ["slack/sample"]="slack"
    ["cra/sample"]="git cra"
    ["cra/sample-cra-ci"]="git cra"
    ["cra/sample-v2"]="git cra"
    ["sonarqube/sample"]="git sonarqube"
)

# Find all sample directories
while IFS= read -r -d '' sample_dir; do
    # Check if README.md exists
    if [ ! -f "$sample_dir/README.md" ]; then
        continue
    fi

    # Find all YAML files and check if they contain Pipeline, TriggerTemplate, EventListener, or Task
    pipeline_files=()
    task_files=()

    # shellcheck disable=SC2044
    for file in $(find "$sample_dir" -maxdepth 1 -type f -name "*.yaml"); do
        # Check if the file contains any document with kind: Pipeline, TriggerTemplate, EventListener, or Task
        # Using yq ea (evaluate all) to handle multi-document YAML files
        kinds=$(yq ea '.kind' "$file" 2>/dev/null)

        # Check if any of the kinds match Pipeline, TriggerTemplate, or EventListener
        if echo "$kinds" | grep -qE '^(Pipeline|TriggerTemplate|EventListener)$'; then
            pipeline_files+=("$file")
        fi
    done

    # Get task folders from the mapping
    sample_key="${sample_dir#./}"  # Remove leading ./
    task_folders_str="${SAMPLE_TASK_FOLDERS[$sample_key]}"

    # Convert space-separated string to array
    task_folders=()
    if [ -n "$task_folders_str" ]; then
        read -ra task_folders <<< "$task_folders_str"
    fi

    # Look for Task files in the mapped folders
    for folder in "${task_folders[@]}"; do
        # Convert relative path to absolute from repo root
        folder_path="$REPO_ROOT/$folder"
        if [ -d "$folder_path" ]; then
            for file in "$folder_path"/*.yaml; do
                if [ -f "$file" ]; then
                    kinds=$(yq ea '.kind' "$file" 2>/dev/null)
                    if echo "$kinds" | grep -qE '^Task$'; then
                        task_files+=("$file")
                    fi
                fi
            done
        fi
    done

    # Skip if no pipeline/trigger template files found
    if [ ${#pipeline_files[@]} -eq 0 ]; then
        continue
    fi

    total_samples=$((total_samples + 1))
    echo "Processing: $sample_dir"
    echo "  Found ${#pipeline_files[@]} file(s) with Pipeline/TriggerTemplate/EventListener"
    if [ ${#task_folders[@]} -gt 0 ]; then
        echo "  Task folders from README: ${task_folders[*]}"
    fi
    echo "  Found ${#task_files[@]} Task file(s)"

    # Build the command with all YAML files
    cmd_args=()
    for file in "${pipeline_files[@]}"; do
        cmd_args+=("--file" "$file")
    done

    # Add Task files
    for file in "${task_files[@]}"; do
        cmd_args+=("--file" "$file")
    done

    # Add output and anchor options
    cmd_args+=("--output" "$sample_dir/README.md")
    cmd_args+=("--anchor-output" "## Detailed Description")

    # Execute the command
    if python3 "$SCRIPT_DIR/generate_pipeline_doc.py" "${cmd_args[@]}"; then
        successful_samples=$((successful_samples + 1))
        echo "  ✓ Successfully updated $sample_dir/README.md"
    else
        failed_samples=$((failed_samples + 1))
        echo "  ✗ Failed to update $sample_dir/README.md"
    fi
    echo ""

done < <(find . -type d -name "*sample*" -print0 2>/dev/null)

# Print summary
echo "=========================================="
echo "Summary:"
echo "  Total sample folders processed: $total_samples"
echo "  Successful: $successful_samples"
echo "  Failed: $failed_samples"
echo "=========================================="

# Exit with error if any sample failed
if [ $failed_samples -gt 0 ]; then
    exit 1
fi

exit 0

# Made with Bob
