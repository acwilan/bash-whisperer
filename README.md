# bash-whisperer 🤖

A local AI-powered assistant that translates natural language into bash commands, helping developers navigate the command line with ease.

## Overview

bash-whisperer is a lightweight command-line tool that uses a local Large Language Model (TinyLlama) to understand natural language queries and convert them into appropriate bash commands. No more googling for common command syntax or flag combinations - just ask in plain English!

## Key Features

- 🏃‍♂️ Runs completely locally - no API calls or internet connection required
- 🔒 Privacy-focused - your commands and data stay on your machine
- 🎯 Shows commands before execution for verification
- 🚀 Fast responses using TinyLlama, a lightweight LLM
- 📚 Comes with built-in examples for common operations
- 💡 Learn as you go - see the actual commands that match your intent

## Installation

### Dependencies
First, ensure you have Python 3.8 or higher installed. The project dependencies are listed in `requirements.txt`:
```
torch>=2.0.0
transformers>=4.36.0
packaging>=23.0
typing-extensions>=4.5.0
numpy>=1.24.0
tqdm>=4.65.0
regex>=2023.0
requests>=2.31.0
pyyaml>=6.0.1
filelock>=3.12.0
```

### Setup

1. Clone the repository:
```bash
git clone https://github.com/acwilan/bash-whisperer.git
cd bash-whisperer
```

2. Set up a virtual environment (recommended):
```bash
# Create a virtual environment
python -m venv venv

# Activate it (on Unix/macOS)
source venv/bin/activate
# OR on Windows
# venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make it executable (optional):
```bash
chmod +x bash_assistant.py
```

### First Run

On first run, the script will:
1. Create a `.bash-whisperer` directory in your home folder
2. Download the TinyLlama model (approximately 2GB) to `.bash-whisperer/models`
3. This download happens only once, and subsequent runs will use the cached model

Note: You need an internet connection for the first run to download the model.

## Usage

```bash
python bash_assistant.py
```

Or create an alias in your `.bashrc` or `.zshrc`:
```bash
alias bw="python /path/to/bash_assistant.py"
```

Then simply describe what you want to do:
```
Enter your query: list all PDF files in current directory sorted by size
Generated command: ls -lhS *.pdf
Execute this command? (y/n):
```

## Examples

- "show system memory usage in human readable format"
- "find all files larger than 100MB"
- "compress all images in this folder"
- "list recently modified files"
- "show directory structure as a tree"

## Requirements

- Python 3.8+
- ~2GB of disk space for the model
- See `requirements.txt` for full dependency list

## Contributing

Contributions are welcome! Feel free to:
- Add more example commands
- Improve command generation
- Enhance the user interface
- Add support for more shells

## License

MIT License

## Acknowledgments

Built using the TinyLlama model, a lightweight and efficient language model suitable for local deployment.