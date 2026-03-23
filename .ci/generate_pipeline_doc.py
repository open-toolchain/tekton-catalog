#!/usr/bin/env python3
"""
Generate markdown documentation for Tekton EventListener, Pipeline and TriggerTemplate parameters.

This script parses YAML files containing Tekton resources and generates markdown documentation
showing all parameters with their descriptions and defaults. When EventListener resources are
present, it generates per-EventListener documentation by following trigger references through
TriggerBindings and TriggerTemplates to the referenced Pipeline.

Usage:
    # Print to stdout (EventListener-based documentation)
    python generate_pipeline_doc.py --file listener.yaml --file pipeline.yaml

    # Save to new file
    python generate_pipeline_doc.py -f listener.yaml -f pipeline.yaml --output PARAMETERS.md

    # Insert at anchor in existing file
    python generate_pipeline_doc.py -f listener.yaml -f pipeline.yaml --output README.md --anchor-output "## Parameters"

    # Short form with all options
    python generate_pipeline_doc.py -f *.yaml -o README.md -a "## Parameters" -v

Options:
    --file, -f              Path to YAML file (can be used multiple times)
    --output, -o            Output markdown file (default: stdout)
    --anchor-output, -a     Heading anchor where content should be inserted (requires --output and existing file)
    --verbose, -v           Enable verbose output

Features:
    - EventListener-centric documentation: When EventListeners are found, generates separate
      parameter documentation for each EventListener showing the complete parameter flow
    - Automatic reference resolution: Follows trigger references from EventListener through
      TriggerBinding and TriggerTemplate to the referenced Pipeline
    - Parameter merging: Intelligently merges parameters from all sources with proper precedence
      (TriggerBinding values > TriggerTemplate defaults > Pipeline defaults)
    - Fallback mode: When no EventListeners are present, generates combined documentation
      for all Pipeline and TriggerTemplate resources (legacy behavior)
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml


def parse_yaml_file(file_path: Path) -> List[Dict]:
    """Parse a YAML file and return all documents."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            documents = list(yaml.safe_load_all(f))
        return documents
    except Exception as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        return []


def extract_pipeline_params(pipeline_doc: Dict) -> List[Dict]:
    """Extract parameters from a Pipeline document."""
    params = []

    if pipeline_doc.get('kind') != 'Pipeline':
        return params

    spec = pipeline_doc.get('spec', {})
    param_list = spec.get('params', [])

    # Handle case where params is None (empty in YAML)
    if param_list is None:
        param_list = []

    for param in param_list:
        params.append({
            'name': param.get('name', ''),
            'description': param.get('description', ''),
            'default': param.get('default', ''),
            'type': param.get('type', 'string'),
            'source': 'Pipeline'
        })

    return params


def extract_trigger_template_params(trigger_doc: Dict) -> List[Dict]:
    """Extract parameters from a TriggerTemplate document."""
    params = []

    if trigger_doc.get('kind') != 'TriggerTemplate':
        return params

    spec = trigger_doc.get('spec', {})
    param_list = spec.get('params', [])

    # Handle case where params is None (empty in YAML)
    if param_list is None:
        param_list = []

    for param in param_list:
        params.append({
            'name': param.get('name', ''),
            'description': param.get('description', ''),
            'default': param.get('default', ''),
            'type': param.get('type', 'string'),
            'source': 'TriggerTemplate'
        })

    return params


def extract_trigger_binding_params(binding_doc: Dict) -> List[Dict]:
    """Extract parameters from a TriggerBinding document."""
    params = []

    if binding_doc.get('kind') != 'TriggerBinding':
        return params

    spec = binding_doc.get('spec', {})
    param_list = spec.get('params', [])

    # Handle case where params is None (empty in YAML)
    if param_list is None:
        param_list = []

    for param in param_list:
        params.append({
            'name': param.get('name', ''),
            'value': param.get('value', ''),
            'source': 'TriggerBinding'
        })

    return params


