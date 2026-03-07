#!/usr/bin/env python3
"""
Error Collector - Collect error messages from Python standard library
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any


class ErrorCollector:
    """Collect error messages from Python standard library exceptions"""

    def __init__(self, library_path: str = None):
        """
        Initialize error collector

        Args:
            library_path: Path to Python standard library (optional, will auto-detect)
        """
        if library_path is None:
            # Try to find Python standard library
            python_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
            library_path = Path(f"/usr/lib/{python_version}/site-packages" if sys.platform == "linux"
                              else f"C:\\Python{sys.version_info.major}.{sys.version_info.minor}\\Lib" if sys.platform == "win32"
                              else f"/usr/local/lib/{python_version}/site-packages")

        self.library_path = Path(library_path)
        self.errors: List[Dict[str, Any]] = []

    def collect_from_module(self, module_name: str) -> List[Dict[str, Any]]:
        """
        Collect errors from a specific module

        Args:
            module_name: Name of the module to collect from

        Returns:
            List of collected errors
        """
        errors = []
        try:
            module = __import__(module_name)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, Exception):
                    # Collect error message from __init__ and __str__
                    error_info = self._extract_error_info(attr)
                    if error_info:
                        error_info["module"] = module_name
                        error_info["class"] = attr.__name__
                        errors.append(error_info)
        except ImportError:
            print(f"Warning: Could not import {module_name}", file=sys.stderr)
        except Exception as e:
            print(f"Error processing {module_name}: {e}", file=sys.stderr)

        return errors

    def _extract_error_info(self, exception_class: type) -> Dict[str, Any]:
        """
        Extract error information from an exception class

        Args:
            exception_class: Exception class to analyze

        Returns:
            Dictionary with error information
        """
        error_info = {
            "code": f"{exception_class.__module__}.{exception_class.__name__}".replace("_", "").upper(),
            "message": "",
            "category": "Unknown",
            "class_name": exception_class.__name__
        }

        # Try to get message from __init__
        if exception_class.__init__.__doc__:
            doc = exception_class.__init__.__doc__
            # Extract first sentence or first line
            lines = doc.strip().split('\n')
            error_info["message"] = lines[0].strip()

        # Try to get message from __str__
        if not error_info["message"] and hasattr(exception_class, "__str__"):
            try:
                # Try to create instance and get message
                instance = exception_class()
                error_info["message"] = str(instance)
            except:
                pass

        # Try to get category from module name
        if "Error" in exception_class.__name__ or "Exception" in exception_class.__name__:
            error_info["category"] = "Error"
        elif "Warning" in exception_class.__name__:
            error_info["category"] = "Warning"
        elif "Runtime" in exception_class.__name__:
            error_info["category"] = "Runtime"

        return error_info

    def collect_from_modules(self, module_names: List[str]) -> None:
        """
        Collect errors from multiple modules

        Args:
            module_names: List of module names to collect from
        """
        for module_name in module_names:
            errors = self.collect_from_module(module_name)
            self.errors.extend(errors)
            print(f"Collected {len(errors)} errors from {module_name}")

    def save_to_file(self, output_path: str = "data/errors.json") -> None:
        """
        Save collected errors to JSON file

        Args:
            output_path: Path to save errors
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "errors": self.errors,
                "collected_at": str(Path.cwd())
            }, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(self.errors)} errors to {output_path}")

    def load_from_file(self, input_path: str = "data/errors.json") -> None:
        """
        Load errors from JSON file

        Args:
            input_path: Path to load errors from
        """
        input_file = Path(input_path)
        if not input_file.exists():
            print(f"Warning: {input_path} does not exist")
            return

        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.errors = data.get("errors", [])
            print(f"Loaded {len(self.errors)} errors from {input_path}")

    def filter_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Filter errors by category

        Args:
            category: Category to filter by

        Returns:
            Filtered list of errors
        """
        return [e for e in self.errors if e.get("category", "").lower() == category.lower()]

    def search_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Search errors by keyword in message or code

        Args:
            keyword: Keyword to search for

        Returns:
            List of matching errors
        """
        keyword = keyword.lower()
        return [e for e in self.errors
                if keyword in e.get("message", "").lower()
                or keyword in e.get("code", "").lower()]

    def list_errors(self) -> None:
        """Print all collected errors"""
        print(f"\nCollected {len(self.errors)} errors:")
        print("-" * 80)
        for i, error in enumerate(self.errors[:20], 1):  # Show first 20
            print(f"{i}. [{error['code']}] {error['message']}")
            print(f"   Class: {error['class_name']}, Module: {error['module']}, Category: {error['category']}")
            print()


def main():
    """Main entry point for CLI"""
    import argparse

    parser = argparse.ArgumentParser(description="Collect Python standard library error messages")
    parser.add_argument("--output", "-o", default="data/errors.json",
                        help="Output JSON file path")
    parser.add_argument("--load", "-l", help="Load errors from file")
    parser.add_argument("--list", "-L", action="store_true",
                        help="List collected errors")
    parser.add_argument("--filter", "-f", help="Filter by category")
    parser.add_argument("--search", "-s", help="Search by keyword")
    parser.add_argument("--modules", "-m", nargs="+",
                        help="Specific modules to collect from")

    args = parser.parse_args()

    collector = ErrorCollector()

    # Load from file if specified
    if args.load:
        collector.load_from_file(args.load)

    # Collect from specific modules if specified
    if args.modules:
        collector.collect_from_modules(args.modules)
    else:
        # Collect from common modules
        common_modules = [
            "builtins", "exceptions", "OSError", "IOError", "ValueError",
            "TypeError", "KeyError", "AttributeError", "RuntimeError",
            "ImportError", "IndexError", "SyntaxError", "LookupError",
            "MemoryError", "ZeroDivisionError", "OverflowError",
            "FileNotFoundError", "PermissionError", "NotImplementedError"
        ]
        collector.collect_from_modules(common_modules)

    # Filter if specified
    if args.filter:
        filtered = collector.filter_by_category(args.filter)
        print(f"\nFiltered by category '{args.filter}': {len(filtered)} errors")
        for error in filtered[:10]:
            print(f"- [{error['code']}] {error['message']}")
        if len(filtered) > 10:
            print(f"... and {len(filtered) - 10} more")
    elif args.search:
        results = collector.search_by_keyword(args.search)
        print(f"\nSearch results for '{args.search}': {len(results)} errors")
        for error in results[:10]:
            print(f"- [{error['code']}] {error['message']}")
        if len(results) > 10:
            print(f"... and {len(results) - 10} more")
    elif args.list:
        collector.list_errors()

    # Save to file if no filtering/searching
    if not args.filter and not args.search and not args.list:
        collector.save_to_file(args.output)


if __name__ == "__main__":
    main()