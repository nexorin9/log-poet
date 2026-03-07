#!/usr/bin/env python3
"""
Poetry Generator - Template-based poetry generation
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class Poem:
    """Data class for poem"""
    error: str
    poem: str
    style: str
    template: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert poem to dictionary"""
        return {
            "error": self.error,
            "poem": self.poem,
            "style": self.style,
            "template": self.template
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Poem':
        """Create poem from dictionary"""
        return cls(**data)


class TemplatePoetryGenerator:
    """Generate poetry using templates"""

    def __init__(self, templates_dir: str = "templates"):
        """
        Initialize poetry generator

        Args:
            templates_dir: Directory containing template files
        """
        self.templates_dir = Path(templates_dir)
        self.templates: Dict[str, str] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """Load all template files"""
        if not self.templates_dir.exists():
            raise FileNotFoundError(f"Templates directory not found: {self.templates_dir}")

        for template_file in self.templates_dir.glob("*.txt"):
            style = template_file.stem  # filename without extension
            with open(template_file, 'r', encoding='utf-8') as f:
                self.templates[style] = f.read()

    def load_template(self, style: str) -> str:
        """
        Load a specific template by style

        Args:
            style: Template style name (aabb, abab, freeverse, haiku)

        Returns:
            Template content

        Raises:
            FileNotFoundError: If template doesn't exist
        """
        template_path = self.templates_dir / f"{style}.txt"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {style}.txt")

        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()

    def generate(self, error_message: str, style: str = "aabb") -> str:
        """
        Generate a poem from an error message

        Args:
            error_message: The error message to transform
            style: Poetry style (aabb, abab, freeverse, haiku)

        Returns:
            Generated poem

        Raises:
            FileNotFoundError: If template doesn't exist
        """
        try:
            template = self.load_template(style)
            poem = self._fill_template(template, error_message)
            return poem
        except FileNotFoundError as e:
            print(f"Error: {e}", file=__import__('sys').stderr)
            # Fallback to freeverse if requested style doesn't exist
            if style != "freeverse":
                print("Falling back to freeverse style", file=__import__('sys').stderr)
                return self.generate(error_message, "freeverse")
            raise

    def _fill_template(self, template: str, error_message: str) -> str:
        """
        Fill template with error message

        Args:
            template: Template string
            error_message: Error message to insert

        Returns:
            Filled template
        """
        # Extract lines from error message
        lines = [line.strip() for line in error_message.split('\n') if line.strip()]

        # Use first line as main message, rest as additional context
        main_message = lines[0] if lines else error_message

        # Prepare placeholders
        placeholders = {
            "message": main_message,
            "first_line": self._generate_line(lines),
            "second_line": self._generate_line(lines),
            "third_line": self._generate_line(lines),
            "fourth_line": self._generate_line(lines),
            "line1": self._generate_line(lines),
            "line2": self._generate_line(lines),
            "line3": self._generate_line(lines)
        }

        # Fill template
        poem = template
        for key, value in placeholders.items():
            poem = poem.replace(f"{{{key}}}", value)

        return poem

    def _generate_line(self, lines: List[str]) -> str:
        """
        Generate a poetic line from error message

        Args:
            lines: List of error message lines

        Returns:
            Generated poetic line
        """
        # Simple line generation: capitalize, add poetic touch
        if not lines:
            return "In silence deep, the error creeps."

        # Take first line and transform it
        line = lines[0]
        words = line.split()

        if len(words) <= 2:
            # Short message - expand with poetic elements
            return f"In {line.lower()}, the shadows sleep."

        # Capitalize and add poetic ending
        capitalized = ' '.join([word.capitalize() for word in words[:3]])
        return f"{capitalized}, where echoes fall."

    def generate_batch(self, errors: List[str], style: str = "aabb") -> List[Poem]:
        """
        Generate poems from multiple error messages

        Args:
            errors: List of error messages
            style: Poetry style

        Returns:
            List of generated poems
        """
        poems = []
        for error in errors:
            try:
                poem = self.generate(error, style)
                poems.append(Poem(error=error, poem=poem, style=style))
            except Exception as e:
                print(f"Error generating poem for '{error}': {e}", file=__import__('sys').stderr)
                # Add error poem
                poems.append(Poem(
                    error=error,
                    poem=f"Error: {e}\n\nFailed to generate poem for: {error}",
                    style=style
                ))
        return poems

    def save_poems(self, poems: List[Poem], output_path: str = "data/poems.json") -> None:
        """
        Save poems to JSON file

        Args:
            poems: List of poems to save
            output_path: Output file path
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "poems": [poem.to_dict() for poem in poems],
                "generated_at": str(Path.cwd())
            }, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(poems)} poems to {output_path}")

    def load_poems(self, input_path: str = "data/poems.json") -> List[Poem]:
        """
        Load poems from JSON file

        Args:
            input_path: Input file path

        Returns:
            List of loaded poems
        """
        input_file = Path(input_path)
        if not input_file.exists():
            print(f"Warning: {input_path} does not exist")
            return []

        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Poem.from_dict(poem_data) for poem_data in data.get("poems", [])]

    def list_templates(self) -> List[str]:
        """
        List available template styles

        Returns:
            List of template style names
        """
        return list(self.templates.keys())


def main():
    """Main entry point for CLI"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate poetry from error messages")
    parser.add_argument("--input", "-i", help="Input error message")
    parser.add_argument("--file", "-f", help="Load errors from file")
    parser.add_argument("--style", "-s", default="aabb",
                        choices=["aabb", "abab", "freeverse", "haiku"],
                        help="Poetry style")
    parser.add_argument("--output", "-o", default="data/poems.json",
                        help="Output JSON file path")
    parser.add_argument("--batch", "-b", action="store_true",
                        help="Batch mode")
    parser.add_argument("--list-templates", "-l", action="store_true",
                        help="List available templates")

    args = parser.parse_args()

    generator = TemplatePoetryGenerator()

    if args.list_templates:
        print("\nAvailable templates:")
        for template in generator.list_templates():
            print(f"  - {template}")
        return

    if args.input:
        # Single message mode
        poem = generator.generate(args.input, args.style)
        print(f"\n{poem}\n")
    elif args.file:
        # Load from file and generate
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            errors = [e.get("message", "") for e in data.get("errors", [])]

        if not errors:
            print("No errors found in file")
            return

        poems = generator.generate_batch(errors, args.style)
        generator.save_poems(poems, args.output)

        print(f"\nGenerated {len(poems)} poems:\n")
        for poem in poems:
            print(f"Error: {poem.error}")
            print(f"Poem:\n{poem.poem}\n")
            print("-" * 80)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()