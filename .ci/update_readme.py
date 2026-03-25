#!/usr/bin/env python3
"""
Update README.md files with generated task documentation.

This script finds all Tekton task YAML files in a given folder and updates
the README.md file by replacing the task documentation sections.

Usage:
    python update_readme.py <folder>
    python update_readme.py git
    python update_readme.py container-registry --dry-run
"""

import argparse
import sys
import re
from pathlib import Path
from typing import List, Optional
import yaml
import os

# Import the task documentation generator
try:
    from generate_task_doc import generate_task_doc_from_file, parse_task_yaml
except ImportError:
    # If running from a different directory, try to import from .ci
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    from generate_task_doc import generate_task_doc_from_file, parse_task_yaml


def find_task_files(folder: Path) -> List[Path]:
    """Find all task YAML files in a folder (excluding samples)."""
    task_files = []

    for file_path in folder.glob("*.y*ml"):
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


def generate_task_list_section(task_files: List[Path]) -> str:
    """Generate the task list section at the top of the tasks documentation."""
    if not task_files:
        return ""

    lines = []
    for task_file in task_files:
        try:
            task_data = parse_task_yaml(str(task_file))
            metadata = task_data.get('metadata', {})
            spec = task_data.get('spec', {})
            labels = metadata.get('labels', {})
            task_name = metadata.get('name', '')
            description = metadata.get('description', spec.get('description', ''))

            # Check if task is deprecated
            is_deprecated = labels.get('tekton.dev/deprecated') == 'true'

            # Clean up description for the list
            desc = ' '.join(description.strip().split())

            # Add deprecated indicator if needed
            task_link = f"[{task_name}](#{task_name})"
            if is_deprecated:
                task_link += " [deprecated]"

            lines.append(f"- **{task_link}**: {desc}")
        except Exception as e:
            print(f"Warning: Could not process {task_file}: {e}", file=sys.stderr)

    return '\n'.join(lines) + '\n'