def extract_task_environment_properties(task_doc: Dict) -> List[Dict]:
    """Extract environment properties from a Task document's stepTemplate and steps.
    Only extracts env entries that have valueFrom.secretKeyRef.
    Resolves the property name and description from the parameter referenced in the key field."""
    env_props = []

    if task_doc.get('kind') != 'Task':
        return env_props

    spec = task_doc.get('spec', {})

    # Build a map of parameter names to their default values and descriptions
    param_info = {}
    params = spec.get('params', [])
    if params:
        for param in params:
            param_name = param.get('name', '')
            param_default = param.get('default', '')
            param_description = param.get('description', '')
            if param_name:
                param_info[param_name] = {
                    'default': param_default,
                    'description': param_description
                }

    def resolve_property_info(secret_key: str) -> tuple:
        """Resolve the property name and description from a secret key that may reference a parameter."""
        # Check if secret_key references a parameter like $(params.xxx)
        import re
        param_match = re.match(r'\$\(params\.([^)]+)\)', secret_key)
        if param_match:
            param_name = param_match.group(1)
            # Return the default value and description of that parameter
            info = param_info.get(param_name, {})
            description = info.get('description', '')

            # Clean up description by removing "field in the secret that contains" prefix
            if description:
                description = re.sub(r'^field in the secret that contains (an? )?', '', description, flags=re.IGNORECASE)

            return info.get('default', secret_key), description
        return secret_key, ''

    # Extract from stepTemplate env
    step_template = spec.get('stepTemplate', {})
    template_env = step_template.get('env', [])
    if template_env:
        for env_var in template_env:
            value_from = env_var.get('valueFrom', {})
            secret_ref = value_from.get('secretKeyRef', {})

            # Only include if it has secretKeyRef
            if secret_ref:
                env_name = env_var.get('name', '')
                secret_name = secret_ref.get('name', '')
                secret_key = secret_ref.get('key', '')
                property_name, property_description = resolve_property_info(secret_key)

                env_props.append({
                    'name': env_name,
                    'property_name': property_name,
                    'description': property_description,
                    'secret_name': secret_name,
                    'secret_key': secret_key,
                    'source': 'Task',
                    'secured': True
                })

    # Extract from individual steps env
    steps = spec.get('steps', [])
    if steps:
        for step in steps:
            step_env = step.get('env', [])
            if step_env:
                for env_var in step_env:
                    value_from = env_var.get('valueFrom', {})
                    secret_ref = value_from.get('secretKeyRef', {})

                    # Only include if it has secretKeyRef
                    if secret_ref:
                        env_name = env_var.get('name', '')
                        secret_name = secret_ref.get('name', '')
                        secret_key = secret_ref.get('key', '')
                        property_name, property_description = resolve_property_info(secret_key)

                        # Only add if not already in env_props (avoid duplicates from stepTemplate)
                        if not any(prop['name'] == env_name and prop['property_name'] == property_name for prop in env_props):
                            env_props.append({
                                'name': env_name,
                                'property_name': property_name,
                                'description': property_description,
                                'secret_name': secret_name,
                                'secret_key': secret_key,
                                'source': 'Task',
                                'secured': True
                            })

    return env_props


def extract_event_listener_info(listener_doc: Dict) -> Dict:
    """Extract EventListener information including trigger references."""
    if listener_doc.get('kind') != 'EventListener':
        return {}

    metadata = listener_doc.get('metadata', {})
    spec = listener_doc.get('spec', {})
    triggers = spec.get('triggers', [])

    trigger_refs = []
    for trigger in triggers:
        trigger_info = {
            'binding': None,
            'template': None
        }

        # Extract binding reference
        binding = trigger.get('binding', trigger.get('bindings', []))
        if isinstance(binding, dict):
            trigger_info['binding'] = binding.get('name')
        elif isinstance(binding, list) and len(binding) > 0:
            # Handle multiple bindings - take first one
            trigger_info['binding'] = binding[0].get('name') if isinstance(binding[0], dict) else binding[0]

        # Extract template reference
        template = trigger.get('template')
        if isinstance(template, dict):
            trigger_info['template'] = template.get('name')

        if trigger_info['binding'] or trigger_info['template']:
            trigger_refs.append(trigger_info)

    return {
        'name': metadata.get('name', 'Unknown'),
        'triggers': trigger_refs
    }


