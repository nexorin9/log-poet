#!/usr/bin/env python3
"""
LLM Poetry Generator - Poetry generation using LLM API
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class LLMPoem:
    """Data class for LLM-generated poem"""
    error: str
    poem: str
    style: str
    model: str
    tokens_used: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert poem to dictionary"""
        return {
            "error": self.error,
            "poem": self.poem,
            "style": self.style,
            "model": self.model,
            "tokens_used": self.tokens_used
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LLMPoem':
        """Create poem from dictionary"""
        return cls(**data)


class LLMPoetryGenerator:
    """Generate poetry using LLM API"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize LLM poetry generator

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model name (defaults to DEFAULT_MODEL env var or gpt-3.5-turbo)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")

        self.model = model or os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")

        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

    def generate(self, error_message: str, style: str = "aabb",
                 tone: str = "playful",
                 additional_context: Optional[str] = None) -> str:
        """
        Generate a poem using LLM

        Args:
            error_message: The error message to transform
            style: Poetry style (aabb, abab, freeverse, haiku)
            tone: Writing tone (formal, playful, mysterious, emotional)
            additional_context: Additional context for the poem

        Returns:
            Generated poem
        """
        # Build prompt
        prompt = self._build_prompt(error_message, style, tone, additional_context)

        # Call LLM API
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a poetic AI that transforms technical error messages into beautiful poetry. Your poems should be thoughtful, creative, and explore the deeper meaning of errors."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=200
            )

            poem = response.choices[0].message.content.strip()
            tokens_used = response.usage.total_tokens

            return poem

        except Exception as e:
            raise Exception(f"LLM API error: {e}")

    def _build_prompt(self, error_message: str, style: str, tone: str,
                      additional_context: Optional[str]) -> str:
        """
        Build prompt for LLM

        Args:
            error_message: Error message
            style: Poetry style
            tone: Writing tone
            additional_context: Additional context

        Returns:
            Prompt string
        """
        prompt = f"Transform the following error message into a {style} style poem with a {tone} tone:\n\n"
        prompt += f"Error message: {error_message}\n"

        if additional_context:
            prompt += f"Context: {additional_context}\n"

        prompt += "\nPoem:"

        return prompt

    def generate_batch(self, errors: List[str], style: str = "aabb",
                       tone: str = "playful",
                       batch_size: int = 10) -> List[LLMPoem]:
        """
        Generate poems from multiple error messages

        Args:
            errors: List of error messages
            style: Poetry style
            tone: Writing tone
            batch_size: Number of errors to process in each batch

        Returns:
            List of generated poems
        """
        poems = []

        for i in range(0, len(errors), batch_size):
            batch = errors[i:i + batch_size]
            print(f"Processing batch {i // batch_size + 1}/{(len(errors) + batch_size - 1) // batch_size}...")

            for error in batch:
                try:
                    poem = self.generate(error, style, tone)
                    poems.append(LLMPoem(
                        error=error,
                        poem=poem,
                        style=style,
                        model=self.model
                    ))
                except Exception as e:
                    print(f"Error generating poem for '{error}': {e}", file=__import__('sys').stderr)
                    # Add error poem
                    poems.append(LLMPoem(
                        error=error,
                        poem=f"Error: {e}\n\nFailed to generate poem for: {error}",
                        style=style,
                        model=self.model
                    ))

        return poems

    def save_poems(self, poems: List[LLMPoem], output_path: str = "data/poems.json") -> None:
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
                "generated_at": str(Path.cwd()),
                "model": self.model
            }, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(poems)} poems to {output_path}")

    def load_poems(self, input_path: str = "data/poems.json") -> List[LLMPoem]:
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
            return [LLMPoem.from_dict(poem_data) for poem_data in data.get("poems", [])]

    def test_connection(self) -> Dict[str, Any]:
        """
        Test API connection

        Returns:
            Connection test result
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": "Say 'Hello from Log Poet!'"
                    }
                ],
                max_tokens=10
            )

            return {
                "success": True,
                "message": response.choices[0].message.content,
                "model": self.model,
                "tokens_used": response.usage.total_tokens
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


def main():
    """Main entry point for CLI"""
    import argparse

    parser = argparse.ArgumentParser(description="Generate poetry using LLM API")
    parser.add_argument("--input", "-i", help="Input error message")
    parser.add_argument("--file", "-f", help="Load errors from file")
    parser.add_argument("--style", "-s", default="aabb",
                        choices=["aabb", "abab", "freeverse", "haiku"],
                        help="Poetry style")
    parser.add_argument("--tone", "-t", default="playful",
                        choices=["formal", "playful", "mysterious", "emotional"],
                        help="Writing tone")
    parser.add_argument("--output", "-o", default="data/poems.json",
                        help="Output JSON file path")
    parser.add_argument("--batch", "-b", action="store_true",
                        help="Batch mode")
    parser.add_argument("--test-connection", action="store_true",
                        help="Test API connection")
    parser.add_argument("--model", help="Override default model")

    args = parser.parse_args()

    # Create generator
    try:
        generator = LLMPoetryGenerator(model=args.model)
    except ValueError as e:
        print(f"Error: {e}", file=__import__('sys').stderr)
        print("Please set OPENAI_API_KEY environment variable", file=__import__('sys').stderr)
        return

    # Test connection
    if args.test_connection:
        result = generator.test_connection()
        if result["success"]:
            print(f"\n✓ Connection successful!")
            print(f"Model: {result['model']}")
            print(f"Response: {result['message']}")
        else:
            print(f"\n✗ Connection failed: {result['error']}")
        return

    # Single message mode
    if args.input:
        try:
            poem = generator.generate(args.input, args.style, args.tone)
            print(f"\n{poem}\n")
        except Exception as e:
            print(f"Error: {e}", file=__import__('sys').stderr)
    elif args.file:
        # Load from file and generate
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            errors = [e.get("message", "") for e in data.get("errors", [])]

        if not errors:
            print("No errors found in file")
            return

        poems = generator.generate_batch(errors, args.style, args.tone)
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