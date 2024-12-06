import os
import ast
import re
import sys
import subprocess
from typing import List, Dict
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DependencyConfig:
    """
    Configuration for dependency detection
    """
    ignore_stdlib: bool = True
    ignore_patterns: List[str] = field(default_factory=lambda: [
        r'^_', r'test_', r'conftest'
    ])
    additional_mappings: Dict[str, str] = field(default_factory=lambda: {
        'PIL': 'pillow',
        'cv2': 'opencv-python',
        'matplotlib.pyplot': 'matplotlib'
    })

class StdLibChecker:
    """
    Utility to check if a module is part of Python standard library
    """
    @staticmethod
    def is_stdlib(module_name: str) -> bool:
        """
        Check if module is part of Python standard library
        """
        try:
            spec = __import__(module_name)
            return spec.__spec__.origin is not None and 'site-packages' not in str(spec.__spec__.origin)
        except (ImportError, AttributeError):
            return False

class ModuleVisitor(ast.NodeVisitor):
    """
    AST Visitor to extract imported modules
    """
    def __init__(self):
        self.imports: set[str] = set()
    
    def visit_Import(self, node):
        """
        Handle direct imports
        """
        for alias in node.names:
            self.imports.add(alias.name.split('.')[0])
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """
        Handle from ... import statements
        """
        if node.module:
            self.imports.add(node.module.split('.')[0])
        self.generic_visit(node)

class DependencyDetector:
    """
    High-level dependency detection and requirements generation
    """
    def __init__(self, config: DependencyConfig = DependencyConfig()):
        """
        Initialize dependency detector
        
        Args:
            config (DependencyConfig): Configuration for dependency detection
        """
        self.config = config
        self.dependencies: set[str] = set()
    
    def _should_ignore(self, filename: str) -> bool:
        """
        Check if file should be ignored based on patterns
        
        Args:
            filename (str): Name of the file to check
        
        Returns:
            bool: Whether file should be ignored
        """
        return any(
            re.search(pattern, filename) 
            for pattern in self.config.ignore_patterns
        )
    
    def detect_dependencies(self, directory: str) -> set[str]:
        """
        Detect dependencies across Python files in a directory
        
        Args:
            directory (str): Path to directory to scan
        
        Returns:
            Set of detected dependencies
        """
        self.dependencies.clear()
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py') and not self._should_ignore(file):
                    filepath = os.path.join(root, file)
                    self._process_file(filepath)
        
        return self._process_dependencies()
    
    def _process_file(self, filepath: str):
        """
        Process individual Python file for imports
        
        Args:
            filepath (str): Path to Python file
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            visitor = ModuleVisitor()
            visitor.visit(tree)
            
            self.dependencies.update(visitor.imports)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    def _process_dependencies(self) -> set[str]:
        """
        Process and filter dependencies
        
        Returns:
            Set of processed dependencies
        """
        filtered_deps = set()
        
        for dep in self.dependencies:
            # Apply custom mappings
            if dep in self.config.additional_mappings:
                filtered_deps.add(self.config.additional_mappings[dep])
                continue
            
            # Ignore standard library
            if self.config.ignore_stdlib and StdLibChecker.is_stdlib(dep):
                continue
            
            filtered_deps.add(dep)
        
        return filtered_deps
    
    def generate_requirements(self, directory: str, output_path: str = 'requirements.txt'):
        """
        Generate requirements.txt file
        
        Args:
            directory (str): Directory to scan for dependencies
            output_path (str): Path to write requirements file
        
        Returns:
            Set of detected dependencies
        """
        dependencies = self.detect_dependencies(directory)
        
        # Try to get package versions
        versioned_deps = []
        for dep in dependencies:
            try:
                # Attempt to get package version
                output = subprocess.check_output(
                    [sys.executable, '-m', 'pip', 'show', dep],
                    universal_newlines=True
                )
                version = re.search(r'Version:\s*(\S+)', output)
                if version:
                    versioned_deps.append(f"{dep}=={version.group(1)}")
                else:
                    versioned_deps.append(dep)
            except subprocess.CalledProcessError:
                versioned_deps.append(dep)
        
        # Write requirements
        with open(output_path, 'w') as f:
            f.write('\n'.join(sorted(versioned_deps)))
        
        return dependencies

class DependencyManagerCLI:
    """
    Command-line interface for dependency management
    """
    def __init__(self):
        """
        Initialize CLI
        """
        self.detector = DependencyDetector()
    
    def run(self, directory: str = '.'):
        """
        Run dependency detection and provide installation option
        
        Args:
            directory (str): Directory to scan (default: current directory)
        """
        print(f"Scanning directory: {os.path.abspath(directory)}")
        
        # Detect and generate requirements
        try:
            dependencies = self.detector.generate_requirements(directory)
            
            print("\nDetected Dependencies:")
            for dep in sorted(dependencies):
                print(f"- {dep}")
            
            # Prompt for installation
            while True:
                choice = input("\nDo you want to install dependencies? (y/n): ").lower()
                
                if choice == 'y':
                    try:
                        print("\nInstalling dependencies...")
                        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
                        print("Dependencies installed successfully!")
                        break
                    except subprocess.CalledProcessError as e:
                        print(f"Error installing dependencies: {e}")
                        retry = input("Retry installation? (y/n): ").lower()
                        if retry != 'y':
                            break
                elif choice == 'n':
                    print("Exiting without installation.")
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
        
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    """
    Main entry point
    """
    cli = DependencyManagerCLI()
    
    # Allow directory specification as command-line argument
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    cli.run(directory)

if __name__ == '__main__':
    main()