def process_yaml_files(file_paths: List[Path], verbose: bool = False) -> Tuple[List[Dict], List[Dict], List[Dict], List[str], List[str], List[Dict], Dict[str, Dict]]:
    """
    Process multiple YAML files and extract all parameters.

    Returns:
        Tuple of (pipeline_params, trigger_params, binding_params, pipeline_names, trigger_names, event_listeners, resource_map)
        where resource_map is a dict mapping resource names to their documents
    """
    pipeline_params = []
    trigger_params = []
    binding_params = []
    pipeline_names = []
    trigger_names = []
    event_listeners = []

    # Map to store all resources by name for reference resolution
    resource_map = {
        'Pipeline': {},
        'TriggerTemplate': {},
        'TriggerBinding': {},
        'EventListener': {},
        'Task': {}
    }

    for file_path in file_paths:
        if not file_path.exists():
            print(f"Warning: File not found: {file_path}", file=sys.stderr)
            continue

        if verbose:
            print(f"Parsing file: {file_path}", file=sys.stderr)

        documents = parse_yaml_file(file_path)

        for doc in documents:
            if not doc:
                continue

            kind = doc.get('kind', '')
            name = doc.get('metadata', {}).get('name', 'Unknown')

            if kind == 'Pipeline':
                pipeline_names.append(name)
                params = extract_pipeline_params(doc)
                pipeline_params.extend(params)
                resource_map['Pipeline'][name] = doc
                if verbose:
                    print(f"  Found Pipeline '{name}' with {len(params)} parameter(s)", file=sys.stderr)

            elif kind == 'TriggerTemplate':
                trigger_names.append(name)
                params = extract_trigger_template_params(doc)
                trigger_params.extend(params)
                resource_map['TriggerTemplate'][name] = doc
                if verbose:
                    print(f"  Found TriggerTemplate '{name}' with {len(params)} parameter(s)", file=sys.stderr)

            elif kind == 'TriggerBinding':
                params = extract_trigger_binding_params(doc)
                binding_params.extend(params)
                resource_map['TriggerBinding'][name] = doc
                if verbose:
                    print(f"  Found TriggerBinding '{name}' with {len(params)} parameter(s)", file=sys.stderr)

            elif kind == 'EventListener':
                listener_info = extract_event_listener_info(doc)
                if listener_info:
                    event_listeners.append(listener_info)
                    resource_map['EventListener'][name] = doc
                    if verbose:
                        print(f"  Found EventListener '{name}' with {len(listener_info.get('triggers', []))} trigger(s)", file=sys.stderr)

            elif kind == 'Task':
                env_props = extract_task_environment_properties(doc)
                resource_map['Task'][name] = doc
                if verbose:
                    print(f"  Found Task '{name}' with {len(env_props)} environment propert(y/ies)", file=sys.stderr)

    return pipeline_params, trigger_params, binding_params, pipeline_names, trigger_names, event_listeners, resource_map


def generate_markdown_table(params: List[Dict], title: str = "Parameters") -> str:
    """Generate a markdown table from parameters."""
    if not params:
        return f"## {title}\n\nNo parameters found.\n"

    markdown = [f"## {title}\n"]

    # Determine columns based on parameter source
    has_binding = any(p.get('source') == 'TriggerBinding' for p in params)

    if has_binding:
        # TriggerBinding format
        markdown.append("| Properties | Value | Source |")
        markdown.append("|------------|-------|--------|")
        for param in params:
            name = param.get('name', '')
            value = param.get('value', '')
            source = param.get('source', '')
            markdown.append(f"| `{name}` | `{value}` | {source} |")
    else:
        # Pipeline/TriggerTemplate format
        markdown.append("| Properties | Description | Default | Type | Source |")
        markdown.append("|------------|-------------|---------|------|--------|")
        for param in params:
            name = param.get('name', '')
            desc = param.get('description', '-')
            default = param.get('default', '')
            param_type = param.get('type', 'string')
            source = param.get('source', '')

            # Format default value
            if default == '':
                default_str = '*(required)*'
            else:
                default_str = f'`{default}`'

            markdown.append(f"| `{name}` | {desc} | {default_str} | {param_type} | {source} |")

    return '\n'.join(markdown) + '\n'


