#!/usr/bin/env python3
"""
Log Poet - Main CLI entry point
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from poetry_generator import TemplatePoetryGenerator
from llm_poetry_generator import LLMPoetryGenerator


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        prog="log-poet",
        description="Transform system error messages into poetry",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate poem from command line
  log-poet --input "File not found: example.txt"

  # Generate from file
  log-poet --file data/errors.json

  # Specify style
  log-poet --input "Error" --style aabb

  # Batch generation
  log-poet --batch --input data/errors.json --output data/poems.json

  # Use LLM
  log-poet --input "Connection timeout" --style freeverse --tone mysterious
        """
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument("--input", "-i", help="Input error message")
    input_group.add_argument("--file", "-f", help="Load errors from JSON file")

    # Style options
    parser.add_argument("--style", "-s", default="aabb",
                        choices=["aabb", "abab", "freeverse", "haiku"],
                        help="Poetry style (default: aabb)")

    # Output options
    parser.add_argument("--output", "-o", default="data/poems.json",
                        help="Output JSON file path (default: data/poems.json)")

    # Batch mode
    parser.add_argument("--batch", "-b", action="store_true",
                        help="Batch mode - generate poems from file")

    # LLM options
    parser.add_argument("--llm", action="store_true",
                        help="Use LLM for generation (requires OpenAI API key)")
    parser.add_argument("--tone", "-t", default="playful",
                        choices=["formal", "playful", "mysterious", "emotional"],
                        help="Writing tone for LLM (default: playful)")

    # Save/Load options
    parser.add_argument("--save", help="Save poem to database")
    parser.add_argument("--load", help="Load poems from file")

    # Data management options
    parser.add_argument("--list-errors", action="store_true",
                        help="List all error messages from data/errors.json")
    parser.add_argument("--filter", help="Filter errors by category")
    parser.add_argument("--search", help="Search errors by keyword")

    # Template options
    parser.add_argument("--list-templates", action="store_true",
                        help="List available poetry templates")

    return parser


def handle_list_templates(generator: TemplatePoetryGenerator) -> None:
    """Handle list templates command"""
    print("\nAvailable poetry templates:")
    for template in generator.list_templates():
        print(f"  - {template}")
    print()


def handle_list_errors() -> None:
    """Handle list errors command"""
    errors_file = Path("data/errors.json")
    if not errors_file.exists():
        print("No errors file found. Run error_collector.py first.")
        return

    try:
        with open(errors_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            errors = data.get("errors", [])

        print(f"\nTotal errors: {len(errors)}\n")
        for i, error in enumerate(errors[:20], 1):  # Show first 20
            print(f"{i}. [{error.get('code', 'N/A')}] {error.get('message', 'N/A')}")
            print(f"   Category: {error.get('category', 'N/A')}")
            print()

        if len(errors) > 20:
            print(f"... and {len(errors) - 20} more errors")
    except Exception as e:
        print(f"Error loading errors: {e}")


def handle_filter_errors(category: str) -> None:
    """Handle filter errors command"""
    errors_file = Path("data/errors.json")
    if not errors_file.exists():
        print("No errors file found.")
        return

    try:
        with open(errors_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            errors = data.get("errors", [])

        filtered = [e for e in errors if e.get("category", "").lower() == category.lower()]

        print(f"\nFiltered by category '{category}': {len(filtered)} errors\n")
        for i, error in enumerate(filtered[:20], 1):
            print(f"{i}. [{error.get('code', 'N/A')}] {error.get('message', 'N/A')}")
            print()

        if len(filtered) > 20:
            print(f"... and {len(filtered) - 20} more errors")
    except Exception as e:
        print(f"Error filtering errors: {e}")


def handle_search_errors(keyword: str) -> None:
    """Handle search errors command"""
    errors_file = Path("data/errors.json")
    if not errors_file.exists():
        print("No errors file found.")
        return

    try:
        with open(errors_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            errors = data.get("errors", [])

        keyword = keyword.lower()
        results = [e for e in errors
                   if keyword in e.get("message", "").lower()
                   or keyword in e.get("code", "").lower()]

        print(f"\nSearch results for '{keyword}': {len(results)} errors\n")
        for i, error in enumerate(results[:20], 1):
            print(f"{i}. [{error.get('code', 'N/A')}] {error.get('message', 'N/A')}")
            print()

        if len(results) > 20:
            print(f"... and {len(results) - 20} more results")
    except Exception as e:
        print(f"Error searching errors: {e}")


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()

    # Handle special commands first (no input required)
    if args.list_templates:
        generator = TemplatePoetryGenerator()
        handle_list_templates(generator)
        return

    if args.list_errors:
        handle_list_errors()
        return

    if args.filter:
        handle_filter_errors(args.filter)
        return

    if args.search:
        handle_search_errors(args.search)
        return

    # Load errors if in batch mode
    errors = []
    if args.batch or args.file:
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                errors = [e.get("message", "") for e in data.get("errors", [])]
        else:
            print("Error: --batch requires --file option")
            return

    # Choose generator based on --llm flag
    if args.llm:
        try:
            generator = LLMPoetryGenerator()
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            print("Please set OPENAI_API_KEY environment variable", file=sys.stderr)
            return
        except Exception as e:
            print(f"Error initializing LLM generator: {e}", file=sys.stderr)
            return
    else:
        generator = TemplatePoetryGenerator()

    # Generate poems
    if args.batch:
        if args.llm:
            poems = generator.generate_batch(errors, args.style, args.tone)
        else:
            poems = generator.generate_batch(errors, args.style)

        generator.save_poems(poems, args.output)

        print(f"\nGenerated {len(poems)} poems:\n")
        for poem in poems:
            print(f"Error: {poem.error}")
            print(f"Poem:\n{poem.poem}\n")
            print("-" * 80)
    else:
        # Single message mode
        if args.input:
            try:
                if args.llm:
                    poem = generator.generate(args.input, args.style, args.tone)
                else:
                    poem = generator.generate(args.input, args.style)

                print(f"\n{poem}\n")
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
        else:
            parser.print_help()


if __name__ == "__main__":
    main()