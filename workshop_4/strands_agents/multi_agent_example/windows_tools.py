"""
Windows-compatible wrapper for strands_tools to handle Unix-specific module import issues
"""

import sys
import types

# Create mock modules for Unix-specific functionality
def create_mock_module(name, attributes=None):
    mock_module = types.ModuleType(name)
    if attributes:
        for attr_name, attr_value in attributes.items():
            setattr(mock_module, attr_name, attr_value)
    return mock_module

# Mock fcntl module
if 'fcntl' not in sys.modules:
    mock_fcntl = create_mock_module('fcntl', {
        'LOCK_EX': 2,
        'LOCK_NB': 4,
        'LOCK_SH': 1,
        'LOCK_UN': 8,
        'flock': lambda fd, operation: None
    })
    sys.modules['fcntl'] = mock_fcntl

# Mock termios module
if 'termios' not in sys.modules:
    mock_termios = create_mock_module('termios', {
        'TCSANOW': 0,
        'TCSADRAIN': 1,
        'TCSAFLUSH': 2,
        'tcgetattr': lambda fd: [],
        'tcsetattr': lambda fd, when, attrs: None,
        'tcdrain': lambda fd: None,
        'tcflush': lambda fd, queue: None,
        'tcflow': lambda fd, action: None
    })
    sys.modules['termios'] = mock_termios

# Mock tty module
if 'tty' not in sys.modules:
    mock_tty = create_mock_module('tty', {
        'setraw': lambda fd, when=None: None,
        'setcbreak': lambda fd, when=None: None
    })
    sys.modules['tty'] = mock_tty

# Mock pty module
if 'pty' not in sys.modules:
    mock_pty = create_mock_module('pty', {
        'openpty': lambda: (0, 1),
        'fork': lambda: (0, 0),
        'spawn': lambda argv, master_read=None, stdin_read=None: None
    })
    sys.modules['pty'] = mock_pty

# Now try importing the tools
try:
    from strands_tools import python_repl, shell, file_read, file_write, editor, calculator, http_request
except ImportError as e:
    print(f"Warning: Could not import some strands_tools: {e}")
    # Create minimal fallback tools if needed
    from strands import tool
    
    @tool
    def python_repl(code: str) -> str:
        """Fallback Python REPL that uses exec"""
        try:
            exec(code)
            return "Code executed successfully"
        except Exception as e:
            return f"Error: {e}"
    
    @tool 
    def shell(command: str) -> str:
        """Fallback shell command"""
        import subprocess
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
        except Exception as e:
            return f"Error: {e}"
    
    @tool
    def file_read(path: str) -> str:
        """Fallback file read"""
        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
    
    @tool
    def file_write(path: str, content: str) -> str:
        """Fallback file write"""
        try:
            with open(path, 'w') as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing file: {e}"
    
    @tool
    def editor(path: str, content: str) -> str:
        """Fallback editor"""
        return file_write(path, content)
    
    @tool
    def calculator(expression: str) -> str:
        """Fallback calculator"""
        try:
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {e}"
    
    @tool
    def http_request(url: str, method: str = "GET", **kwargs) -> str:
        """Fallback HTTP request"""
        import urllib.request
        try:
            with urllib.request.urlopen(url) as response:
                return response.read().decode()
        except Exception as e:
            return f"Error: {e}"

# Export the tools
__all__ = ['python_repl', 'shell', 'file_read', 'file_write', 'editor', 'calculator', 'http_request']