def resolve_event_listener_parameters(listener_info: Dict, resource_map: Dict[str, Dict], verbose: bool = False) -> List[Dict]:
    """
    Resolve all parameters for a specific EventListener by following trigger references.

    Args:
        listener_info: EventListener information with trigger references
        resource_map: Map of all resources by kind and name
        verbose: Print debug information

    Returns:
        List of merged parameters for this EventListener
    """
    all_params = []
    listener_name = listener_info.get('name', 'Unknown')

    if verbose:
        print(f"  Resolving parameters for EventListener '{listener_name}'", file=sys.stderr)

    for trigger in listener_info.get('triggers', []):
        binding_name = trigger.get('binding')
        template_name = trigger.get('template')

        # Get TriggerTemplate parameters
        if template_name and template_name in resource_map['TriggerTemplate']:
            template_doc = resource_map['TriggerTemplate'][template_name]
            template_params = extract_trigger_template_params(template_doc)
            all_params.extend(template_params)

            # Try to find referenced Pipeline
            pipeline_ref = None
            resource_templates = template_doc.get('spec', {}).get('resourcetemplates', [])
            for rt in resource_templates:
                if rt.get('kind') == 'PipelineRun':
                    pipeline_ref = rt.get('spec', {}).get('pipelineRef', {}).get('name')
                    break

            # Get Pipeline parameters if found
            if pipeline_ref and pipeline_ref in resource_map['Pipeline']:
                pipeline_doc = resource_map['Pipeline'][pipeline_ref]
                pipeline_params = extract_pipeline_params(pipeline_doc)
                all_params.extend(pipeline_params)
                if verbose:
                    print(f"    Found Pipeline '{pipeline_ref}' with {len(pipeline_params)} parameter(s)", file=sys.stderr)

                # Extract Task references from Pipeline and get their environment properties
                pipeline_spec = pipeline_doc.get('spec', {})
                pipeline_tasks = pipeline_spec.get('tasks', [])
                for task in pipeline_tasks:
                    task_ref = task.get('taskRef', {})
                    task_name = task_ref.get('name') if isinstance(task_ref, dict) else None

                    if task_name and task_name in resource_map['Task']:
                        task_doc = resource_map['Task'][task_name]
                        task_env_props = extract_task_environment_properties(task_doc)
                        all_params.extend(task_env_props)
                        if verbose:
                            print(f"      Found Task '{task_name}' with {len(task_env_props)} environment propert(y/ies)", file=sys.stderr)

        # Get TriggerBinding parameters
        if binding_name and binding_name in resource_map['TriggerBinding']:
            binding_doc = resource_map['TriggerBinding'][binding_name]
            binding_params = extract_trigger_binding_params(binding_doc)
            all_params.extend(binding_params)

    return all_params


def merge_parameters(pipeline_params: List[Dict],
                     trigger_params: List[Dict],
                     binding_params: List[Dict]) -> List[Dict]:
    """
    Merge parameters from all sources into a unified list.
    For parameters that appear in multiple sources, combine their information.
    Priority: Binding Value > Pipeline/Trigger Default
    """
    # Create a dictionary to track parameters by name
    param_dict = {}

    # Process pipeline parameters
    for param in pipeline_params:
        name = param['name']
        if name not in param_dict:
            param_dict[name] = {
                'name': name,
                'description': param.get('description', ''),
                'default': param.get('default', ''),
                'type': param.get('type', 'string'),
                'sources': []
            }
        param_dict[name]['sources'].append('Pipeline')
        if param.get('description'):
            param_dict[name]['description'] = param['description']
        # Store default if not already set
        if not param_dict[name]['default'] and param.get('default'):
            param_dict[name]['default'] = param['default']

    # Process trigger template parameters
    for param in trigger_params:
        name = param['name']
        if name not in param_dict:
            param_dict[name] = {
                'name': name,
                'description': param.get('description', ''),
                'default': param.get('default', ''),
                'type': param.get('type', 'string'),
                'sources': []
            }
        else:
            # Use trigger description if pipeline didn't have one
            if not param_dict[name]['description'] and param.get('description'):
                param_dict[name]['description'] = param['description']
            # Use trigger default if pipeline didn't have one
            if not param_dict[name]['default'] and param.get('default'):
                param_dict[name]['default'] = param['default']
        param_dict[name]['sources'].append('TriggerTemplate')

    # Process binding parameters - these override defaults
    for param in binding_params:
        name = param['name']
        binding_value = param.get('value', '')
        if name not in param_dict:
            param_dict[name] = {
                'name': name,
                'description': '',
                'default': binding_value,  # Binding value becomes the default
                'type': 'string',
                'sources': []
            }
        else:
            # Binding value overrides any default
            if binding_value:
                param_dict[name]['default'] = binding_value
        param_dict[name]['sources'].append('TriggerBinding')

    # Convert back to list and sort by name
    merged_params = sorted(param_dict.values(), key=lambda x: x['name'])
    return merged_params


