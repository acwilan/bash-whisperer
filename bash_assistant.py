#!/usr/bin/env python3
import sys
import subprocess
import os
from pathlib import Path
from typing import Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Pipeline, pipeline

class BashAssistant:
    def __init__(self, 
                 model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                 models_dir: str = "~/.bash-whisperer/models"):
        """
        Initialize the bash assistant with a specified model.
        
        Args:
            model_name: The name of the model to use from Hugging Face
            models_dir: Local directory to store the downloaded model
        """
        self.model_name = model_name
        self.models_dir = os.path.expanduser(models_dir)
        
        # Create models directory if it doesn't exist
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Initialize model and tokenizer
        self._initialize_model()
        
        # Load command templates and examples
        self.examples = [
            ("list files by size", "ls -lhS"),
            ("show disk usage", "du -h"),
            ("find large files", "find . -type f -size +100M"),
            ("show system memory", "free -h"),
            ("show directory structure", "tree"),
        ]
    
    def _initialize_model(self):
        """Download and initialize the model and tokenizer."""
        print(f"Loading model from {self.models_dir}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=self.models_dir
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                cache_dir=self.models_dir
            )
            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=100
            )
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Please ensure you have an internet connection for the first run.")
            sys.exit(1)
    
    @property
    def model_size(self) -> str:
        """Get the size of the downloaded model."""
        model_path = Path(self.models_dir)
        if not model_path.exists():
            return "Model not downloaded"
        
        total_size = sum(f.stat().st_size for f in model_path.rglob('*') if f.is_file())
        return f"{total_size / (1024 * 1024 * 1024):.1f} GB"
        
    def generate_command(self, query: str) -> str:
        """Generate a bash command based on the natural language query."""
        prompt = self._create_prompt(query)
        print(f"Generated prompt: {prompt}")
        response = self.pipe(prompt)[0]['generated_text']
        
        # Extract the command from the response
        try:
            command = response.split("Command:")[-1].strip()
            return command
        except Exception:
            return "Echo 'Could not generate a valid command'"
            
    def _create_prompt(self, query: str) -> str:
        """Create a prompt with examples and the current query."""
        prompt = "Convert natural language to bash commands. Examples:\n\n"
        for example_query, example_command in self.examples:
            prompt += f"Query: {example_query}\nCommand: {example_command}\n\n"
        prompt += f"Query: {query}\nCommand:"
        return prompt
    
    def execute_command(self, command: str) -> None:
        """Execute the generated bash command."""
        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            print(result.stdout)
            if result.stderr:
                print("Error:", result.stderr, file=sys.stderr)
        except Exception as e:
            print(f"Error executing command: {e}", file=sys.stderr)

def main():
    # Create bash assistant
    print("Initializing Bash Whisperer...")
    print("This might take a while on first run as the model needs to be downloaded.")
    
    assistant = BashAssistant()
    print(f"Model size on disk: {assistant.model_size}")
    
    while True:
        try:
            # Get user input
            query = input("\nEnter your query (or 'exit' to quit): ")
            
            if query.lower() == 'exit':
                break
                
            # Generate and show the command
            command = assistant.generate_command(query)
            print(f"\nGenerated command: {command}")
            
            # Ask for confirmation
            confirm = input("Execute this command? (y/n): ")
            if confirm.lower() == 'y':
                assistant.execute_command(command)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()