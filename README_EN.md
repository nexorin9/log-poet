# Log Poet — Transform System Error Messages into Poetry

> Turn cold system error messages into poetic words, exploring the lyrical expression of technical text.

## Overview

Log Poet is an experimental tool that transforms system error messages into poetry in various styles. It aims to explore the poetic expression of technical text and discover the hidden beauty and structure behind error messages.

## Features

- **Multiple poetry styles**: supports AABB, ABAB, free verse, haiku, and more templates
- **LLM-powered**: integrates OpenAI API for more creative poem generation
- **Interactive CLI**: command-line interface supporting single messages and batch processing
- **Error management**: collect, filter, and manage system error messages

## Project Structure

```
log-poet/
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Project configuration
├── .env.example             # Environment variable example
├── setup.py                 # Install script
├── main.py                  # CLI entry point
├── poetry_generator.py      # Template-based poetry generator
├── llm_poetry_generator.py  # LLM-based poetry generator
├── error_collector.py       # Error message collector
├── data/                    # Data storage
│   ├── errors.json          # Collected error messages
│   └── poems.json           # Generated poems
├── templates/               # Poetry templates
│   ├── aabb.txt             # AABB rhyme template
│   ├── abab.txt             # ABAB rhyme template
│   ├── freeverse.txt        # Free verse template
│   └── haiku.txt            # Haiku template
└── output/                  # Output directory
```

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API Key (optional, for LLM generation)

### Steps

1. Clone or download the project

2. Install dependencies
```bash
cd log-poet
pip install -r requirements.txt
```

3. Configure environment variables
```bash
cp .env.example .env
# Edit .env and add your OpenAI API Key
```

## Usage

### Basic

```bash
# Generate a poem from a command-line message
log-poet --input "File not found: example.txt"

# Load error messages from a file
log-poet --file data/errors.json

# Specify a poetry style
log-poet --input "Error" --style aabb

# Batch generation
log-poet --batch --input data/errors.json --output data/poems.json
```

### Options

| Option | Description |
|--------|-------------|
| `--input TEXT` | Input error message |
| `--file PATH` | Load error messages from file |
| `--style STYLE` | Poetry style (aabb/abab/freeverse/haiku) |
| `--batch` | Batch processing mode |
| `--output PATH` | Output file path |
| `--save TEXT` | Save poem |
| `--load PATH` | Load poem |
| `--list-errors` | List all error messages |
| `--filter CATEGORY` | Filter errors by category |
| `--search KEYWORD` | Search error messages |

## Poetry Templates

The project provides multiple templates supporting different rhythms and styles:

- **AABB**: paired rhyme, e.g., lines 1-2 rhyme, lines 3-4 rhyme
- **ABAB**: alternating rhyme, e.g., lines 1 & 3 rhyme, lines 2 & 4 rhyme
- **Freeverse**: free verse, no strict meter
- **Haiku**: three-line short poem (5-7-5 syllables)

## Data Formats

### Error message format (errors.json)

```json
{
  "errors": [
    {
      "code": "ENOENT",
      "message": "File not found",
      "category": "IO"
    }
  ]
}
```

### Poem output format (poems.json)

```json
{
  "poems": [
    {
      "error": "File not found",
      "poem": "A poem about the error",
      "style": "aabb"
    }
  ]
}
```

## Development

### Module descriptions

- `poetry_generator.py`: template-based poem generation
- `llm_poetry_generator.py`: LLM-based poem generation
- `error_collector.py`: collect system error messages
- `main.py`: CLI entry point and command handling

### Development mode

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linter
flake8 .
```

## Examples

### Example 1: Single error message

```bash
$ log-poet --input "File not found: example.txt" --style aabb
```

Output:
```
A file was lost, in the digital night,
Searching the void with all our might,
No trace remains, in the endless space,
Just silence echoes in this empty place.
```

### Example 2: Batch generation

```bash
$ log-poet --batch --input data/errors.json --output data/poems.json
```

### Example 3: LLM-powered generation

```bash
$ log-poet --input "Connection timeout" --style freeverse --model gpt-4
```

## License

MIT License

## Contributing

Issues and Pull Requests are welcome!

## Acknowledgements

Inspired by the exploration of poetic expression in technical text, and the discovery of hidden aesthetics behind error messages.

---

## Support the Author

If you find this project helpful, feel free to buy me a coffee! ☕

![Buy Me a Coffee](buymeacoffee.png)

**Buy me a coffee (crypto)**

| Chain | Address |
|-------|---------|
| BTC | `bc1qc0f5tv577z7yt59tw8sqaq3tey98xehy32frzd` |
| ETH / USDT | `0x3b7b6c47491e4778157f0756102f134d05070704` |
| SOL | `6Xuk373zc6x6XWcAAuqvbWW92zabJdCmN3CSwpsVM6sd` |