def insert_at_anchor(existing_content: str, new_content: str, anchor: str, verbose: bool = False) -> str:
    """
    Insert new content at a specific anchor (heading) in existing markdown content.
    Replaces content between the anchor and the next heading of same or higher level.

    Args:
        existing_content: The existing markdown content
        new_content: The new content to insert
        anchor: The heading to search for (e.g., "## Parameters")
        verbose: Print debug information

    Returns:
        Updated content with new content inserted at anchor
    """
    import re

    lines = existing_content.split('\n')

    # Determine anchor level (count # characters)
    anchor_match = re.match(r'^(#+)\s+(.+)$', anchor.strip())
    if not anchor_match:
        print(f"Warning: Anchor '{anchor}' is not a valid markdown heading", file=sys.stderr)
        return existing_content

    anchor_level = len(anchor_match.group(1))
    anchor_text = anchor_match.group(2).strip()

    if verbose:
        print(f"Looking for anchor: level={anchor_level}, text='{anchor_text}'", file=sys.stderr)

    # Find the anchor line
    anchor_idx = -1
    for i, line in enumerate(lines):
        line_match = re.match(r'^(#+)\s+(.+)$', line.strip())
        if line_match:
            line_level = len(line_match.group(1))
            line_text = line_match.group(2).strip()
            if line_level == anchor_level and line_text.lower() == anchor_text.lower():
                anchor_idx = i
                if verbose:
                    print(f"Found anchor at line {i}", file=sys.stderr)
                break

    if anchor_idx == -1:
        print(f"Warning: Anchor '{anchor}' not found in file", file=sys.stderr)
        return existing_content

    # Find the next heading of same or higher level (lower number)
    next_heading_idx = len(lines)
    for i in range(anchor_idx + 1, len(lines)):
        line_match = re.match(r'^(#+)\s+', lines[i].strip())
        if line_match:
            line_level = len(line_match.group(1))
            if line_level <= anchor_level:
                next_heading_idx = i
                if verbose:
                    print(f"Found next heading at line {i}", file=sys.stderr)
                break

    # Extract content to insert from new content
    # When EventListeners are present, the content starts with subsection headings (e.g., "## eventlistener-name")
    # We want to keep these subsection headings and their content
    new_lines = new_content.split('\n')

    # Find where the actual content starts (skip any top-level title if present)
    content_start = 0
    for i, line in enumerate(new_lines):
        stripped = line.strip()
        # Skip empty lines and top-level titles that start with single #
        if stripped and not (stripped.startswith('# ') and not stripped.startswith('## ')):
            content_start = i
            break

    # Get content to insert
    content_to_insert = new_lines[content_start:] if content_start < len(new_lines) else new_lines

    # Remove trailing empty lines
    while content_to_insert and not content_to_insert[-1].strip():
        content_to_insert.pop()

    if verbose:
        print(f"Inserting {len(content_to_insert)} lines of content", file=sys.stderr)

    # Build the updated content
    result_lines = []
    result_lines.extend(lines[:anchor_idx + 1])  # Keep everything up to and including anchor
    result_lines.append('')  # Add blank line after anchor
    result_lines.extend(content_to_insert)  # Add new content
    if next_heading_idx < len(lines):
        result_lines.append('')  # Add blank line before next section
        result_lines.extend(lines[next_heading_idx:])  # Add remaining content

    result = '\n'.join(result_lines)
    # Ensure single trailing newline
    if not result.endswith('\n'):
        result += '\n'
    return result


