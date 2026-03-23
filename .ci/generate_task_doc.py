#!/usr/bin/env python3
"""
Generate markdown documentation from Tekton task YAML files.

This script parses a Tekton task YAML file and generates markdown documentation
in a format similar to the README.md files in the tekton-catalog.

Usage:
    python generate_task_docs.py <task-file.yaml>
    python generate_task_docs.py <task-file.yaml> --output <output.md>
"""

import argparse
import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional


def parse_task_yaml(file_path: str) -> Dict[str, Any]:
    """Parse a Tekton task YAML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def format_param_description(description: str, default: Optional[str] = None) -> str:
    """Format parameter description with optional default value."""
    # Clean up multi-line descriptions
    desc = ' '.join(description.strip().split())

    if default is not None and default != "":
        desc += f" (default to `{default}`)"

    return desc


def generate_parameters_section(params: List[Dict[str, Any]], heading_prefix: str = "###") -> str:
    """Generate the Parameters section of the documentation."""
    if not params:
        return ""

    lines = [f"{heading_prefix} Parameters\n"]

    for param in params:
        name = param.get('name', '')
        description = param.get('description', '')
        default = param.get('default')

        # Determine if parameter is optional
        is_optional = default is not None or '(optional)' in description.lower()

        formatted_desc = format_param_description(description, default)
        lines.append(f"* **{name}**: {formatted_desc}")

    return '\n'.join(lines) + '\n'


def generate_workspaces_section(workspaces: List[Dict[str, Any]], heading_prefix: str = "###") -> str:
    """Generate the Workspaces section of the documentation."""
    if not workspaces:
        return ""

    lines = [f"{heading_prefix} Workspaces\n"]

    for workspace in workspaces:
        name = workspace.get('name', '')
        description = workspace.get('description', '')

        # Clean up multi-line descriptions
        desc = ' '.join(description.strip().split())

        lines.append(f"* **{name}**: {desc}")

    return '\n'.join(lines) + '\n'


def generate_results_section(results: List[Dict[str, Any]], heading_prefix: str = "###") -> str:
    """Generate the Results section of the documentation."""
    if not results:
        return ""

    lines = [f"{heading_prefix} Results"]

    for result in results:
        name = result.get('name', '')
        description = result.get('description', '')

        # Clean up multi-line descriptions
        desc = ' '.join(description.strip().split())

        lines.append(f"* **{name}**: {desc}")

    return '\n'.join(lines) + '\n'


def extract_secret_refs_from_env(env_vars: List[Dict[str, Any]], secret_refs: List[Dict[str, str]]) -> None:
    """
    Extract secretKeyRef references from environment variables.
    Updates secret_refs list in place.
    """
    for env_var in env_vars:
        value_from = env_var.get('valueFrom', {})
        secret_key_ref = value_from.get('secretKeyRef', {})

        if secret_key_ref:
            name_ref = secret_key_ref.get('name', '')
            key_ref = secret_key_ref.get('key', '')

            # Extract parameter names from $(params.xxx) format
            name_param = None
            key_param = None

            if name_ref.startswith('$(params.') and name_ref.endswith(')'):
                name_param = name_ref[9:-1]  # Extract 'xxx' from '$(params.xxx)'

            if key_ref.startswith('$(params.') and key_ref.endswith(')'):
                key_param = key_ref[9:-1]

            if name_param and key_param:
                # Check if we already have this secret reference
                existing = next((s for s in secret_refs if s['name_param'] == name_param), None)
                if existing:
                    if key_param not in existing['key_params']:
                        existing['key_params'].append(key_param)
                else:
                    secret_refs.append({
                        'name_param': name_param,
                        'key_params': [key_param]
                    })


def extract_secret_refs_from_spec(spec: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Extract secretKeyRef references from task spec (both stepTemplate and steps).
    Returns list of dicts with 'name_param' and 'key_params' extracted from $(params.xxx) references.
    """
    secret_refs = []

    # Check stepTemplate.env
    step_template = spec.get('stepTemplate', {})
    if step_template:
        env_vars = step_template.get('env', [])
        extract_secret_refs_from_env(env_vars, secret_refs)

    # Check each step's env
    steps = spec.get('steps', [])
    for step in steps:
        env_vars = step.get('env', [])
        extract_secret_refs_from_env(env_vars, secret_refs)

    return secret_refs


