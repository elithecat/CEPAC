#!/usr/bin/env python3
"""
CEPAC Preset Generator CLI

Generate .in files from published parameter presets without using the UI.

Usage:
    python generate_preset.py --list
    python generate_preset.py --preset PMC9087297_VHR_NoPrEP --output run.in
    python generate_preset.py --preset PMC9087297 --all --output-dir ./presets/
"""

import argparse
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from input_generator import InputGenerator
from presets.pmc9087297 import (
    PMC9087297_SCENARIOS,
    get_pmc9087297_scenario,
    PAPER_METADATA
)


# Registry of all available presets
PRESET_REGISTRY = {
    'PMC9087297': {
        'metadata': PAPER_METADATA,
        'scenarios': PMC9087297_SCENARIOS,
        'get_scenario': get_pmc9087297_scenario,
    },
}


def list_presets():
    """List all available presets and scenarios."""
    print("Available Presets")
    print("=" * 70)

    for preset_id, preset_info in PRESET_REGISTRY.items():
        meta = preset_info['metadata']
        print(f"\n{preset_id}")
        print(f"  Title: {meta.get('title', 'N/A')}")
        print(f"  Setting: {meta.get('setting', 'N/A')}")
        print(f"  Population: {meta.get('population', 'N/A')}")
        print(f"  Currency Year: {meta.get('currency_year', 'N/A')}")
        print(f"\n  Scenarios:")

        for scenario_name, scenario_info in preset_info['scenarios'].items():
            print(f"    - {scenario_name}")
            print(f"      {scenario_info.get('description', '')}")

    print("\n" + "=" * 70)
    print("\nUsage:")
    print("  python generate_preset.py --preset <SCENARIO_NAME> --output <file.in>")
    print("  python generate_preset.py --preset <PRESET_ID> --all --output-dir <dir>")


def get_preset_scenario(scenario_name):
    """Get parameters for a scenario from any registered preset."""
    # Check each preset for the scenario
    for preset_id, preset_info in PRESET_REGISTRY.items():
        if scenario_name in preset_info['scenarios']:
            return preset_info['get_scenario'](scenario_name)

    # Not found
    all_scenarios = []
    for preset_info in PRESET_REGISTRY.values():
        all_scenarios.extend(preset_info['scenarios'].keys())

    raise ValueError(f"Unknown scenario: {scenario_name}\n"
                    f"Available scenarios: {', '.join(all_scenarios)}")


def generate_in_file(params):
    """Generate .in file content from parameters."""
    generator = InputGenerator()
    return generator.generate(params)


def write_scenario_file(scenario_name, output_path, verbose=True):
    """Generate and write a single scenario to a file."""
    params = get_preset_scenario(scenario_name)
    content = generate_in_file(params)

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, 'w') as f:
        f.write(content)

    if verbose:
        print(f"Generated: {output_path}")

    return output_path


def generate_all_scenarios(preset_id, output_dir, verbose=True):
    """Generate all scenarios for a preset."""
    if preset_id not in PRESET_REGISTRY:
        raise ValueError(f"Unknown preset: {preset_id}. "
                        f"Available: {', '.join(PRESET_REGISTRY.keys())}")

    preset_info = PRESET_REGISTRY[preset_id]
    generated_files = []

    for scenario_name in preset_info['scenarios'].keys():
        output_path = os.path.join(output_dir, f"{scenario_name}.in")
        write_scenario_file(scenario_name, output_path, verbose)
        generated_files.append(output_path)

    return generated_files


def main():
    parser = argparse.ArgumentParser(
        description='Generate CEPAC .in files from published parameter presets',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  List all available presets and scenarios:
    python generate_preset.py --list

  Generate a single scenario:
    python generate_preset.py --preset PMC9087297_VHR_NoPrEP --output run.in

  Generate all scenarios for a preset:
    python generate_preset.py --preset PMC9087297 --all --output-dir ./presets/
        """
    )

    parser.add_argument('--list', '-l', action='store_true',
                       help='List all available presets and scenarios')
    parser.add_argument('--preset', '-p', type=str,
                       help='Preset or scenario name to generate')
    parser.add_argument('--output', '-o', type=str,
                       help='Output file path (for single scenario)')
    parser.add_argument('--output-dir', '-d', type=str, default='.',
                       help='Output directory (for --all)')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Generate all scenarios for a preset')
    parser.add_argument('--verbose', '-v', action='store_true', default=True,
                       help='Print progress messages')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress progress messages')

    args = parser.parse_args()
    verbose = args.verbose and not args.quiet

    if args.list:
        list_presets()
        return 0

    if not args.preset:
        parser.print_help()
        return 1

    try:
        if args.all:
            # Generate all scenarios for a preset
            if args.preset in PRESET_REGISTRY:
                files = generate_all_scenarios(args.preset, args.output_dir, verbose)
                if verbose:
                    print(f"\nGenerated {len(files)} files in {args.output_dir}")
            else:
                print(f"Error: '{args.preset}' is not a preset ID. Use --list to see available presets.",
                      file=sys.stderr)
                return 1
        else:
            # Generate a single scenario
            output_path = args.output or f"{args.preset}.in"
            write_scenario_file(args.preset, output_path, verbose)

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