def generate_combined_markdown(pipeline_params: List[Dict],
                               trigger_params: List[Dict],
                               binding_params: List[Dict],
                               pipeline_names: List[str],
                               trigger_names: List[str],
                               event_listeners: List[Dict],
                               resource_map: Dict[str, Dict],
                               heading_level: int = 1,
                               verbose: bool = False) -> str:
    """
    Generate combined markdown documentation with unified parameter table.
    If EventListeners are present, generates documentation per EventListener.
    Otherwise, generates combined documentation for all resources.

    Args:
        pipeline_params: List of pipeline parameters
        trigger_params: List of trigger template parameters
        binding_params: List of trigger binding parameters
        pipeline_names: List of pipeline names
        trigger_names: List of trigger template names
        event_listeners: List of EventListener information
        resource_map: Map of all resources by kind and name
        heading_level: Heading level for the main title (default: 1 for #)
        verbose: Print debug information
    """
    heading_prefix = '#' * heading_level
    params_heading_prefix = '#' * (heading_level + 1)

    # If EventListeners are present, generate documentation per EventListener
    if event_listeners:
        markdown_sections = []

        # Add introductory sentence before EventListener sections
        intro = [f"This pipeline and relevant trigger(s) can be configured using the properties described below.\n"]
        intro.append("See https://cloud.ibm.com/docs/ContinuousDelivery?topic=ContinuousDelivery-tekton-pipelines&interface=ui#configure_tekton_pipeline for more information.")
        markdown_sections.append('\n'.join(intro))

        for listener_info in event_listeners:
            listener_name = listener_info.get('name', 'Unknown')
            # Use heading one level deeper than the anchor for each EventListener
            section = [f"{params_heading_prefix} {listener_name}\n"]

            section.append(f"**EventListener**: {listener_name}")
            section.append('\n')

            # Resolve parameters for this EventListener
            listener_params = resolve_event_listener_parameters(listener_info, resource_map, verbose)

            # Separate by type
            el_pipeline_params = [p for p in listener_params if p.get('source') == 'Pipeline']
            el_trigger_params = [p for p in listener_params if p.get('source') == 'TriggerTemplate']
            el_binding_params = [p for p in listener_params if p.get('source') == 'TriggerBinding']
            el_task_env_props = [p for p in listener_params if p.get('source') == 'Task']

            # Merge parameters (excluding Task environment properties)
            merged_params = merge_parameters(el_pipeline_params, el_trigger_params, el_binding_params)

            if not merged_params and not el_task_env_props:
                section.append(f"No parameters found.\n")
            else:
                # Generate unified table for both parameters and environment properties
                section.append("| Properties | Description | Default | Required | Type |")
                section.append("|------------|-------------|---------|----------|------|")

                # Collect all properties in a list for sorting
                all_properties = []

                # Add regular parameters
                for param in merged_params:
                    name = param['name']
                    desc = param['description'] or '-'
                    default = param['default']

                    # Determine if required (no default value)
                    if default == '':
                        required = 'Yes'
                        default_str = '-'
                    else:
                        required = 'No'
                        default_str = f'`{default}`'

                    param_type = param['type']

                    all_properties.append({
                        'name': name,
                        'display_name': f'`{name}`',
                        'desc': desc,
                        'default_str': default_str,
                        'required': required,
                        'type': param_type
                    })

                # Add Task environment properties
                if el_task_env_props:
                    # Deduplicate by property_name
                    seen_props = {}
                    for prop in el_task_env_props:
                        property_name = prop.get('property_name', '-')
                        description = prop.get('description', '-')

                        if property_name not in seen_props:
                            seen_props[property_name] = True
                            all_properties.append({
                                'name': property_name,
                                'display_name': f'`{property_name}` (**secured property**)',
                                'desc': description,
                                'default_str': '-',
                                'required': 'Yes',
                                'type': 'secret'
                            })

                # Sort all properties by name (case-insensitive)
                all_properties.sort(key=lambda x: x['name'].lower())

                # Output sorted properties
                for prop in all_properties:
                    section.append(f"| {prop['display_name']} | {prop['desc']} | {prop['default_str']} | {prop['required']} | {prop['type']} |")

                section.append("")

            markdown_sections.append('\n'.join(section))

        result = ('\n' + '\n').join(markdown_sections)
        # Ensure single trailing newline using OS-specific line ending
        result = result.rstrip('\n') + '\n'
        return result

    # Fallback: Generate combined documentation (original behavior)
    markdown = [f"{heading_prefix} Properties Documentation\n"]

    # Add resource information
    resources = []
    if pipeline_names:
        resources.extend(pipeline_names)
    if trigger_names:
        resources.extend(trigger_names)

    if resources:
        markdown.append('\n')
        markdown.append(f"**resources**: {', '.join(resources)}")
        markdown.append('\n')

    # Merge all parameters
    merged_params = merge_parameters(pipeline_params, trigger_params, binding_params)

    if not merged_params:
        markdown.append(f"{params_heading_prefix} Parameters\n\nNo parameters found.\n")
        return '\n'.join(markdown) + '\n'

    # Generate unified table
    markdown.append(f"{params_heading_prefix} Parameters\n")
    markdown.append("| Properties | Description | Default | Required | Type |")
    markdown.append("|------------|-------------|---------|----------|------|")

    for param in merged_params:
        name = param['name']
        desc = param['description'] or '-'
        default = param['default']

        # Determine if required (no default value)
        if default == '':
            required = 'Yes'
            default_str = '-'
        else:
            required = 'No'
            default_str = f'`{default}`'

        param_type = param['type']

        markdown.append(f"| `{name}` | {desc} | {default_str} | {required} | {param_type} |")

    markdown.append("")

    result = '\n'.join(markdown)
    # Ensure single trailing newline using OS-specific line ending
    result = result.rstrip('\n') + '\n'
    return result


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate markdown documentation for Tekton parameters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process multiple YAML files and print to stdout
  python generate_pipeline_doc.py --file pipeline.yaml --file listener.yaml

  # Save to a new file
  python generate_pipeline_doc.py -f pipeline.yaml -f listener.yaml -o PARAMETERS.md

  # Insert at anchor in existing file
  python generate_pipeline_doc.py -f pipeline.yaml -f listener.yaml -o README.md -a "## Parameters"

  # Process all YAML files in directory
  python generate_pipeline_doc.py -f *.yaml -o PARAMETERS.md

  # Verbose mode
  python generate_pipeline_doc.py -f pipeline.yaml -f listener.yaml -v
        """
    )
    parser.add_argument('--file', '-f',
                       action='append',
                       dest='files',
                       required=True,
                       help='Path to YAML file (can be used multiple times). Files can contain Pipeline, TriggerTemplate, or TriggerBinding resources.')
    parser.add_argument('--output', '-o',
                       help='Output markdown file (default: print to stdout)')
    parser.add_argument('--anchor-output', '-a',
                       help='Markdown heading anchor in output file where content should be inserted (e.g., "## Parameters"). If specified, replaces content between this anchor and the next heading of same or higher level.')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    # Convert file paths to Path objects
    file_paths = [Path(f) for f in args.files]

    if args.verbose:
        print(f"Processing {len(file_paths)} file(s)...", file=sys.stderr)

    # Determine heading level from anchor if provided
    heading_level = 1  # Default
    if args.anchor_output:
        import re
        anchor_match = re.match(r'^(#+)\s+', args.anchor_output.strip())
        if anchor_match:
            # Use the same level as the anchor for the main heading
            # So if anchor is "## Parameters", we use "## Properties Documentation"
            heading_level = len(anchor_match.group(1))
            if args.verbose:
                print(f"Anchor level: {heading_level}, using same heading level for content", file=sys.stderr)

    # Process all files
    pipeline_params, trigger_params, binding_params, pipeline_names, trigger_names, event_listeners, resource_map = process_yaml_files(
        file_paths,
        args.verbose
    )

    # Generate markdown with appropriate heading level
    markdown = generate_combined_markdown(
        pipeline_params,
        trigger_params,
        binding_params,
        pipeline_names,
        trigger_names,
        event_listeners,
        resource_map,
        heading_level,
        args.verbose
    )

    # Output
    if args.output:
        output_path = Path(args.output)

        # Check if we need to insert at anchor
        if args.anchor_output:
            if output_path.exists():
                # Read existing file
                with open(output_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()

                # Insert at anchor
                updated_content = insert_at_anchor(existing_content, markdown, args.anchor_output, args.verbose)

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"Documentation inserted at anchor '{args.anchor_output}' in {output_path}")
            else:
                print(f"Error: Output file {output_path} does not exist. Cannot use --anchor-output with non-existent file.", file=sys.stderr)
                sys.exit(1)
        else:
            # Write entire file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"Documentation written to {output_path}")
    else:
        print(markdown)

    if args.verbose:
        print(f"\nSummary:", file=sys.stderr)
        print(f"  Pipelines found: {len(pipeline_names)}", file=sys.stderr)
        print(f"  Pipeline parameters: {len(pipeline_params)}", file=sys.stderr)
        print(f"  TriggerTemplates found: {len(trigger_names)}", file=sys.stderr)
        print(f"  TriggerTemplate parameters: {len(trigger_params)}", file=sys.stderr)
        print(f"  TriggerBinding parameters: {len(binding_params)}", file=sys.stderr)


if __name__ == '__main__':
    main()

# Made with Bob
