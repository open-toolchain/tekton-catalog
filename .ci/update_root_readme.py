#!/usr/bin/env python3
"""
Update root README.md with task summaries from all folders.

This script scans all task folders, extracts task information using generate_task_doc.py,
and updates the "# Tasks" section in the root README.md file.

Usage:
    python update_root_readme.py
    python update_root_readme.py --dry-run
"""

import argparse
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import yaml
import os

# Import the task documentation generator
try:
    from generate_task_doc import parse_task_yaml
except ImportError:
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    from generate_task_doc import parse_task_yaml


# Folder to category name mapping
FOLDER_CATEGORIES = {
    "cloudfoundry": "Cloud Foundry related tasks",
    "container-registry": "IBM Cloud Container Registry related tasks",
    "cra": "IBM Cloud Code Risk Analyzer scanners related tasks",
    "devops-insights": "IBM Cloud Devops Insights related tasks",
    "git": "Git related tasks",
    "kubernetes-service": "IBM Cloud Kubernetes Service related tasks",
    "linter": "Linter related tasks",
    "slack": "Slack related tasks",
    "sonarqube": "SonarQube related tasks",
    "tester": "Tester related tasks",
    "toolchain": "Open-Toolchain related tasks",
}

# Order of folders in the README
FOLDER_ORDER = [
    "cloudfoundry",
    "container-registry",
    "cra",
    "devops-insights",
    "git",
    "kubernetes-service",
    "linter",
    "slack",
    "sonarqube",
    "tester",
    "toolchain",
]


def is_task_deprecated(task_data: dict) -> bool:
    """Check if a task is marked as deprecated."""
    metadata = task_data.get('metadata', {})
    labels = metadata.get('labels', {})
    return labels.get('tekton.dev/deprecated') == 'true'


def find_task_files(folder: Path) -> List[Path]:
    """Find all task YAML files in a folder (excluding samples)."""
    task_files = []

    for file_path in folder.glob("task-*.yaml"):
        # Skip if in a sample directory
        if "sample" in str(file_path):
            continue

        # Check if it's a valid task
        try:
            task_data = parse_task_yaml(str(file_path))
            if task_data.get('kind') == 'Task':
                task_files.append(file_path)
        except Exception as e:
            print(f"Warning: Could not parse {file_path}: {e}", file=sys.stderr)

    return sorted(task_files)


def get_task_info(task_file: Path, folder_name: str) -> Optional[Dict]:
    """Extract task information from a task file."""
    try:
        task_data = parse_task_yaml(str(task_file))
        metadata = task_data.get('metadata', {})
        spec = task_data.get('spec', {})

        task_name = metadata.get('name', '')
        description = metadata.get('description', spec.get('description', ''))

        # Clean up description
        desc = ' '.join(description.strip().split())

        # Check if deprecated
        is_deprecated = is_task_deprecated(task_data)

        return {
            'name': task_name,
            'description': desc,
            'folder': folder_name,
            'deprecated': is_deprecated
        }
    except Exception as e:
        print(f"Error extracting info from {task_file}: {e}", file=sys.stderr)
        return None


def generate_folder_section(folder_name: str, repo_root: Path) -> str:
    """Generate the task list section for a specific folder."""
    folder_path = repo_root / folder_name

    if not folder_path.exists():
        return ""

    # Get category name
    category_name = FOLDER_CATEGORIES.get(folder_name, f"{folder_name} related tasks")

    # Find all task files
    task_files = find_task_files(folder_path)

    if not task_files:
        return ""

    # Generate section
    lines = [f"## {category_name}\n"]

    # Generate task entries
    for task_file in task_files:
        task_info = get_task_info(task_file, folder_name)
        if task_info:
            task_name = task_info['name']
            description = task_info['description']
            is_deprecated = task_info['deprecated']

            # Create link to folder README with anchor
            link = f"./{folder_name}/README.md#{task_name}"

            # Add deprecated marker if needed
            task_link = f"[{task_name}]({link})"
            if is_deprecated:
                task_link += " [deprecated]"

            lines.append(f"- **{task_link}**: {description}")

    return '\n'.join(lines) + '\n'


def update_root_readme(repo_root: Path, dry_run: bool = False, verbose: bool = False) -> bool:
    """
    Update the root README.md file with task summaries from all folders.

    Args:
        repo_root: Path to the repository root
        dry_run: If True, show what would be changed without modifying files
        verbose: If True, print detailed progress information

    Returns:
        True if successful, False otherwise
    """
    readme_path = repo_root / "README.md"

    if not readme_path.exists():
        print(f"Error: README.md not found in {repo_root}", file=sys.stderr)
        return False

    # Read existing README
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    # Generate task sections for all folders
    task_sections = []

    for folder_name in FOLDER_ORDER:
        if verbose:
            print(f"Processing folder: {folder_name}")

        section = generate_folder_section(folder_name, repo_root)
        if section:
            task_sections.append(section)
            if verbose:
                task_count = section.count('- **[')
                print(f"  Found {task_count} task(s)")

    # Combine all sections
    all_tasks_content = '\n'.join(task_sections)

    # Find the "# Tasks" section in the README
    lines = readme_content.split('\n')

    # Find the Tasks section
    tasks_section_idx = -1
    for i, line in enumerate(lines):
        if re.match(r'^#\s+Tasks\s*$', line):
            tasks_section_idx = i
            break

    if tasks_section_idx == -1:
        print("Error: Could not find '# Tasks' section in root README.md", file=sys.stderr)
        return False

    # Find the next major section (# heading)
    next_section_idx = len(lines)
    for i in range(tasks_section_idx + 1, len(lines)):
        if re.match(r'^#\s+', lines[i]) and not re.match(r'^##', lines[i]):
            next_section_idx = i
            break

    # Reconstruct the README
    before_tasks = '\n'.join(lines[:tasks_section_idx + 1])  # Include "# Tasks" heading
    after_tasks = '\n'.join(lines[next_section_idx:]) if next_section_idx < len(lines) else ""

    # Build new content
    parts = [before_tasks, "", all_tasks_content]
    if after_tasks:
        parts.append(after_tasks)

    new_content = '\n'.join(parts)

    if dry_run:
        print(f"\n" + "="*60)
        print("DRY RUN - Would update root README.md")
        print("="*60)
        print(f"Generated {len(task_sections)} category section(s)")
        print(f"Total content: {len(all_tasks_content)} chars")
        print("="*60)
        if verbose:
            print(f"\nPreview of Tasks section:")
            print(all_tasks_content[:1000])
            if len(all_tasks_content) > 1000:
                print("...")
        return True

    # Write updated README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\n✓ Successfully updated {readme_path}")
    print(f"  - Updated {len(task_sections)} category section(s)")
    total_tasks = sum(section.count('- **[') for section in task_sections)
    print(f"  - Total tasks documented: {total_tasks}")
    return True


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Update root README.md with task summaries from all folders.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update root README
  python update_root_readme.py

  # Dry run to see what would change
  python update_root_readme.py --dry-run

  # Verbose output
  python update_root_readme.py -v
        """
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be changed without modifying files')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Determine repository root (parent of .ci directory)
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    if args.verbose:
        print(f"Repository root: {repo_root}", file=sys.stderr)

    try:
        success = update_root_readme(repo_root, args.dry_run, args.verbose)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

# Made with Bob
