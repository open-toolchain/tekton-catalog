#!/usr/bin/env python3
"""
Update README.md files with generated task documentation.

This script processes Tekton task YAML files specified via --file parameters
(supporting glob patterns) and updates the README.md file by replacing the
task documentation sections.

Usage:
    python update_readme.py --file git/*.yaml
    python update_readme.py --file git/task-*.yaml --file container-registry/task-*.yaml
    python update_readme.py -f "git/*.yaml" -f "container-registry/*.yaml" --dry-run
"""

import argparse
import sys
import re
from pathlib import Path
from typing import List, Optional
import yaml
import os
import glob

# Import the task documentation generator
try:
    from generate_task_doc import generate_task_doc_from_file, parse_task_yaml
except ImportError:
    # If running from a different directory, try to import from .ci
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    from generate_task_doc import generate_task_doc_from_file, parse_task_yaml


def resolve_file_patterns(patterns: List[str], base_dir: Optional[Path] = None) -> List[Path]:
    """
    Resolve file patterns (including globs) to actual file paths.

    Args:
        patterns: List of file patterns (can include glob patterns like *.yaml)
        base_dir: Base directory to resolve relative paths from

    Returns:
        Sorted list of resolved file paths
    """
    resolved_files = []

    for pattern in patterns:
        pattern_path = Path(pattern)

        # If pattern is not absolute, resolve from base_dir
        if not pattern_path.is_absolute() and base_dir:
            pattern = str(base_dir / pattern)

        # Expand glob pattern
        matched_files = glob.glob(pattern, recursive=True)

        if not matched_files:
            print(f"Warning: No files matched pattern '{pattern}'", file=sys.stderr)
            continue

        for file_path in matched_files:
            path = Path(file_path)

            # Skip if in a sample directory
            if "sample" in str(path):
                continue

            # Check if it's a valid task file
            try:
                task_data = parse_task_yaml(str(path))
                if task_data.get('kind') == 'Task':
                    resolved_files.append(path)
            except Exception as e:
                print(f"Warning: Could not parse {path}: {e}", file=sys.stderr)

    return sorted(set(resolved_files))  # Remove duplicates and sort


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


def update_readme(task_files: List[Path], dry_run: bool = False, verbose: bool = False, output_file: Optional[Path] = None, details_anchor_heading: str = "## Tasks", summary_anchor_heading: Optional[str] = None) -> bool:
    """
    Update the README.md file with generated task documentation.

    Args:
        task_files: List of task file paths to process
        dry_run: If True, show what would be changed without modifying files
        verbose: If True, print detailed progress information
        output_file: Path to the README.md file to update (required)
        details_anchor_heading: The heading to use for inserting detailed task documentation (default: "## Tasks")
        summary_anchor_heading: Optional heading to use for inserting task list summary. If not provided, summary is placed with details.

    Returns:
        True if successful, False otherwise
    """
    if not output_file:
        print(f"Error: --output parameter is required to specify README.md location", file=sys.stderr)
        return False

    readme_path = output_file

    if not readme_path.exists():
        print(f"Error: README.md not found at {readme_path}", file=sys.stderr)
        return False

    if not task_files:
        print(f"Error: No task files provided", file=sys.stderr)
        return False

    print(f"Found {len(task_files)} task file(s)")
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

    # Check if both anchors are the same
    anchors_are_same = (summary_anchor_heading and
                       summary_anchor_heading.strip().lower() == details_anchor_heading.strip().lower())

    if anchors_are_same:
        # When both anchors are the same, combine summary and details in one section
        combined_content = task_list + '\n' + all_task_docs
        new_content, found = replace_section_content(readme_content, details_anchor_heading, combined_content)

        if not found:
            print(f"Warning: Could not find anchor heading '{details_anchor_heading}' in README.md", file=sys.stderr)
            print("Appending task documentation to the end of the file", file=sys.stderr)
            new_content = readme_content + f"\n\n{details_anchor_heading}\n\n" + combined_content
    else:
        # Process summary anchor if provided and different from details anchor
        if summary_anchor_heading:
            readme_content, summary_found = replace_section_content(readme_content, summary_anchor_heading, task_list)
            if not summary_found:
                print(f"Warning: Could not find summary anchor heading '{summary_anchor_heading}' in README.md", file=sys.stderr)

        # Process details anchor
        # If summary anchor is provided (and different), only insert details; otherwise insert both
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
  # Process all YAML files in git folder
  python update_readme.py --file "git/*.yaml" --output git/README.md

  # Process specific task files
  python update_readme.py -f git/task-clone-repo.yaml -f git/task-set-commit-status.yaml -o git/README.md

  # Process multiple folders with glob patterns
  python update_readme.py -f "git/task-*.yaml" -f "container-registry/task-*.yaml" -o README.md

  # Dry run to see what would change
  python update_readme.py -f "git/*.yaml" -o git/README.md --dry-run

  # Verbose output
  python update_readme.py -f "git/*.yaml" -o git/README.md -v

  # Use absolute paths
  python update_readme.py -f "/path/to/tekton-catalog/git/*.yaml" -o /path/to/custom/README.md

  # Use custom anchor headings
  python update_readme.py -f "git/*.yaml" -o git/README.md --details-anchor-output "# Available Tasks"

  # Separate summary and details sections
  python update_readme.py -f "git/*.yaml" -o git/README.md --summary-anchor-output "## Task List" --details-anchor-output "## Task Details"
        """
    )
    parser.add_argument('-f', '--file', action='append', required=True, dest='files',
                        help='Task file or glob pattern (can be used multiple times). Examples: "git/*.yaml", "git/task-clone-repo.yaml"')
    parser.add_argument('-o', '--output', required=True,
                        help='Path to the README.md file to update')
    parser.add_argument('--details-anchor-output', default='## Tasks',
                        help='Heading to use for inserting detailed task documentation (default: "## Tasks")')
    parser.add_argument('--summary-anchor-output', default=None,
                        help='Optional heading to use for inserting task list summary. If not provided, summary is placed with details.')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be changed without modifying files')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Determine base directory for resolving relative paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Resolve file patterns to actual task files
    if args.verbose:
        print(f"Resolving file patterns: {args.files}", file=sys.stderr)

    task_files = resolve_file_patterns(args.files, repo_root)

    if not task_files:
        print(f"Error: No valid task files found matching the provided patterns", file=sys.stderr)
        sys.exit(1)

    # Handle output file path
    output_path = Path(args.output)
    if not output_path.is_absolute():
        # Resolve relative to current working directory
        output_path = Path.cwd() / args.output

    if args.verbose:
        print(f"Processing {len(task_files)} task file(s):", file=sys.stderr)
        for task_file in task_files:
            print(f"  - {task_file}", file=sys.stderr)
        print(f"Output README.md: {output_path}", file=sys.stderr)
        print(f"Details anchor heading: {args.details_anchor_output}", file=sys.stderr)
        if args.summary_anchor_output:
            print(f"Summary anchor heading: {args.summary_anchor_output}", file=sys.stderr)

    try:
        success = update_readme(task_files, args.dry_run, args.verbose, output_path, args.details_anchor_output, args.summary_anchor_output)
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