def generate_context_section(params: List[Dict[str, Any]], spec: Dict[str, Any], heading_prefix: str = "###") -> str:
    """
    Generate Context - ConfigMap/Secret section by analyzing secretKeyRef usage in stepTemplate and steps.
    """
    secret_refs = extract_secret_refs_from_spec(spec)

    if not secret_refs:
        return ""

    # Create a parameter lookup dict
    param_dict = {p.get('name'): p for p in params}

    lines = [f"{heading_prefix} Context - ConfigMap/Secret\n"]
    lines.append(f"  The task may rely on the following kubernetes resources to be defined:\n")

    # Process each secret reference found in steps
    for secret_ref in secret_refs:
        name_param = secret_ref['name_param']
        key_params = secret_ref['key_params']

        # Get the secret name parameter details
        secret_param = param_dict.get(name_param)
        if not secret_param:
            continue

        secret_default = secret_param.get('default', '')
        secret_description = secret_param.get('description', '')

        # Display secret name
        if secret_default:
            lines.append(f"* **Secret {secret_default}**")
        else:
            lines.append(f"* **Secret** (name configured via `{name_param}` parameter)")

        if secret_description:
            desc = ' '.join(secret_description.strip().split())
            lines.append(f"  {desc}")

        lines.append("")

        # Display secret keys
        if key_params:
            lines.append("  Secret containing:")
            for key_param_name in key_params:
                key_param = param_dict.get(key_param_name)
                if key_param:
                    key_default = key_param.get('default', '')
                    key_description = key_param.get('description', '')

                    if key_default:
                        desc = ' '.join(key_description.strip().split()) if key_description else ''
                        lines.append(f"  * **{key_default}**: {desc}")

        lines.append("")

    lines.append("Note: secret name and secret key(s) can be configured using Task's params.")
    return '\n'.join(lines)


def generate_markdown(task_data: Dict[str, Any], task_file: str, heading_level: int = 2) -> str:
    """Generate complete markdown documentation from task data."""
    metadata = task_data.get('metadata', {})
    spec = task_data.get('spec', {})

    task_name = metadata.get('name', 'unknown-task')
    annotations = metadata.get('annotations', {})
    labels = metadata.get('labels', {})
    display_name = annotations.get('tekton.dev/displayName', '')
    description = metadata.get('description', spec.get('description', f'{task_name} task'))

    # Check if task is deprecated
    is_deprecated = labels.get('tekton.dev/deprecated') == 'true'

    # Generate heading prefix based on level
    heading_prefix = '#' * heading_level
    subheading_prefix = '#' * (heading_level + 1)

    # Start with the main heading, add deprecated indicator if needed
    heading = f"{heading_prefix} {task_name}"
    if is_deprecated:
        heading += " [deprecated]"
    lines = [f"{heading}\n"]

    # Add display name if available
    if display_name:
        lines.append(f"{display_name}\n")

    lines.append(f"{description}\n")

    # Add Context section if applicable
    params = spec.get('params', [])
    context_section = generate_context_section(params, spec, subheading_prefix)
    if context_section:
        lines.append(context_section)

    # Add Parameters section
    params_section = generate_parameters_section(params, subheading_prefix)
    if params_section:
        lines.append(params_section)

    # Add Workspaces section
    workspaces = spec.get('workspaces', [])
    workspaces_section = generate_workspaces_section(workspaces, subheading_prefix)
    if workspaces_section:
        lines.append(workspaces_section)

    # Add Results section
    results = spec.get('results', [])
    results_section = generate_results_section(results, subheading_prefix)
    if results_section:
        lines.append(results_section)

    result = '\n'.join(lines)
    # Ensure single trailing newline using OS-specific line ending
    result = result.rstrip('\n') + '\n'
    return result


def generate_task_doc_from_file(task_file: str, heading_level: int = 2) -> str:
    """
    Generate markdown documentation from a task file.

    Args:
        task_file: Path to the Tekton task YAML file
        heading_level: Initial heading level (1-6)

    Returns:
        Generated markdown documentation as a string

    Raises:
        FileNotFoundError: If task file doesn't exist
        yaml.YAMLError: If YAML parsing fails
        ValueError: If heading level is invalid
    """
    task_path = Path(task_file)
    if not task_path.exists():
        raise FileNotFoundError(f"File '{task_file}' not found.")

    if heading_level < 1 or heading_level > 6:
        raise ValueError("Heading level must be between 1 and 6.")

    task_data = parse_task_yaml(task_file)
    return generate_markdown(task_data, task_file, heading_level)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Generate markdown documentation from Tekton task YAML files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_task_doc.py task-clone-repo.yaml
  python generate_task_doc.py task-clone-repo.yaml --output docs.md
  python generate_task_doc.py task-clone-repo.yaml --heading-level 3
  python generate_task_doc.py ../git/task-clone-repo.yaml -l 1 -o output.md
        """
    )
    parser.add_argument('task_file', help='Path to the Tekton task YAML file')
    parser.add_argument('-o', '--output', help='Output markdown file (default: stdout)')
    parser.add_argument('-l', '--heading-level', type=int, default=2,
                        help='Initial heading level (default: 2 for ##)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if args.verbose:
        print(f"Parsing task file: {args.task_file}", file=sys.stderr)

    try:
        # Generate markdown using the public function
        markdown = generate_task_doc_from_file(args.task_file, args.heading_level)

        # Output the result
        if args.output:
            with open(args.output, 'w', encoding='utf-8', newline='') as f:
                f.write(markdown)
            if args.verbose:
                print(f"Documentation written to: {args.output}", file=sys.stderr)
        else:
            print(markdown)

        if args.verbose:
            print("Documentation generated successfully!", file=sys.stderr)

    except (FileNotFoundError, yaml.YAMLError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

# Made with Bob