def update_readme(folder: Path, dry_run: bool = False, verbose: bool = False, output_file: Optional[Path] = None, details_anchor_heading: str = "## Tasks", summary_anchor_heading: Optional[str] = None) -> bool:
    """
    Update the README.md file in the given folder with generated task documentation.

    Args:
        folder: Path to the folder containing task files and README.md
        dry_run: If True, show what would be changed without modifying files
        verbose: If True, print detailed progress information
        output_file: Optional custom path for the README.md file to update
        details_anchor_heading: The heading to use for inserting detailed task documentation (default: "## Tasks")
        summary_anchor_heading: Optional heading to use for inserting task list summary. If not provided, summary is placed with details.

    Returns:
        True if successful, False otherwise
    """
    readme_path = output_file if output_file else folder / "README.md"

    if not readme_path.exists():
        print(f"Error: README.md not found in {folder}", file=sys.stderr)
        return False

    # Find all task files
    task_files = find_task_files(folder)

    if not task_files:
        print(f"No task files found in {folder}", file=sys.stderr)
        return False

    print(f"Found {len(task_files)} task file(s) in {folder}")
    if verbose:
        for task_file in task_files:
            print(f"  - {task_file.name}")

    # Read existing README
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    # Generate task list section (summary at the top)
    task_list = generate_task_list_section(task_files)

    # Calculate heading level for task documentation based on details_anchor_heading
    # Extract the heading level from details_anchor_heading (e.g., "## Tasks" -> 2)
    anchor_match = re.match(r'^(#+)\s+', details_anchor_heading.strip())
    if anchor_match:
        anchor_level = len(anchor_match.group(1))
        # Task sections should be one level deeper than the anchor heading
        task_heading_level = anchor_level + 1
    else:
        # Default to level 3 if anchor heading format is invalid
        task_heading_level = 3

    # Generate detailed documentation for each task using generate_task_doc
    task_docs = []
    for task_file in task_files:
        try:
            if verbose:
                print(f"Generating documentation for {task_file.name}...")
            # Use calculated heading level for task sections
            doc = generate_task_doc_from_file(str(task_file), heading_level=task_heading_level)
            task_docs.append(doc)
        except Exception as e:
            print(f"Error generating docs for {task_file}: {e}", file=sys.stderr)

    # Combine all task documentation
    all_task_docs = '\n'.join(task_docs)

    # Helper function to replace content under a heading
    def replace_section_content(content: str, anchor_heading: str, new_content: str) -> tuple[str, bool]:
        """Replace content under a heading anchor. Returns (new_content, found)."""
        lines = content.split('\n')

        # Parse the anchor heading to determine level and text
        anchor_match = re.match(r'^(#+)\s+(.+)$', anchor_heading.strip())
        if not anchor_match:
            print(f"Error: Invalid anchor heading format: '{anchor_heading}'", file=sys.stderr)
            print("Expected format: '# Heading' or '## Heading' etc.", file=sys.stderr)
            return content, False

        anchor_level = len(anchor_match.group(1))
        anchor_text = anchor_match.group(2).strip()

        # Find the anchor heading in the content
        section_idx = -1
        for i, line in enumerate(lines):
            line_match = re.match(r'^(#+)\s+(.+)$', line.strip())
            if line_match:
                line_level = len(line_match.group(1))
                line_text = line_match.group(2).strip()
                if line_level == anchor_level and line_text.lower() == anchor_text.lower():
                    section_idx = i
                    break

        if section_idx == -1:
            return content, False

        # Find the end of the section (next heading of same or higher level)
        end_section_idx = len(lines)
        for i in range(section_idx + 1, len(lines)):
            line_match = re.match(r'^(#+)\s+(.+)$', lines[i].strip())
            if line_match:
                line_level = len(line_match.group(1))
                # Stop at any heading of same or higher level (lower number = higher level)
                if line_level <= anchor_level:
                    end_section_idx = i
                    break

        # Reconstruct content
        before_section = '\n'.join(lines[:section_idx + 1])
        after_section = '\n'.join(lines[end_section_idx:]) if end_section_idx < len(lines) else ""

        parts = [before_section, new_content]
        if after_section:
            parts.append(after_section)

        return '\n'.join(parts), True

    # Process summary anchor if provided
    if summary_anchor_heading:
        readme_content, summary_found = replace_section_content(readme_content, summary_anchor_heading, task_list)
        if not summary_found:
            print(f"Warning: Could not find summary anchor heading '{summary_anchor_heading}' in README.md", file=sys.stderr)

    # Process details anchor
    # If summary anchor is provided, only insert details; otherwise insert both
    details_content = all_task_docs if summary_anchor_heading else task_list + '\n' + all_task_docs
    new_content, details_found = replace_section_content(readme_content, details_anchor_heading, details_content)

    if not details_found:
        print(f"Warning: Could not find details anchor heading '{details_anchor_heading}' in README.md", file=sys.stderr)
        print("Appending task documentation to the end of the file", file=sys.stderr)
        new_content = readme_content + f"\n\n{details_anchor_heading}\n\n" + details_content

    if dry_run:
        print('\n' + "="*60)
        print("DRY RUN - Would update README.md")
        print("="*60)
        print(f"Task list section ({len(task_list)} chars)")
        print(f"Task documentation ({len(all_task_docs)} chars)")
        print(f"Total new content: {len(new_content)} chars")
        print("="*60)
        if verbose:
            print(f"\nPreview (first 1000 chars):")
            print(new_content[:1000])
            print("...")
        return True

    # Write updated README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\n✓ Successfully updated {readme_path}")
    print(f"  - Updated {len(task_files)} task documentation section(s)")
    return True


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Update README.md with generated task documentation.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update git folder README
  python update_readme.py git

  # Dry run to see what would change
  python update_readme.py container-registry --dry-run

  # Verbose output
  python update_readme.py git -v

  # Use absolute path
  python update_readme.py /path/to/tekton-catalog/git

  # Specify custom README.md location
  python update_readme.py git --output /path/to/custom/README.md
  python update_readme.py git -o ../docs/git-tasks.md

  # Use custom anchor headings
  python update_readme.py git --details-anchor-output "# Available Tasks"
  python update_readme.py git --details-anchor-output "### Task Documentation"

  # Separate summary and details sections
  python update_readme.py git --summary-anchor-output "## Task List" --details-anchor-output "## Task Details"
        """
    )
    parser.add_argument('folder', help='Folder containing task files and README.md')
    parser.add_argument('-o', '--output', help='Custom path to the README.md file to update (default: <folder>/README.md)')
    parser.add_argument('--details-anchor-output', default='## Tasks',
                        help='Heading to use for inserting detailed task documentation (default: "## Tasks")')
    parser.add_argument('--summary-anchor-output', default=None,
                        help='Optional heading to use for inserting task list summary. If not provided, summary is placed with details.')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be changed without modifying files')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Resolve folder path
    folder_path = Path(args.folder)
    if not folder_path.is_absolute():
        # If relative path, resolve from script location's parent (repo root)
        script_dir = Path(__file__).parent
        repo_root = script_dir.parent
        folder_path = repo_root / args.folder

    if not folder_path.exists():
        print(f"Error: Folder '{args.folder}' not found.", file=sys.stderr)
        sys.exit(1)

    if not folder_path.is_dir():
        print(f"Error: '{args.folder}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Handle output file path
    output_path = None
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            # Resolve relative to current working directory
            output_path = Path.cwd() / args.output

    if args.verbose:
        print(f"Processing folder: {folder_path}", file=sys.stderr)
        if output_path:
            print(f"Output README.md: {output_path}", file=sys.stderr)
        print(f"Details anchor heading: {args.details_anchor_output}", file=sys.stderr)
        if args.summary_anchor_output:
            print(f"Summary anchor heading: {args.summary_anchor_output}", file=sys.stderr)

    try:
        success = update_readme(folder_path, args.dry_run, args.verbose, output_path, args.details_anchor_output, args.summary_anchor_output)
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
