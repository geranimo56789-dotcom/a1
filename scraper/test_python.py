import sys
import requests
from PIL import Image
import os

print("Python is working!")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Test if required packages are available
try:
    print("✓ requests module available")
except ImportError:
    print("✗ requests module not available")

try:
    print("✓ PIL (Pillow) module available")
except ImportError:
    print("✗ PIL (Pillow) module not available")

print("\nPython installation is ready!")
